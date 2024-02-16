
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor
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
        self.status_control_button = QPushButton(parent=self, text="Resume")

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
        self.status_control_button.setCheckable(True)
        self.bottomLayout.addWidget(self.status_control_button)
        self.mainLayout.addLayout(self.bottomLayout)

        # -------- SLOTS --------
        self.backButton.clicked.connect(lambda: self.m_parent.switchWidget(0))
        # self.status_control_button.clicked.connect()
        # self.endButton.clicked.connect()


    def start(self):
        self.backButton.setDisabled(True)
        self.status_control_button.setText("Pause")
        self.status_control_button.setChecked(True)       # True if working, False otherwise
        self.reset()

    def end(self):
        self.backButton.setDisabled(False)
        self.status_control_button.setText("Resume")
        self.status_control_button.setChecked(False)

    def addLog(self, log: str, color: str = ""):
        item = QListWidgetItem(parent=self.logsListWidget)
        item.setText(log)

        if color:
            item.setForeground(QColor(color))
        self.logsListWidget.addItem(item)

    def updateRow(self, rowIndex: int):
        self.rowSpin.setValue(rowIndex)

    def reset(self):
        self.logsListWidget.clear()
        self.rowSpin.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    window = LogsWidget()
    window.addLog("Error!", "#ED7D31")
    window.addLog("Done Bro", "green")

    name = "Sayed"
    window.addLog(f"[45]: {name} -> I'm writing anything just to test it out", "orange")
    window.addLog("Done Bro", "green")
    window.show()

    app.exec()
