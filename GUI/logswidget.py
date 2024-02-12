
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSpinBox,
    QAbstractSpinBox)

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor
from main import MainApp    # Parent
import sys


class LogsWidget(QWidget):
    def __init__(self, parent:MainApp = None):
        super().__init__(parent=parent)

        # Main Layout
        self.mainGridLayout = QGridLayout(self)

        # Logs List
        self.logsListWidget = QListWidget(parent=self)

        # Row Label Section
        self.rowLabel = QLabel(parent=self, text="Current Row: ")
        self.rowSpin = QSpinBox(parent=self)

        # Stop Button
        self.stopButton = QPushButton(parent=self, text="Stop")

        # Setup
        self.setupUi()

    def setupUi(self):
        self.mainGridLayout.setColumnStretch(2, 5)
        self.mainGridLayout.setColumnStretch(3, 2)

        # Logs List
        self.mainGridLayout.addWidget(self.logsListWidget, 0, 0, 1, 4)
        
        # Current Row Section
        self.rowSpin.setMinimumSize(QSize(0, 25))
        self.rowSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rowSpin.setReadOnly(True)
        self.rowSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.rowSpin.setMinimum(1)
        self.rowSpin.setMaximum(100000)
        self.mainGridLayout.addWidget(self.rowLabel, 2, 0, 1, 1)
        self.mainGridLayout.addWidget(self.rowSpin, 2, 1, 1, 1)
        
        # Stop Button
        self.stopButton.setMinimumSize(QSize(0, 30))
        self.mainGridLayout.addWidget(self.stopButton, 2, 3, 1, 1)


    def addLog(self, log: str, color: str = ""):
        item = QListWidgetItem(parent=self.logsListWidget)
        item.setText(log)
        item.setForeground(QColor(color))
        self.logsListWidget.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LogsWidget()
    window.addLog("Error!", "red")
    window.addLog("Done Bro", "green")
    window.show()

    app.exec()
