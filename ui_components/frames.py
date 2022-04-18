import tkinter

# Import from the files contained in this project
from settings import Settings
from device_io.v_out import volt_out
from ui_components.plotting import Plotter
from motion_control import movement as move


class MainWindow(tkinter.Frame):
    """
    Creates and places the components on the GUI window.
    """

    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.create_components()
        self.create_drawing_frame()
        self.create_visualization_frame()

    def create_components(self):

        # Main canvas that contains all components
        self.main_canvas = tkinter.Canvas(
            master=self,
            bg=Settings.BG_COLOR,
            highlightthickness=0,
            height=Settings.HEIGHT,
            width=Settings.WIDTH,
        )
        self.main_canvas.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)

        icons = ["⭦", "⭡", "⭧", "⭠", "Stop", "⭢", "⭩", "⭣", "⭨"]

        self.buttons = []

        # Create 3x3 grid for the directional buttons
        for i in range(3):
            for j in range(3):

                # Adjust font size only for the arrows
                if (3 * i + j) == 4:
                    font = 11
                else:
                    font = 18

                self.buttons.append(
                    self.tkButton(
                        self.main_canvas,
                        text=icons[3 * i + j],
                        command=lambda: print(icons[3 * i + j]),
                        font=("", font),
                    )
                )
                self.buttons[3 * i + j].place(
                    x=j * 45 + 15, y=i * 45 + 15, width=45, height=45
                )

        # Create function buttons
        self.btn_home = self.tkButton(
            self.main_canvas,
            text="Home",
            command=lambda: print("Home"),
            font=("", 11),
        )
        self.btn_home.place(x=175, y=15 + 7, width=75, height=30)

        self.btn_square = self.tkButton(
            self.main_canvas,
            text="Square",
            command=lambda: print("Draw Square"),
            font=("", 11),
        )
        self.btn_square.place(x=175, y=60 + 7, width=75, height=30)

        self.btn_diamond = self.tkButton(
            self.main_canvas,
            text="Diamond",
            command=lambda: print("Draw Diamond"),
            font=("", 11),
        )
        self.btn_diamond.place(x=175, y=105 + 7, width=75, height=30)

        self.btn_draw = self.tkButton(
            self.main_canvas,
            text="Draw",
            command=lambda: print("Draw Diamond"),
            font=("", 11),
        )
        self.btn_draw.place(x=325, y=200, width=55, height=30)

        self.btn_clear = self.tkButton(
            self.main_canvas,
            text="Clear",
            command=lambda: self.drawing.delete("all"),
            font=("", 11),
        )
        self.btn_clear.place(x=390, y=200, width=55, height=30)

        # Create labels
        self.lbl_encoders = self.tkLabel(
            self.main_canvas, text="Encoder Values:", font=("", 11)
        )
        self.lbl_encoders.place(x=275, y=15, width=105, height=25)

        self.lbl_encoder_vals = self.tkLabel(
            self.main_canvas, text="PLACEHOLDER", font=("", 10)
        )
        self.lbl_encoder_vals.place(x=275, y=40, width=95, height=30)

        self.lbl_lasers = self.tkLabel(
            self.main_canvas, text="Laser Values: ", font=("", 11)
        )
        self.lbl_lasers.place(x=425, y=15, width=95, height=25)

        self.lbl_laser_vals = self.tkLabel(
            self.main_canvas, text="PLACEHOLDER", font=("", 10)
        )
        self.lbl_laser_vals.place(x=430, y=40, width=95, height=30)

        self.lbl_output_voltage = self.tkLabel(
            self.main_canvas, text="Motor Voltage: ", font=("", 11)
        )
        self.lbl_output_voltage.place(x=275, y=85, width=95, height=20)

        # Create voltage slider
        self.sldr_voltage = tkinter.Scale(
            self.main_canvas,
            orient=tkinter.HORIZONTAL,
            bg=Settings.BG_COLOR,
            fg="#FFFFFF",
            borderwidth=0,
            resolution=0.5,
            relief=tkinter.FLAT,
            highlightthickness=0,
        )
        self.sldr_voltage.set(Settings.MOTOR_VOLTAGE_DEFAULT)
        self.sldr_voltage.place(x=275, y=105, width=275, height=45)

    def create_visualization_frame(self):
        self.frame_visualization = tkinter.Canvas(
            master=self.main_canvas,
            bg=Settings.BG_COLOR,
            highlightthickness=0,
            height=Settings.HEIGHT / 3 + 50,
            width=Settings.WIDTH / 3 + 25,
        )
        self.frame_visualization.place(
            x=Settings.WIDTH / 2 + 40, y=Settings.HEIGHT / 2 - 50
        )

        # Left rail
        self.frame_visualization.create_rectangle(
            0, 0, 15, Settings.HEIGHT / 3 + 49, fill="#c8c8c8"
        )
        # Right rail
        self.frame_visualization.create_rectangle(
            Settings.WIDTH / 3 + 9,
            0,
            Settings.WIDTH / 3 + 25,
            Settings.HEIGHT / 3 + 49,
            fill="#c8c8c8",
        )

        self.vis_gantry = self.frame_visualization.create_rectangle(
            0,
            Settings.HEIGHT / 3 + 34,
            Settings.WIDTH / 3 + 25,
            Settings.HEIGHT / 3 + 50,
            fill="#c8c8c8",
        )

    def create_drawing_frame(self):
        self.drawing = tkinter.Canvas(
            master=self.main_canvas,
            bg="white",
            highlightthickness=0,
            height=Settings.HEIGHT / 2,
            width=Settings.WIDTH / 2,
        )
        self.drawing.place(x=15, y=Settings.WIDTH / 2 - 100)

        def draw_line(self, event):
            self.line_points.extend((event.x, event.y))
            if self.line_id is not None:
                self.drawing.delete(self.line_id)
            self.line_id = self.drawing.create_line(
                self.line_points, **self.line_options
            )

        def set_start(self, event):
            self.line_points.extend((event.x, event.y))

        def end_line(self, event=None):
            self.line_points.clear()
            self.line_id = None

    def tkLabel(self, *args, **kwargs):
        """Simplifies creating labels with the same standard attributes"""
        return tkinter.Label(bg=Settings.BG_COLOR, fg="#FFFFFF", *args, **kwargs)

    def tkButton(self, *args, **kwargs):
        """Simplifies creating buttons with the same standard attributes"""
        return tkinter.Button(bg=Settings.BTN_COLOR, fg="#FFFFFF", *args, **kwargs)
