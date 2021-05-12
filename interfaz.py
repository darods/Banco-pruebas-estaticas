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

import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.dockarea import *


app = QtGui.QApplication([])

params = [
        {'name': 'Configuración de toma de datos', 'type': 'group', 'children': [
            {'name': 'Serial port', 'type': 'str', 'value': '/dev/ttyUSB0'},
            {'name': 'Baudrate', 'type': 'list', 'values': [9600, 38400, 115200], 'value': 9600},
            ]},
        {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
            {'name': 'Save State', 'type': 'action'},
            {'name': 'Restore State', 'type': 'action', 'children': [
                {'name': 'Add missing items', 'type': 'bool', 'value': True},
                {'name': 'Remove extra items', 'type': 'bool', 'value': True},
            ]},
        ]},
        {'name': 'Almacenamiento de datos', 'type': 'group', 'children': [
            {'name': 'Iniciar', 'type': 'action'},
            {'name': 'Detener', 'type': 'action'},
            ]},
        ]

p = Parameter.create(name='params', type='group', children=params)

## If anything changes in the tree, print a message
def change(param, changes):
    print("tree changes:")
    for param, change, data in changes:
        path = p.childPath(param)
        if path is not None:
            childName = '.'.join(path)
        else:
            childName = param.name()
        print('  parameter: %s'% childName)
        print('  change:    %s'% change)
        print('  data:      %s'% str(data))
        print('  ----------')

p.sigTreeStateChanged.connect(change)

def valueChanging(param, value):
    print("Value changing (not finalized): %s %s" % (param, value))
# Too lazy for recursion:
    for child in p.children():
        child.sigValueChanging.connect(valueChanging)
        for ch2 in child.children():
            ch2.sigValueChanging.connect(valueChanging)
def save():
    global state
    state = p.saveState()

def restore():
    global state
    add = p['Save/Restore functionality', 'Restore State', 'Add missing items']
    rem = p['Save/Restore functionality', 'Restore State', 'Remove extra items']
    p.restoreState(state, addChildren=add, removeChildren=rem)
p.param('Save/Restore functionality', 'Save State').sigActivated.connect(save)
p.param('Save/Restore functionality', 'Restore State').sigActivated.connect(restore)

## Create two ParameterTree widgets, both accessing the same data
t = ParameterTree()
t.setParameters(p, showTop=False)
t.setWindowTitle('pyqtgraph example: Parameter Tree')
#t2 = ParameterTree()
#t2.setParameters(p, showTop=False)


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

win = QtGui.QMainWindow()
area = DockArea()
win.setCentralWidget(area)

win.resize(1000, 600)
win.setWindowTitle('Curva de empuje')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


d1 = Dock("Dock1", size=(300, 500))
d2 = Dock("Dock2", size=(700, 500))
area.addDock(d1, 'left')
area.addDock(d2, 'right')
d1.addWidget(t)

s = p.saveState()
p.restoreState(s)


p1 = pg.PlotWidget(
    title="Semillero ATL - Grupo LIDER <br>Muestra y guarda la información de la curva de empuje")
p1.setClipToView(True)
p1.addLegend()

curva = p1.plot(pen="b", name=' gramos')
datos = np.linspace(0, 0)
d2.hideTitleBar()
d2.addWidget(p1)
win.show()

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

def start(state):
    if (state==True):
        while True:
            update()
    else:
        print('detenido')

def iniciar():
    start(True)

def detener():
    start(False)

p.param('Almacenamiento de datos', 'Iniciar').sigActivated.connect(iniciar)
p.param('Almacenamiento de datos', 'Detener').sigActivated.connect(detener)

if __name__ == '__main__':
    app.exec_()
