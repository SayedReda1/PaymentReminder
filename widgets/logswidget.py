
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QFont
import time
import sys


class LogsWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)

        self.m_parent = parent

        # Main Layout
        self.mainLayout = QVBoxLayout(self)

        # Upper Row Section
        self.topLayout = QHBoxLayout()
        self.rowLabel = QLabel(parent=self, text="Row: ")
        self.rowSpin = QSpinBox(parent=self)

        # Logs List
        self.logsListWidget = QListWidget(parent=self)

        # Lower Buttons Section
        self.bottomLayout = QHBoxLayout()
        self.backButton = QPushButton(parent=self, text="Back")
        self.pauseButton = QPushButton(parent=self, text="Resume")
        self.endButton = QPushButton(parent=self, text="End")

        # Setup
        self.setupUi()

    def setupUi(self):

        # Upper Row Section
        self.topLayout.addWidget(self.rowLabel)
        self.rowSpin.setStyleSheet("background-color: transparent;")
        self.rowSpin.setFrame(False)
        self.rowSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rowSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.rowSpin.setReadOnly(True)
        self.rowSpin.setRange(1, 100000)
        self.topLayout.addWidget(self.rowSpin)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.topLayout.addItem(spacerItem)
        self.mainLayout.addLayout(self.topLayout)

        # List Widget Section
        self.mainLayout.addWidget(self.logsListWidget)

        # Bottom Buttons Section
        self.bottomLayout.addWidget(self.backButton)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.bottomLayout.addItem(spacerItem2)
        self.bottomLayout.addWidget(self.pauseButton)
        self.bottomLayout.addWidget(self.endButton)
        self.mainLayout.addLayout(self.bottomLayout)

        ######## SLOTS ########
        # self.backButton.clicked.connect()
        # self.pauseButton.clicked.connect()
        # self.endButton.clicked.connect()

    def addLog(self, log: str, color: str = ""):
        item = QListWidgetItem(parent=self.logsListWidget)
        item.setText(log)
        if color:
            item.setForeground(QColor(color))
        self.logsListWidget.addItem(item)

    def setRow(self, rowIndex:int):
        self.rowSpin.setValue(rowIndex)

    def reset(self):
        self.logsListWidget.clear()
        self.rowSpin.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LogsWidget()
    window.addLog("Error!", "red")
    window.addLog("Done Bro", "green")
    window.show()

    app.exec()
