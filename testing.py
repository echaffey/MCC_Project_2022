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

        self.mainloop()

        # self.main_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    def tkButton(self, *args, **kwargs):
        """Simplifies creating buttons with the same standard attributes"""
        return tkinter.Button(bg=Settings.BTN_COLOR, *args, **kwargs)

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

        # Container frame to hold the motor buttons
        # self.button_frame = tkinter.Frame(master=self, bg=Settings.BG_COLOR)
        # self.button_frame.place(relx=0, rely=0, relheight=0.5, relwidth=1)

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

        icons = ['⭦', '⭡', '⭧', '⭠', 'Stop', '⭢', '⭩', '⭣', '⭨']
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


if __name__ == '__main__':
    App()
