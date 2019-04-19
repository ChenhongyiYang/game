import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class mainBoard(QMainWindow):
    def show(self):
        self.widget.show()

    def setupGUI(self):
        self.widget.setWindowTitle(' Board Game ')
        self.widget.resize(self.width, self.height)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        hbox = QHBoxLayout(self.widget)

        # set up two panels
        self.panelcheck = QFrame(self.widget)
        self.panelcheck.setFrameShape(QFrame.StyledPanel)
        self.panelgrid = QFrame(self.widget)
        self.panelgrid.setFrameShape(QFrame.StyledPanel)
        self.setupCheckBoxPanel()

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.panelcheck)
        splitter.addWidget(self.panelgrid)
        splitter.setStretchFactor(0, self.ratio1)
        splitter.setStretchFactor(1, self.ratio2)

        hbox.addWidget(splitter)
        self.widget.setLayout(hbox)

    def setupCheckBoxPanel(self):
        hbox = QHBoxLayout(self.panelcheck)
        hbox.setAlignment(Qt.AlignHCenter)

        # dual mode
        dualbox = QRadioButton("Dual mode")
        dualbox.setObjectName(self.mode_battle)
        dualbox.toggled.connect(lambda: self.radioBtnFunction())

        # ai battle mode
        aibox = QRadioButton("AI Battle mode")
        aibox.setObjectName(self.mode_ai)
        aibox.toggled.connect(lambda: self.radioBtnFunction())

        hbox.addWidget(dualbox)
        hbox.addWidget(aibox)
        self.panelcheck.setLayout(hbox)

    def radioBtnFunction(self):
        # only working for checkbox that is selected
        if self.sender().isChecked():
            self.resetGridPanel()
            self.setupGridPanel()
            self.current_mode = self.sender().objectName()

            if self.sender().objectName() == self.mode_ai:
                self.setAImode()

    def resetGridPanel(self):
        if self.gridLayout is not None:
            while self.gridLayout.count():
                item = self.gridLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        self.current_player = self.player_one

    # ai mode doesn't need to click
    # enable == false
    def setAImode(self):
        for btn in self.btnList:
            btn.setEnabled(False)

    def setupGridPanel(self):
        if self.gridLayout is None:
            self.gridLayout = QGridLayout(self.panelgrid)
        width, height, = self.autoCalculateSizeForEach()
        self.btnList = [QToolButton(self.panelgrid) for _ in range(self.gridHeight) for _ in range(self.gridWidth)]

        for row in range(self.gridHeight):
            for col in range(self.gridWidth):
                btn = self.btnList[row * self.gridWidth + col]
                btn.setText("")
                btn.setIconSize(QSize(width, height))
                btn.setObjectName("" + str(row) + "-" + str(col))
                btn.clicked.connect(lambda: self.pushBtnFunction())
                self.gridLayout.addWidget(btn, row, col, 1, 1)


    def pushBtnFunction(self):
        btn = self.sender()

        row, col = btn.objectName().split('-')
        row, col = int(row), int(col)

        # send msg to backend
        self.actionHandler(row, col)

        if self.current_player == self.player_one:
            btn.setIcon(self.xIcon)
        elif self.current_player == self.player_two:
            btn.setIcon(self.oIcon)

        btn.setEnabled(False)
        self.roleChange()


    def autoCalculateSizeForEach(self):
        w, h = self.panelgrid.width(), self.panelgrid.height()
        w, h = int(w / self.gridWidth), int(h / self.gridHeight)
        w, h = int(w * 0.8), int(h * 0.75)  # leave some white space

        return w, h

    def roleChange(self):
        self.current_player = self.player_one \
        if self.current_player == self.player_two else self.player_two

    def clickBtn(self, rowIndex, colIndex):
        btn = self.btnList[rowIndex * self.gridWidth + colIndex]
        btn.click()

    def setbtnInAImode(self, rowIndex, colIndex):
        btn = self.btnList[rowIndex * self.gridWidth + colIndex]
        if self.current_player == self.player_one:
            btn.setIcon(self.xIcon)
        elif self.current_player == self.player_two:
            btn.setIcon(self.oIcon)
        self.roleChange()

    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        # basic variable, layout related
        self.width = 800
        self.height = 800
        self.ratio1 = 1
        self.ratio2 = 22

        # define game mode
        self.mode_ai = "aiMode"
        self.mode_battle = "battleMode"
        self.current_mode = None

        # define player role
        self.player_one = "X"
        self.player_two = "O"
        self.current_player = self.player_one

        # two kinds of icon, the key to make a fancy GUI!
        self.xIcon = QIcon(os.path.join("Icons", "x.png"))
        self.oIcon = QIcon(os.path.join("Icons", "o.png"))

        # two working panels
        self.panelcheck = None
        self.panelgrid = None
        self.gridLayout = None

        # button list, can access all buttons here
        self.btnList = []

        self.gridWidth = width
        self.gridHeight = height
        self.widget = QWidget()
        self.setupGUI()

    ### APIs that would interact with backend
    def move(self, rowIndex, colIndex):
        if self.current_mode == self.mode_ai:
            self.setbtnInAImode(rowIndex, colIndex)
        elif self.current_mode == self.mode_battle:
            self.clickBtn(rowIndex, colIndex)

    def notify(self):
        # send out current mode
        return

    def actionHandler(self, row, col):
        # send out user's move
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = mainBoard(8, 8)
    board.show()

    sys.exit(app.exec_())
