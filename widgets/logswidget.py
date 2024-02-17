import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import *


class LogsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.m_parent = parent

        # Main Layout
        self.main_layout = QVBoxLayout(self)

        # Upper Row Section
        self.top_layout = QHBoxLayout()
        self.row_label = QLabel(parent=self, text="Row: ")
        self.row_spin = QSpinBox(parent=self)

        # Logs List
        self.logs_list_widget = QListWidget(parent=self)

        # Lower Buttons Section
        self.bottom_layout = QHBoxLayout()
        self.back_button = QPushButton(parent=self, text="Back")
        self.status_control_button = QPushButton(parent=self, text="Resume")

        # Setup
        self.setupUi()

    def setupUi(self):
        # Upper Row Section
        self.top_layout.addWidget(self.row_label)
        self.row_spin.setStyleSheet("background-color: transparent;")
        self.row_spin.setFrame(False)
        self.row_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.row_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.row_spin.setReadOnly(True)
        self.row_spin.setRange(1, 100000)
        self.top_layout.addWidget(self.row_spin)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.top_layout.addItem(spacerItem)
        self.main_layout.addLayout(self.top_layout)

        # List Widget Section
        self.main_layout.addWidget(self.logs_list_widget)

        # Bottom Buttons Section
        self.bottom_layout.addWidget(self.back_button)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.bottom_layout.addItem(spacerItem2)
        self.status_control_button.setCheckable(True)
        self.bottom_layout.addWidget(self.status_control_button)
        self.main_layout.addLayout(self.bottom_layout)

        # -------- SLOTS --------
        self.back_button.clicked.connect(lambda: self.m_parent.switchWidget(0))

    def start(self):
        self.back_button.setDisabled(True)
        self.status_control_button.setText("Pause")
        self.status_control_button.setChecked(True)  # True if working, False otherwise
        self.reset()

    def end(self):
        self.back_button.setDisabled(False)
        self.status_control_button.setText("Resume")
        self.status_control_button.setChecked(False)

    def addLog(self, log: str, color: str = ""):
        item = QListWidgetItem(self.logs_list_widget)
        item.setText(log)

        if color:
            item.setForeground(QColor(color))
        self.logs_list_widget.addItem(item)

    def updateRow(self, row_index: int):
        self.row_spin.setValue(row_index)

    def reset(self):
        self.logs_list_widget.clear()
        self.row_spin.clear()


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
