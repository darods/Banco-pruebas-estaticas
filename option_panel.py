from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.dockarea import *
from dataBase import data_base


class tree_menu(ParameterTree):
    def __init__(self, data_base):
        super().__init__()
        self.data_base = data_base
        self.setParameters(self.get_parameters(), showTop=False)
        self.setWindowTitle('parameterTree')

    def get_parameters(self):
        self.params = [
        {'name': 'Configuración de toma de datos', 'type': 'group', 'children': [
            {'name': 'Serial port', 'type': 'str', 'value': '/dev/ttyUSB0'},
            {'name': 'Baudrate', 'type': 'list', 'values': [9600, 38400, 115200], 'value': 9600},
            ]},
        #{'name': 'Save/Restore functionality', 'type': 'group', 'children': [
        #    {'name': 'Save State', 'type': 'action'},
        #    {'name': 'Restore State', 'type': 'action', 'children': [
        #        {'name': 'Add missing items', 'type': 'bool', 'value': True},
        #        {'name': 'Remove extra items', 'type': 'bool', 'value': True},
        #    ]},
        #]},
        {'name': 'Almacenamiento de datos', 'type': 'group', 'children': [
            {'name': 'Iniciar', 'type': 'action'},
            {'name': 'Detener', 'type': 'action'},
            ]},
        ]

        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.p.sigTreeStateChanged.connect(self.change)
        self.p.param('Almacenamiento de datos', 'Iniciar').sigActivated.connect(self.data_base.start)
        self.p.param('Almacenamiento de datos', 'Detener').sigActivated.connect(self.data_base.stop)

        #self.p.param('Save/Restore functionality', 'Save State').sigActivated.connect(self.save)
        #self.p.param('Save/Restore functionality', 'Restore State').sigActivated.connect(self.restore)
        return  self.p

    def change(self, param, changes):
        print("tree changes:")
        for param, change, data in changes:
            path = self.p.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()
            print('  parameter: %s'% childName)
            print('  change:    %s'% change)
            print('  data:      %s'% str(data))
        print('  ----------')

    def valueChanging(self, param, value):
        print("Value changing (not finalized): %s %s" % (param, value))
    # Too lazy for recursion:
        for child in self.p.children():
            child.sigValueChanging.connect(valueChanging)
            for ch2 in child.children():
                ch2.sigValueChanging.connect(valueChanging)
    def save(self):
        global state
        state = self.p.saveState()

    def restore(self):
        global state
        add = self.p['Save/Restore functionality', 'Restore State', 'Add missing items']
        rem = self.p['Save/Restore functionality', 'Restore State', 'Remove extra items']
        self.__init__p.restoreState(state, addChildren=add, removeChildren=rem)




