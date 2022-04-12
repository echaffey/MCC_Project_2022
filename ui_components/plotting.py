import numpy as np
from settings import Settings

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Plotter:
    def __init__(self, master, *args, **kwargs):
        self.y = np.zeros(100)
        self.max_vals = 100

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.fig.patch.set_facecolor(Settings.BG_COLOR)
        self.ax = self.fig.add_subplot(111)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().label.set_color("white")
        self.ax.set_facecolor(Settings.BG_COLOR)

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)

    def update(self, y):
        if type(y) == list and len(y) > self.y.shape[0]:
            if not self.y.shape[0] == len(y):
                self.y = np.vstack((self.y, np.zeros((len(y) - 1, 100))))

            for i, val in enumerate(y):
                if self.y.shape[1] > self.max_vals - 1:
                    self.y = self.y[:, 1:]

                self.y = np.append(self.y[i], val, axis=0)

        else:
            if len(self.y) > self.max_vals - 1:
                self.y = self.y[1:]

            self.y = np.append(self.y, y)

    def plot(self, master):

        self.ax.clear()
        self.ax.plot(self.y)
        self.canvas.draw()

        return self.canvas
