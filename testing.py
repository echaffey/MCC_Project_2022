import tkinter

# from motion_control import movement as move
from settings import Settings


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

        self.create_buttons()

        self.title(Settings.APP_NAME)
        self.geometry(f"{Settings.WIDTH}x{Settings.HEIGHT}")
        self.resizable(True, True)
        self.minsize(Settings.WIDTH, Settings.HEIGHT)
        self.maxsize(Settings.MAX_WIDTH, Settings.MAX_HEIGHT)

        self.line_id = None
        self.line_points = []
        self.line_options = {}

        self.drawing.bind("<Button-1>", self.set_start)
        self.drawing.bind("<B1-Motion>", self.draw_line)
        self.drawing.bind("<ButtonRelease-1>", self.end_line)

        self.mainloop()

        # self.main_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    def draw_line(self, event):
        self.line_points.extend((event.x, event.y))
        if self.line_id is not None:
            self.drawing.delete(self.line_id)
        self.line_id = self.drawing.create_line(self.line_points, **self.line_options)

    def set_start(self, event):
        self.line_points.extend((event.x, event.y))

    def end_line(self, event=None):
        self.line_points.clear()
        self.line_id = None

    def tkButton(self, *args, **kwargs):
        """Simplifies creating buttons with the same standard attributes"""
        return tkinter.Button(bg=Settings.BTN_COLOR, fg="#FFFFFF", *args, **kwargs)

    def tkLabel(self, *args, **kwargs):
        """Simplifies creating labels with the same standard attributes"""
        return tkinter.Label(
            bg=Settings.BG_COLOR, fg="#FFFFFF", font=("", 10), *args, **kwargs
        )

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

        self.drawing = tkinter.Canvas(
            master=self.main_canvas,
            bg="white",
            highlightthickness=0,
            height=Settings.HEIGHT / 2,
            width=Settings.WIDTH / 2,
        )
        self.drawing.place(x=0, y=Settings.WIDTH / 2 - 100)

        icons = ["⭦", "⭡", "⭧", "⭠", "Stop", "⭢", "⭩", "⭣", "⭨"]
        # icons = ['nw', 'up', 'ne', 'w', 'S', 'E', 'sw', 's', 'se']

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
            self.main_canvas, text="Home", command=lambda: print("Home")
        )
        self.btn_home.place(x=175, y=15 + 7, width=75, height=30)

        self.btn_square = self.tkButton(
            self.main_canvas, text="Square", command=lambda: print("Draw Square")
        )
        self.btn_square.place(x=175, y=60 + 7, width=75, height=30)

        self.btn_diamond = self.tkButton(
            self.main_canvas, text="Diamond", command=lambda: print("Draw Diamond")
        )
        self.btn_diamond.place(x=175, y=105 + 7, width=75, height=30)

        self.btn_draw = self.tkButton(
            self.main_canvas, text="Draw", command=lambda: print("Draw Diamond")
        )
        self.btn_draw.place(x=325, y=200, width=55, height=30)

        self.btn_clear = self.tkButton(
            self.main_canvas, text="Clear", command=lambda: self.drawing.delete("all")
        )
        self.btn_clear.place(x=325, y=245, width=55, height=30)

        # Create labels
        self.lbl_encoders = self.tkLabel(self.main_canvas, text="Encoder Values:")
        self.lbl_encoders.place(x=275, y=15, width=95, height=25)

        self.lbl_encoder_vals = self.tkLabel(self.main_canvas, text="PLACEHOLDER")
        self.lbl_encoder_vals.place(x=275, y=45, width=95, height=25)

        self.lbl_lasers = self.tkLabel(self.main_canvas, text="Laser Values: ")
        self.lbl_lasers.place(x=425, y=15, width=95, height=25)

        self.lbl_laser_vals = self.tkLabel(self.main_canvas, text="PLACEHOLDER")
        self.lbl_laser_vals.place(x=430, y=45, width=95, height=25)


if __name__ == "__main__":
    App()
