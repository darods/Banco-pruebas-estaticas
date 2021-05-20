from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
from pyqtgraph.dockarea import *
from option_panel import tree_menu
from QtPlot import QtPlot
from dataBase import data_base

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.data_base = data_base()
        self.resize(1000,600)
        self.area = DockArea()
        self.setCentralWidget(self.area)
        self.d1 = Dock("Dock1", size=(700,600))
        self.d2 = Dock("Dock2", size=(300,600))
        self.area.addDock(self.d1, 'right')
        self.area.addDock(self.d2, 'left')
        self.graphWidget = QtPlot(self.data_base)
        self.tree = tree_menu(self.data_base)
        self.d1.addWidget(self.graphWidget)
        self.d2.addWidget(self.tree)
        
        # plot data: x, y values
        #self.graphWidget.plot(hour, temperature)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
