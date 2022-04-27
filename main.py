from time import time
import tkinter
import os

from settings import Settings

from ui_components.frames import MainFrame
from ui_components.timing import Timer

from motion_control import movement as move

# from motion.wrapper_new import cb_C7266_config
from motion_control.sensors import LaserSensor, MotorEncoder


class App(tkinter.Tk):
    """
    Main window and loop of the program.  Creates the GUI window, initializes the sensors and handles updating.

    Methods:
        bind_keys : connects keyboard bindings to functions.
        draw_main_frame : sets the initial parameters for the GUI window and displays it.
        get_encoder_values : reads the values on each of the 4 counter channels.
        on_closing : code executed when the GUI is closed or force quit.
        update_GUI : updates the GUI components with the sensor values.
        run : main program loop.
    """

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.main_path = os.path.dirname(os.path.abspath(__file__))

        self.encoder = MotorEncoder(Settings.ENCODER_BOARD_NUM)
        self.laser_1 = LaserSensor(Settings.ADC_BOARD_NUM, Settings.LASER_1_CHANNEL)
        self.laser_2 = LaserSensor(Settings.ADC_BOARD_NUM, Settings.LASER_2_CHANNEL)
        self.timer = Timer(Settings.HZ)

        self.main_frame = MainFrame(self)

        # self.devices = self.connect_to_devices()

        # Handle window closing event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Sets up the keybindings
        self.bind_keys()

        # Display the GUI
        self.draw_main_frame()

        self.running = True

    def bind_keys(self):
        """Assigns the events to the keyboard keys"""

        # Handle force quit kyboard shortcut
        self.bind("<Alt-Key-F4>", self.on_closing)

        # Assign the keys which move the end effector
        v = Settings.MOTOR_VOLTAGE_OUT
        self.bind("<Left>", lambda e: move.pos_Y(v))
        self.bind("<Right>", lambda e: move.neg_Y(v))
        self.bind("<Down>", lambda e: move.pos_X(v))
        self.bind("<Up>", lambda e: move.neg_X(v))
        self.bind("<space>", lambda e: move.stop_motors())
        self.bind("s", lambda e: move.draw_square(1.5))
        self.bind("d", lambda e: move.draw_diamond(2.15))

    def draw_main_frame(self, event=0):
        """Initializes the GUI window settings and displays it."""

        self.title(Settings.APP_NAME)
        self.geometry(f"{Settings.WIDTH}x{Settings.HEIGHT}")
        self.resizable(True, True)
        self.minsize(Settings.WIDTH, Settings.HEIGHT)
        self.maxsize(Settings.MAX_WIDTH, Settings.MAX_HEIGHT)

        self.main_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    def read_from_devices(self):
        # print(self.encoder.get_counter_value(counter_num=1))
        # print(self.encoder.get_all_counter_values())
        # print(self.laser_1.read_laser_value())
        pass

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

        self.main_frame.lbl_encoder_left_val.config(text=self.get_encoder_vals()[0])
        self.main_frame.lbl_encoder_right_val.config(text=self.get_encoder_vals()[1])

        self.main_frame.lbl_voltage_left.config(text="Laser 1: ")
        self.main_frame.lbl_voltage_left_val.config(
            text=round(self.laser_1.read_laser_value()[1], 1)
        )
        self.main_frame.lbl_voltage_right.config(text="Laser 2: ")
        self.main_frame.lbl_voltage_right_val.config(
            text=round(self.laser_2.read_laser_value()[1], 1)
        )

    def run(self):
        """Main program loop"""

        start_time = time()

        while self.running:

            # self.main_frame.update_plot(a)
            # move.adjust_speed(self.laser_1.read_laser_value()[1])
            if time() - start_time >= Settings.TIME_DELTA:
                self.read_from_devices()
                self.update_GUI()
                self.update()
                start_time = time()
                # self.timer.wait()

        move.stop_motors()


if __name__ == "__main__":
    """Start the applicaiton."""
    App().run()
