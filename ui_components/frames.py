import tkinter
from settings import Settings

from ui_components.plotting import Plotter

from device_io.v_out import set_output_voltage, volt_out

from motion_control import movement as move


class MainFrame(tkinter.Frame):
    """
    Creates and places the components on the GUI.
    """

    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # self.create_components()
        self.create_buttons()
        self.set_button_functions()

    def create_buttons(self):

        # Main canvas that contains all components
        self.main_canvas = tkinter.Canvas(
            master=self,
            bg=Settings.BG_COLOR,
            highlightthickness=0,
            height=Settings.HEIGHT,
            width=Settings.WIDTH,
        )
        self.main_canvas.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)

        # funcs = [
        #     move.se,
        #     move.neg_X,
        #     move.sw,
        #     move.neg_Y,
        #     move.stop_motors,
        #     move.pos_Y,
        #     move.ne,
        #     move.pos_X,
        #     move.nw,
        # ]

        icons = ['⭦', '⭡', '⭧', '⭠', 'S', '⭢', '⭩', '⭣', '⭨']

        buttons = []

        for i in range(3):
            for j in range(3):
                buttons.append(
                    self.tkButton(
                        self.main_canvas,
                        text=icons[3 * i + j],
                        command=lambda: print(icons[3 * i + j]),
                    )
                )
                buttons[3 * i + j].place(
                    x=j * 45 + 15, y=i * 45 + 15, width=45, height=45
                )
                print(3 * i + j)

        self.btn_home = self.tkButton(
            self.main_canvas, text='Home', command=lambda: print('Home')
        )
        self.btn_home.place(x=175, y=15 + 7, width=75, height=30)

        self.btn_square = self.tkButton(
            self.main_canvas, text='Square', command=lambda: print('Draw Square')
        )
        self.btn_square.place(x=175, y=60 + 7, width=75, height=30)

        self.btn_diamond = self.tkButton(
            self.main_canvas, text='Diamond', command=lambda: print('Draw Diamond')
        )
        self.btn_diamond.place(x=175, y=105 + 7, width=75, height=30)

    def create_components(self):
        """
        Creates all of the components and places them in their location on the GUI.
        """

        # Main canvas that contains all components
        self.main_canvas = tkinter.Canvas(
            master=self,
            bg=Settings.BG_COLOR,
            highlightthickness=0,
            height=Settings.HEIGHT,
            width=Settings.WIDTH,
        )
        self.main_canvas.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)

        # Create plotter
        self.plotter = Plotter(self.main_canvas)
        self.plot = self.plotter.plot(self.main_canvas)
        self.plot.draw()
        self.plot.get_tk_widget().place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        # Container frame to hold the motor buttons
        self.button_frame = tkinter.Frame(master=self, bg=Settings.BG_COLOR)
        self.button_frame.place(relx=0, rely=0, relheight=0.5, relwidth=1)

        # Container to hold the left motor buttons and labels
        self.motor_left = tkinter.Canvas(
            master=self.button_frame,
            bg=Settings.BG_COLOR,
            highlightthickness=0,
            height=Settings.CANVAS_SIZE / 2,
            width=Settings.CANVAS_SIZE,
        )
        self.motor_left.place(relx=0, rely=0.125, relheight=0.5, relwidth=0.5)

        # Left motor title label
        self.lbl_motor_left = self.tkLabel(master=self.motor_left, text="Left Motor")
        self.lbl_motor_left.place(anchor=tkinter.N, relx=0.5)

        # Left motor clockwise button
        self.btn_motor_left_CW = self.tkButton(
            self.motor_left, text="CW", command=lambda: print("left CW")
        )
        left_pos = 100
        self.btn_motor_left_CW.place(x=left_pos, y=35, width=45, height=45)

        # Left motor counterclockwise button
        self.btn_motor_left_CCW = self.tkButton(
            self.motor_left, text="CCW", command=lambda: print("left CCW")
        )
        self.btn_motor_left_CCW.place(x=left_pos + 55, y=35, width=45, height=45)

        # Left motor encoder label
        self.lbl_encoder_left = self.tkLabel(self.motor_left, text="Encoder Value: ")
        self.lbl_encoder_left.place(relx=0.25, y=100)

        # Left motor encoder value label
        self.lbl_encoder_left_val = self.tkLabel(
            self.motor_left, text=f"{self.parent.get_encoder_vals()}"
        )
        self.lbl_encoder_left_val.place(x=175, y=100)

        # Left motor voltage label
        self.lbl_voltage_left = self.tkLabel(self.motor_left, text="Voltage: ")
        self.lbl_voltage_left.place(relx=0.25, y=125)

        # Left motor voltage value label
        self.lbl_voltage_left_val = self.tkLabel(
            self.motor_left, text=f"{self.parent.get_encoder_vals()} V"
        )
        self.lbl_voltage_left_val.place(x=175, y=125)

        # Left motor laser label
        self.lbl_laser_left = self.tkLabel(self.motor_left, text="Laser Value: ")
        self.lbl_laser_left.place(relx=0.25, y=150)

        # Left motor laser value label
        self.lbl_laser_left_val = self.tkLabel(
            self.motor_left, text=f"{self.parent.get_encoder_vals()}"
        )
        self.lbl_laser_left_val.place(x=175, y=150)

        # Container to hold the right motor buttons and labels
        self.motor_right = tkinter.Canvas(
            master=self.button_frame,
            bg=Settings.BG_COLOR,
            highlightthickness=0,
            height=Settings.CANVAS_SIZE / 2,
            width=Settings.CANVAS_SIZE,
        )
        self.motor_right.place(relx=0.5, rely=0.125, relheight=0.5, relwidth=0.5)

        # Right motor title label
        self.lbl_motor_right = self.tkLabel(self.motor_right, text="Right Motor")
        self.lbl_motor_right.place(anchor=tkinter.N, relx=0.5)

        # Right motor clockwise button
        self.btn_motor_right_CW = self.tkButton(
            self.motor_right, text="CW", command=lambda: print("right CW")
        )
        pos_right = 100
        self.btn_motor_right_CW.place(x=pos_right, y=35, width=45, height=45)

        # Right motor counterclockwise button
        self.btn_motor_right_CCW = self.tkButton(
            self.motor_right, text="CCW", command=lambda: print("right CCW")
        )
        self.btn_motor_right_CCW.place(x=pos_right + 55, y=35, width=45, height=45)

        # Right encoder label
        self.lbl_encoder_right = self.tkLabel(self.motor_right, text="Encoder Value: ")
        self.lbl_encoder_right.place(relx=0.25, y=100)

        # Right encoder value label
        self.lbl_encoder_right_val = self.tkLabel(
            self.motor_right, text=f"{self.parent.get_encoder_vals()}"
        )
        self.lbl_encoder_right_val.place(x=175, y=100)

        # Right motor voltage label
        self.lbl_voltage_right = self.tkLabel(self.motor_right, text="Voltage: ")
        self.lbl_voltage_right.place(relx=0.25, y=125)

        # Right motor voltage value label
        self.lbl_voltage_right_val = self.tkLabel(
            self.motor_right, text=f"{self.parent.get_encoder_vals()} V"
        )
        self.lbl_voltage_right_val.place(x=175, y=125)

        # Stop button
        self.btn_stop = self.tkButton(
            self.button_frame, text="Stop", command=lambda: print("Stop")
        )
        self.btn_stop.place(x=275, y=73, width=45, height=45)

    def update_plot(self, y):
        self.plotter.update(y)
        self.plot = self.plotter.plot(self.main_canvas)
        self.plot.draw()
        self.plot.get_tk_widget().place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    def both(self):
        volt_out(1, 0, 1)
        volt_out(1, 1, 1)

    def set_button_functions(self):
        """
        Binds the GUI buttons to their respective functions.
        """
        # self.btn_motor_left_CW.config(command=lambda: set_output_voltage(1, 0, 0.1))
        self.btn_motor_left_CW.config(command=lambda: volt_out(1, 0, 2))
        self.btn_motor_left_CCW.config(command=lambda: volt_out(1, 0, -2))
        self.btn_motor_right_CW.config(command=lambda: volt_out(1, 1, 2))
        self.btn_motor_right_CCW.config(command=lambda: volt_out(1, 1, -2))
        self.btn_stop.config(command=move.stop_motors)

    def tkLabel(self, *args, **kwargs):
        """Simplifies creating labels with the same standard attributes"""
        return tkinter.Label(bg=Settings.BG_COLOR, fg="#FFFFFF", *args, **kwargs)

    def tkButton(self, *args, **kwargs):
        """Simplifies creating buttons with the same standard attributes"""
        return tkinter.Button(bg=Settings.BTN_COLOR, *args, **kwargs)
