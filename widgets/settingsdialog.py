import os
import sqlite3
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import *

DATA_DIR = os.path.abspath('./config')


class SettingsDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        # Main Layout
        self.main_layout = QVBoxLayout(self)

        # Scroll Area
        self.scroll_area = QScrollArea(self)

        # Scroll Area Content Widget
        self.scroll_area_contents_widget = QWidget(self.scroll_area)
        self.contents_widget_layout = QVBoxLayout(self.scroll_area_contents_widget)

        # Columns group box
        self.cols_box = QGroupBox(self.scroll_area_contents_widget)
        self.cols_layout = QGridLayout(self.cols_box)

        # Labels and Spins
        self.cols_labels = [QLabel(self.cols_box) for _ in range(6)]
        self.cols_spins = [QSpinBox(self.cols_box) for _ in range(6)]

        # Range Box
        self.range_box = QGroupBox(self.scroll_area_contents_widget)
        self.range_layout = QHBoxLayout(self.range_box)
        self.range_start_spin = QSpinBox(self.range_box)
        self.arrow_label = QLabel(self.range_box)
        self.range_end_spin = QSpinBox(self.range_box)
        self.range_data = None

        # Message Box
        self.message_box = QGroupBox(self.scroll_area_contents_widget)
        self.message_box_layout = QVBoxLayout(self.message_box)
        self.message_plain_text = QPlainTextEdit(self.message_box)

        # Restore defaults
        self.reset_layout = QHBoxLayout()
        self.reset_button = QPushButton(self.scroll_area_contents_widget)

        # Dialog buttons
        self.button_box = QDialogButtonBox(self)

        # Modifiers
        self.setupUi()

        # Retrieve previous settings from database
        self.retrieveData()

    def setupUi(self):
        # ------ Main
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(":\icons\settings-dark.png"))
        self.resize(500, 250)

        # ------ Scroll Area
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Shadow.Sunken)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_contents_widget.setStyleSheet("QWidget {background-color: None;}")
        self.main_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_area_contents_widget)

        # ------ Columns Group Box
        self.cols_box.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.cols_box.setFlat(True)
        self.cols_box.setTitle("Columns")
        self.contents_widget_layout.addWidget(self.cols_box)

        # Student
        self.cols_labels[0].setText("Student")
        self.cols_spins[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cols_spins[0].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cols_spins[0].setMinimum(1)
        self.cols_spins[0].setMaximum(100000)
        self.cols_layout.addWidget(self.cols_labels[0], 1, 0, 1, 1)
        self.cols_layout.addWidget(self.cols_spins[0], 2, 0, 1, 1)

        # Course
        self.cols_labels[1].setText("Course")
        self.cols_spins[1].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cols_spins[1].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cols_spins[1].setMinimum(1)
        self.cols_spins[1].setMaximum(100000)
        self.cols_layout.addWidget(self.cols_labels[1], 3, 0, 1, 1)
        self.cols_layout.addWidget(self.cols_spins[1], 4, 0, 1, 1)

        # Start Date
        self.cols_labels[2].setText("Start date")
        self.cols_spins[2].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cols_spins[2].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cols_spins[2].setMinimum(1)
        self.cols_spins[2].setMaximum(100000)
        self.cols_layout.addWidget(self.cols_labels[2], 1, 4, 1, 1)
        self.cols_layout.addWidget(self.cols_spins[2], 2, 4, 1, 1)

        # End Date
        self.cols_labels[3].setText("End date")
        self.cols_spins[3].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cols_spins[3].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cols_spins[3].setMinimum(1)
        self.cols_spins[3].setMaximum(100000)
        self.cols_layout.addWidget(self.cols_labels[3], 3, 4, 1, 1)
        self.cols_layout.addWidget(self.cols_spins[3], 4, 4, 1, 1)

        # Phone
        self.cols_labels[4].setText("Phone number")
        self.cols_spins[4].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cols_spins[4].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cols_spins[4].setMinimum(1)
        self.cols_spins[4].setMaximum(100000)
        self.cols_layout.addWidget(self.cols_labels[4], 1, 5, 1, 1)
        self.cols_layout.addWidget(self.cols_spins[4], 2, 5, 1, 1)

        # Bot notes
        self.cols_labels[5].setText("Bot notes")
        self.cols_spins[5].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cols_spins[5].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cols_spins[5].setMinimum(1)
        self.cols_spins[5].setMaximum(100000)
        self.cols_layout.addWidget(self.cols_spins[5], 4, 5, 1, 1)
        self.cols_layout.addWidget(self.cols_labels[5], 3, 5, 1, 1)

        # ------- Range Box
        self.range_box.setTitle("Row range")
        self.range_box.setFlat(True)
        self.range_layout.setSpacing(6)
        self.range_layout.setStretch(0, 3)
        self.range_layout.setStretch(1, 1)
        self.range_layout.setStretch(2, 3)
        self.range_box.setToolTip("Row range to be checked out.\n[1 -> 1] means check the whole sheet.")
        self.contents_widget_layout.addWidget(self.range_box)

        # Range start
        self.range_start_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.range_start_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.range_start_spin.setMinimum(1)
        self.range_start_spin.setMaximum(100000)
        self.range_layout.addWidget(self.range_start_spin)

        # Middle Icon
        self.arrow_label.setPixmap(QPixmap(":/icons/right-arrow.png"))
        self.arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.range_layout.addWidget(self.arrow_label)

        # Range end
        self.range_end_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.range_end_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.range_end_spin.setMinimum(1)
        self.range_end_spin.setMaximum(100000)
        self.range_layout.addWidget(self.range_end_spin)

        # ------ Message Box
        self.message_box.setToolTip("Enter the sent message format with optional 5 entries:\n"
                                    "- {student}:    student name.\n"
                                    "- {course}:     student\'s course of study.\n"
                                    "- {start}:      course start date.\n"
                                    "- {end}:        course end date.\n"
                                    "- {month}:      current month.\n")
        self.message_box.setTitle("Message format")
        self.message_box.setMinimumSize(QSize(0, 200))
        self.message_box.setFlat(True)
        self.message_box_layout.setObjectName("messageBoxLayout")
        self.contents_widget_layout.addWidget(self.message_box)

        # Message PlainText
        self.message_box_layout.addWidget(self.message_plain_text)

        # ----- Settings Buttons
        self.reset_layout.setStretch(0, 1)
        self.reset_layout.setStretch(1, 8)
        self.contents_widget_layout.addLayout(self.reset_layout)

        # Reset button
        self.reset_button.setText("  Reset")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/restart-dark.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.reset_button.setIcon(icon)
        self.reset_button.setIconSize(QSize(16, 16))
        self.reset_button.setToolTip("Restore default settings")
        self.reset_layout.addWidget(self.reset_button)

        # Spacer
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.reset_layout.addItem(spacer_item)

        # ------ Dialog Buttons
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.main_layout.addWidget(self.button_box)

        # ------ SIGNALS -------
        self.button_box.accepted.connect(self.updateData)
        self.button_box.rejected.connect(self.reject)
        self.reset_button.clicked.connect(lambda: self.reset(True))
        self.range_start_spin.editingFinished.connect(self.onSpinValueChange)
        self.range_end_spin.editingFinished.connect(self.onSpinValueChange)

    def updateData(self):
        """
            Updates the database with given updated data on OK button
        """
        global DATA_DIR

        # Return QMessageBox.accepted flag
        self.accept()

        # Connection
        connection = sqlite3.connect(os.path.join(DATA_DIR, 'settings.db'))
        cursor = connection.cursor()

        # Updating Columns
        for i in range(6):
            cursor.execute(
                f"UPDATE Column SET Col = {self.cols_spins[i].value()} WHERE ID={i};")

        # Updating Range
        cursor.execute(
            f"UPDATE Range SET Start = {self.range_start_spin.value()}, End = {self.range_end_spin.value()} WHERE ID=0;")

        # Updating Message Format
        cursor.execute(f"UPDATE MessageFormat SET Format = \"{self.message_plain_text.toPlainText()}\" WHERE ID=0;")

        # Finishing up
        connection.commit()
        connection.close()

    def createData(self):
        """
            Creates the database in case it was deleted from current settings
        """
        global DATA_DIR

        connection = sqlite3.connect(os.path.join(DATA_DIR, 'settings.db'))
        cursor = connection.cursor()

        # Dropping Tables if they exist
        cursor.execute("DROP TABLE IF EXISTS Column;")
        cursor.execute("DROP TABLE IF EXISTS Range;")
        cursor.execute("DROP TABLE IF EXISTS MessageFormat;")

        # Creating new tables
        cursor.execute("CREATE TABLE Column (ID INTEGER, Col INTEGER);")
        cursor.execute("CREATE TABLE Range (ID INTEGER, Start INTEGER, End INTEGER);")
        cursor.execute("CREATE TABLE MessageFormat (ID INTEGER, Format TEXT);")

        # Inserting current data
        # Columns
        for i in range(6):
            cursor.execute(
                f"INSERT INTO Column VALUES ({i}, {self.cols_spins[i].value()});")

        # Range
        cursor.execute(f"INSERT INTO Range VALUES (0, {self.range_start_spin.value()}, {self.range_end_spin.value()});")

        # Message Format
        cursor.execute(f"INSERT INTO MessageFormat VALUES (0, \"{self.message_plain_text.toPlainText()}\");")

        # Committing and closing
        connection.commit()
        connection.close()

    def retrieveData(self):
        """
            Retrieves data from settings.db
        """
        global DATA_DIR

        connection = sqlite3.connect(os.path.join(DATA_DIR, 'settings.db'))
        try:
            cursor = connection.cursor()

            # Retrieving columns
            cursor.execute("SELECT * FROM Column;")
            cols = cursor.fetchall()
            for i, row in cols:
                self.cols_spins[i].setValue(row)

            # Retrieving Range
            cursor.execute("SELECT * FROM Range;")

            # Only one range
            ranges = cursor.fetchall()[0]
            self.range_start_spin.setValue(ranges[1])
            self.range_end_spin.setValue(ranges[2])
            self.range_data = list(ranges[1:])

            # Retrieving Message Format
            cursor.execute("SELECT * FROM MessageFormat;")
            # Only one message format
            msg_format = cursor.fetchall()[0]
            self.message_plain_text.setPlainText(msg_format[1])

        except sqlite3.Error:
            # In case settings.db is deleted, we create a new one with defaults
            self.reset(False)
            self.createData()

        finally:
            connection.close()

    def reset(self, warn):
        # Check if warning is required
        status = True
        if warn:
            status = (QMessageBox.warning(parent=self, title="Reset Settings",
                                          text="Are you sure to reset settings to default?",
                                          buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                      == QMessageBox.StandardButton.Yes)

        # Start to reset
        if status:
            self.cols_spins[0].setValue(1)
            self.cols_spins[1].setValue(3)
            self.cols_spins[2].setValue(10)
            self.cols_spins[3].setValue(11)
            self.cols_spins[4].setValue(13)
            self.cols_spins[5].setValue(15)

            # Range (check all)
            self.range_start_spin.setValue(1)
            self.range_end_spin.setValue(1)
            self.range_data = [1, 1]

            # Message format
            self.message_plain_text.setPlainText("Assalamu Alaikum\n"
                                                 "We'd like to remind you that *{student}*'s current course ended, "
                                                 "alhamdulilah, and we're beginning the next one for *{month}*.\n"
                                                 "\n"
                                                 "_*New course details:*_\n"
                                                 "*Student:* {student}\n"
                                                 "*Course:* {course}\n"
                                                 "*Start Date:* {start}\n"
                                                 "*End Date:* {end}")

    def onSpinValueChange(self):
        if self.range_start_spin.value() > self.range_end_spin.value():
            self.range_start_spin.setValue(self.range_data[0])
            self.range_end_spin.setValue(self.range_data[1])
        else:
            self.range_data[0], self.range_data[1] = (
                self.range_start_spin.value(), self.range_end_spin.value())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = SettingsDialog()
    dialog.show()

    app.exec()
