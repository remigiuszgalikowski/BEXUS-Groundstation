from PyQt5.QtWidgets import QWidget, QVBoxLayout
from pyqtgraph import PlotWidget
import pyqtgraph as pg


class Charts(QWidget):

    def __init__(self, *args, structure, units, **kwargs):
        super(Charts, self).__init__(*args, **kwargs)

        #MAIN LAYOUT
        self.layout = QVBoxLayout()

        self.primaryKeys = list(structure.keys())
        self.secondaryKeys = []

        self.plotWidgets = []
        self.lines = []

        self.indeces = []
        self.data = []
        self.isAvg = []

        self.time = [0]
        self.timeAvg = [0]
        self.timeIndex = structure[self.primaryKeys[1]]

        #ALTITUDE
        self.plotWidgets.append(PlotWidget())
        self.plotWidgets[-1].setMinimumSize(0, 200)
        self.plotWidgets[-1].setMouseEnabled(False, False)
        self.plotWidgets[-1].setTitle(self.primaryKeys[2])
        self.plotWidgets[-1].setLabel('left', units[self.primaryKeys[2].lower()]['name'] + ' [' + units[self.primaryKeys[2].lower()]['symbol'] + ']')
        self.plotWidgets[-1].setLabel('bottom', 'time [hh/mm/ss]')
        self.indeces.append([])
        self.data.append([])
        self.isAvg.append([])
        self.lines.append([])
        self.indeces[-1].append(structure[self.primaryKeys[1]])
        self.data[-1].append([0])
        self.isAvg[-1].append(False)
        self.lines[-1].append(self.plotWidgets[-1].plot(self.time, self.data[-1][-1]))

        #LOWER LAYER OF DATA
        for p in range(3,len(self.primaryKeys)):
            self.secondaryKeys = list(structure[self.primaryKeys[p]].keys())
            for s in range(len(structure[self.primaryKeys[p]][self.secondaryKeys[0]])):
                self.plotWidgets.append(PlotWidget())
                self.plotWidgets[-1].setMinimumSize(0,200)
                self.plotWidgets[-1].setMouseEnabled(False, False)
                self.plotWidgets[-1].setTitle(self.primaryKeys[p] + ' ' + structure[self.primaryKeys[p]][self.secondaryKeys[0]][s])
                self.plotWidgets[-1].setLabel('left', units[self.primaryKeys[p].lower()]['name'] + ' [' + units[self.primaryKeys[p].lower()]['symbol'] + ']')
                self.plotWidgets[-1].setLabel('bottom', 'time [hh/mm/ss]')
                self.indeces.append([])
                self.data.append([])
                self.isAvg.append([])
                self.lines.append([])
                for v in range(1,len(structure[self.primaryKeys[p]])):
                    if 'average' in self.secondaryKeys[v].lower():
                        self.indeces[-1].append(structure[self.primaryKeys[p]][self.secondaryKeys[v]][s])
                        self.data[-1].append([0])
                        self.lines[-1].append(self.plotWidgets[-1].plot(self.timeAvg, self.data[-1][-1], pen = pg.mkPen(color=(0, 255, 0))))
                        self.isAvg[-1].append(True)
                    elif 'current' in self.secondaryKeys[v].lower():
                        self.indeces[-1].append(structure[self.primaryKeys[p]][self.secondaryKeys[v]][s])
                        self.data[-1].append([0])
                        self.lines[-1].append(self.plotWidgets[-1].plot(self.time, self.data[-1][-1]))
                        self.isAvg[-1].append(False)

        #some clearing
        self.primaryKeys.clear()
        self.secondaryKeys.clear()
        del self.primaryKeys
        del self.secondaryKeys

        #adding widgets to layout
        for pw in self.plotWidgets:
            self.layout.addWidget(pw)

        #setting layout for custom widget
        self.setLayout(self.layout)

    def update(self, input):

        #cutting out excess of chart
        t = len(self.time)
        w = self.geometry().width() / 3
        if t > w:
            r = int(abs(t - w))
            for _ in range(r):
                for i in range(len(self.data)):
                    for j in range(len(self.data[i])):
                        if not self.isAvg[i][j]:
                            self.data[i][j].pop(0)
                self.time.pop(0)

        #adding new data from input
        self.time.append(input[self.timeIndex])
        self.timeAvg.clear()
        self.timeAvg.extend([self.time[0], self.time[-1]])

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.isAvg[i][j]:
                    self.data[i][j].clear()
                    self.data[i][j].extend([input[self.indeces[i][j]], input[self.indeces[i][j]]])
                else:
                    self.data[i][j].append(input[self.indeces[i][j]])

        #updating lines
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i])):
                if self.isAvg[i][j]:
                    self.lines[i][j].setData(self.timeAvg, self.data[i][j])
                else:
                    self.lines[i][j].setData(self.time, self.data[i][j])