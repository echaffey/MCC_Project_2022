import os
import tkinter
from time import sleep, time

# Import the user defined settings in \settings.py
from settings import Settings

# Import from files located in the ...\h_frame_positioner\ folder
from ui_components.frames import MainWindow
from motion_control import movement as move
from motion_control.sensors import LaserSensor, LimitSensors, MotorEncoder
from motion_control.movement import Speed


class App(tkinter.Tk):
    """
    Main window and loop of the program.  Creates the GUI window, initializes the sensors and handles updating.

    Methods:
        bind_keys : connects keyboard bindings to functions.
        draw_main_window : sets the initial parameters for the GUI window and displays it.
        get_encoder_values : reads the values on each of the 4 counter channels.
        on_closing : code executed when the GUI is closed or force quit.
        update_GUI : updates the GUI components with the sensor values.
        run : main program loop.
    """

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        # Sets the current working directory
        self.main_path = os.path.dirname(os.path.abspath(__file__))

        # Creates the encoder and laser objects
        self.encoder = MotorEncoder(Settings.ENCODER_BOARD_NUM)
        self.laser_1 = LaserSensor(Settings.ADC_BOARD_NUM, Settings.LASER_1_CHANNEL)
        self.laser_2 = LaserSensor(Settings.ADC_BOARD_NUM, Settings.LASER_2_CHANNEL)
        self.limit_sensors = LimitSensors(
            Settings.ADC_BOARD_NUM,
            Settings.LIMIT_SENSORS,
        )

        # Defines the default value for the motor voltage
        self.motor_voltage = Settings.MOTOR_VOLTAGE_DEFAULT

        # Create the main GUI window
        self.main_window = MainWindow(self)

        # Handle window closing event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Sets up the keybindings
        self.bind_keys()

        # Display the GUI
        self.draw_main_window()

        self.homing_position = None

        self.running = True

    def bind_keys(self, event=None):
        """Assigns the events to the keyboard keys"""

        # Handle force quit kyboard shortcut
        self.bind("<Alt-Key-F4>", self.on_closing)

        v = self.motor_voltage

        # Assign the keyboard keys that move the end effector
        self.bind("<Left>", lambda e: move.pos_Y(v))
        self.bind("<Right>", lambda e: move.neg_Y(v))
        self.bind("<Down>", lambda e: move.pos_X(v))
        self.bind("<Up>", lambda e: move.neg_X(v))
        self.bind("<space>", lambda e: move.stop_motors())
        self.bind("s", lambda e: move.draw_square(1.5))
        self.bind("d", lambda e: move.draw_diamond(2.15))

        # Functions to be assigned to the directional buttons
        funcs = [
            lambda: move.se(v),
            lambda: move.neg_X(v),
            lambda: move.sw(v),
            lambda: move.pos_Y(v),
            lambda: move.stop_motors(),
            lambda: move.neg_Y(v),
            lambda: move.ne(v),
            lambda: move.pos_X(v),
            lambda: move.nw(v),
        ]

        # Loop through the directional button grid and assign the functions
        for row in range(3):
            for col in range(3):
                self.main_window.buttons[row * 3 + col].config(
                    command=funcs[row * 3 + col]
                )
        # Set up homing button
        self.main_window.btn_home.config(command=lambda: self.homing_sequence())
        # Set up shape buttons
        self.main_window.btn_square.config(command=lambda: move.draw_square(v))
        self.main_window.btn_diamond.config(command=lambda: move.draw_diamond(v))

        # Assign range to the voltage level slider. bind_keys is called when the
        # slider is change to update voltage to the new value.
        min_v = 0
        max_v = Settings.MOTOR_VOLTAGE_ALLOWABLE
        self.main_window.sldr_voltage.config(
            variable=self.motor_voltage, from_=min_v, to=max_v, command=self.bind_keys
        )

    def draw_main_window(self, event=0):
        """Initializes the GUI window settings and displays it."""

        self.title(Settings.APP_NAME)
        self.geometry(f"{Settings.WIDTH}x{Settings.HEIGHT}")
        self.resizable(True, True)
        self.minsize(Settings.WIDTH, Settings.HEIGHT)
        self.maxsize(Settings.MAX_WIDTH, Settings.MAX_HEIGHT)

        self.main_window.place(relx=0, rely=0, relheight=1, relwidth=1)

    def get_encoder_vals(self):
        """Reads all 4 of the encoder counter values"""

        return self.encoder.get_all_counter_values()

    def on_closing(self, event=0):
        """Handles the window closing events to ensure that the motors stop on exit."""

        move.stop_motors()
        self.running = False
        self.quit()
        self.destroy()

    def update_GUI(self):
        """Updates the GUI label components with the values read from the sensors."""

        # Update the labels with the current encoder values
        self.main_window.lbl_encoder_vals.config(
            text="\n".join([str(val) for val in self.get_encoder_vals()[:2]])
        )

        # Read the voltage value from both lasers
        laser_vals = [
            self.laser_1.read_laser_value()[1],
            self.laser_2.read_laser_value()[1],
        ]

        # Update the labels with the current laser values
        self.main_window.lbl_laser_vals.config(
            text="\n".join([str(round(val, 2)) for val in laser_vals])
        )

        # Update the motor voltage variable with the current value of the slider
        self.motor_voltage = self.main_window.sldr_voltage.get()

        # Update visualization
        gantry = self.main_window.vis_gantry
        effector = self.main_window.vis_effector

        x1, y1, x2, y2 = self.main_window.frame_visualization.coords(gantry)
        u1, v1, u2, v2 = self.main_window.frame_visualization.coords(effector)

        self.main_window.frame_visualization.move(
            gantry, x1, Speed.speed_2 / 5 * y1 / 15
        )

        self.main_window.frame_visualization.move(
            effector, u1, Speed.speed_2 / 5 * y1 / 15
        )

        # Read from the limit switches
        limit_vals = self.limit_sensors.read_switches()

        # Update limit switch visualizations
        self.main_window.update_limit_sensor_indicators(limit_vals)

        # Get the current x, y position of the end effector in inches from the origin
        if self.homing_position is not None:
            pos1, pos2 = self.get_encoder_vals()[:2]

            # TODO: Need to figure out how to account for the counter rolling over back to 0
            # If current position is < home position
            if pos1 < self.homing_position[0]:

                pos1 = Settings.ENCODER_VALUES - self.homing_position[0] + pos1

            else:
                pos1 = pos1 - self.homing_position[0]

            if pos2 < self.homing_position[1]:
                pos2 = Settings.ENCODER_VALUES - self.homing_position[1] + pos2

            else:
                pos2 = pos2 - self.homing_position[1]

            print(move.get_pos(pos1, pos2))

            # print(move.get_pos(pos1, pos2))

            # print(
            #     move.get_pos(
            #         pos1 - self.homing_position[0], pos2 - self.homing_position[1]
            #     )
            # )
            # print(pos1, pos2)
            # print(self.homing_position[0] - pos1, self.homing_position[1] - pos2)

    def homing_sequence(self):
        homing_voltage = 1.5
        home = False

        move.nw(homing_voltage)

        # Initial position finding
        while not home:
            limit_vals = self.limit_sensors.read_switches()
            self.update_GUI()
            self.update()

            # If S3 triggered
            if limit_vals[2]:
                move.pos_X(homing_voltage)

            # If S4 triggered
            if limit_vals[3]:
                move.neg_Y(homing_voltage)

            if limit_vals[2] and limit_vals[3]:
                home = True

        # Get the current encoder values
        e_1, e_2 = self.get_encoder_vals()[:2]
        print("Initial", e_1, e_2)
        home = False

        move.pos_Y(1)
        sleep(1)
        move.neg_Y(0.6)

        # Check Y axis
        while not home:
            limit_vals = self.limit_sensors.read_switches()
            self.update_GUI()
            self.update()

            if limit_vals[2]:
                home = True
                e_1, e_2 = self.get_encoder_vals()[:2]
                print("Y", e_1, e_2)

        home = False

        move.neg_X(1)
        sleep(1)
        move.pos_X(0.6)

        # Check X axis
        while not home:
            limit_vals = self.limit_sensors.read_switches()
            self.update_GUI()
            self.update()

            if limit_vals[3]:
                home = True
                e_1, e_2 = self.get_encoder_vals()[:2]
                print("X", e_1, e_2)

        move.stop_motors()

        # Store encoder position at homing location
        self.homing_position = (e_1, e_2)

    def run(self):
        """Main program loop. This will run at the frequency specified in the settings.py file for HZ"""

        start_time = time()

        # self.homing_sequence()

        while self.running:
            if time() - start_time >= Settings.TIME_DELTA:
                self.update_GUI()
                self.update()
                start_time = time()

        # Redundancy to make sure that the motors are stopped when running = False
        move.stop_motors()


if __name__ == "__main__":
    """Start the applicaiton."""
    App().run()
