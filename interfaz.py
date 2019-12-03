from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from numpy import *
import serial

# Variables del puerto serial
portName = '/dev/ttyACM0'
baudrate = 38400
ser = serial.Serial(portName, baudrate)

pg.setConfigOption('background', (227, 229, 219))
pg.setConfigOption('foreground', 'k')
# Variables de la interfaz
app = QtGui.QApplication([])
view = pg.GraphicsView()
Grafico = pg.GraphicsLayout()
view.setCentralItem(Grafico)
view.show()
view.setWindowTitle('Monitereo de vuelo')
view.resize(800, 600)
