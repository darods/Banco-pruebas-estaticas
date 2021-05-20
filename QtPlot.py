from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint
from dataBase import data_base

class QtPlot(PlotWidget):
    def __init__(self, data_base):
        super().__init__()
        self.view = self.getViewBox()
        self.setAntialiasing(True)
        self.setTitle("Thrust curve")
        self.setLabel('bottom', "Time", units='s')
        self.setLabel('left', "Grams", units='g')
        self.showGrid(x=True, y=True, alpha=1.0)
        self.setMouseEnabled(x=True, y=False)
        self.data_base = data_base
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points
        self.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.plot(self.x, self.y, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        # plot data: x, y values
        #self.plot(self.hour, self.temperature)

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append( randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.
        values = [self.x, self.y]
        self.data_base.guardar(values)

