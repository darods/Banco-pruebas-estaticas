'''
Hecho por Daniel Alejandro Rodriguez - 2019
basado en : https://bit.ly/2RlMQj4
'''
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial
import time
import csv

puertoEncontrado = False
try:
    ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1)
    ser.flushInput()
    puertoEncontrado = True
except:
    print("Serial port not found!")

# QtGui.QApplication.setGraphicsSystem('raster')

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle('Curva de empuje')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


p1 = win.addPlot(
    title="Semillero ATL - Grupo LIDER <br>Muestra y guarda la información de la curva de empuje")
p1.setClipToView(True)
p1.addLegend()

curva = p1.plot(pen="b", name=' gramos')
datos = np.linspace(0, 0)


def update():
    global curva, datos, decoded_bytes
    datos[:-1] = datos[1:]
    
    if(puertoEncontrado == True):
        try:
            ser_bytes = ser.readline()
            decoded_bytes = float(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
            print(decoded_bytes)
        except ValueError:
            print(str(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")))
    else: decoded_bytes = np.random.random_sample()

    datos[-1] = decoded_bytes
    curva.setData(datos)
    QtGui.QApplication.processEvents()    # you MUST process the plot now
    with open("test_data.csv", "a") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow([time.asctime(), decoded_bytes])


Bandera = True
while Bandera:
    update()


if __name__ == '__main__':
    app.exec_()
