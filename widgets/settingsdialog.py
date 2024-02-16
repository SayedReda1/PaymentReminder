from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, QRect, Qt
import sys
import os
import sqlite3

DATA_DIR = os.path.abspath('./config')


class SettingsDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        # Main Layout
        self.mainLayout = QVBoxLayout(self)

        # Scroll Area
        self.scrollArea = QScrollArea(parent=self)

        # Scroll Area Content Widget
        self.scrollAreaWidgetContents = QWidget()
        self.contentsLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        # Columns group box
        self.colsBox = QGroupBox(parent=self.scrollAreaWidgetContents)
        self.colsLayout = QGridLayout(self.colsBox)

        # Labels and Spins
        self.columnLabels = [QLabel(parent=self.colsBox) for i in range(6)]
        self.columnSpins = [QSpinBox(parent=self.colsBox) for i in range(6)]

        # Range Box
        self.rangeBox = QGroupBox(parent=self.scrollAreaWidgetContents)
        self.rangeBoxLayout = QHBoxLayout(self.rangeBox)
        self.rangeStartSpin = QSpinBox(parent=self.rangeBox)
        self.arrowLabel = QLabel(parent=self.rangeBox)
        self.rangeEndSpin = QSpinBox(parent=self.rangeBox)

        # Message Box
        self.messageBox = QGroupBox(parent=self.scrollAreaWidgetContents)
        self.messageBoxLayout = QVBoxLayout(self.messageBox)
        self.messagePlainText = QPlainTextEdit(parent=self.messageBox)

        # Restore defaults
        self.resetButtonLayout = QHBoxLayout()
        self.resetButton = QPushButton(parent=self.scrollAreaWidgetContents)

        # Dialog buttons
        self.buttonBox = QDialogButtonBox(parent=self)

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
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Sunken)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents.setStyleSheet("QWidget {\n"
                                                    "    background-color: None;\n"
                                                    "}")
        self.mainLayout.addWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # ------ Columns Group Box
        self.colsBox.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.colsBox.setFlat(True)
        self.colsBox.setTitle("Columns")
        self.contentsLayout.addWidget(self.colsBox)

        # Student
        self.columnLabels[0].setText("Student")
        self.columnSpins[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.columnSpins[0].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.columnSpins[0].setMinimum(1)
        self.columnSpins[0].setMaximum(100000)
        self.colsLayout.addWidget(self.columnLabels[0], 1, 0, 1, 1)
        self.colsLayout.addWidget(self.columnSpins[0], 2, 0, 1, 1)

        # Course
        self.columnLabels[1].setText("Course")
        self.columnSpins[1].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.columnSpins[1].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.columnSpins[1].setMinimum(1)
        self.columnSpins[1].setMaximum(100000)
        self.colsLayout.addWidget(self.columnLabels[1], 3, 0, 1, 1)
        self.colsLayout.addWidget(self.columnSpins[1], 4, 0, 1, 1)

        # Start Date
        self.columnLabels[2].setText("Start date")
        self.columnSpins[2].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.columnSpins[2].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.columnSpins[2].setMinimum(1)
        self.columnSpins[2].setMaximum(100000)
        self.colsLayout.addWidget(self.columnLabels[2], 1, 4, 1, 1)
        self.colsLayout.addWidget(self.columnSpins[2], 2, 4, 1, 1)

        # End Date
        self.columnLabels[3].setText("End date")
        self.columnSpins[3].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.columnSpins[3].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.columnSpins[3].setMinimum(1)
        self.columnSpins[3].setMaximum(100000)
        self.colsLayout.addWidget(self.columnLabels[3], 3, 4, 1, 1)
        self.colsLayout.addWidget(self.columnSpins[3], 4, 4, 1, 1)

        # Phone
        self.columnLabels[4].setText("Phone number")
        self.columnSpins[4].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.columnSpins[4].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.columnSpins[4].setMinimum(1)
        self.columnSpins[4].setMaximum(100000)
        self.colsLayout.addWidget(self.columnLabels[4], 1, 5, 1, 1)
        self.colsLayout.addWidget(self.columnSpins[4], 2, 5, 1, 1)

        # Bot notes
        self.columnLabels[5].setText("Bot notes")
        self.columnSpins[5].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.columnSpins[5].setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.columnSpins[5].setMinimum(1)
        self.columnSpins[5].setMaximum(100000)
        self.colsLayout.addWidget(self.columnSpins[5], 4, 5, 1, 1)
        self.colsLayout.addWidget(self.columnLabels[5], 3, 5, 1, 1)

        # ------- Range Box
        self.rangeBox.setTitle("Row range")
        self.rangeBox.setFlat(True)
        self.rangeBoxLayout.setSpacing(6)
        self.rangeBoxLayout.setStretch(0, 3)
        self.rangeBoxLayout.setStretch(1, 1)
        self.rangeBoxLayout.setStretch(2, 3)
        self.rangeBox.setToolTip("Row range to be checked out.\n[1 -> 1] means check the whole sheet.")
        self.contentsLayout.addWidget(self.rangeBox)

        # Range start
        self.rangeStartSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rangeStartSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.rangeStartSpin.setMinimum(1)
        self.rangeStartSpin.setMaximum(100000)
        self.rangeBoxLayout.addWidget(self.rangeStartSpin)

        # Middle Icon
        self.arrowLabel.setPixmap(QPixmap(":/icons/right-arrow.png"))
        self.arrowLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rangeBoxLayout.addWidget(self.arrowLabel)

        # Range end
        self.rangeEndSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rangeEndSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.rangeEndSpin.setMinimum(1)
        self.rangeEndSpin.setMaximum(100000)
        self.rangeBoxLayout.addWidget(self.rangeEndSpin)

        # ------ Message Box
        self.messageBox.setToolTip("Enter the sent message format with optional 5 entries:\n"
                                   "- {student}:	student name.\n"
                                   "- {course}:	student\'s course of study.\n"
                                   "- {startDate}:	course start date.\n"
                                   "- {endDate}:	course end date.\n"
                                   "- {month}:  	current month.\n")
        self.messageBox.setTitle("Message format")
        self.messageBox.setMinimumSize(QSize(0, 200))
        self.messageBox.setFlat(True)
        self.messageBoxLayout.setObjectName("messageBoxLayout")
        self.contentsLayout.addWidget(self.messageBox)

        # Message PlainText
        self.messageBoxLayout.addWidget(self.messagePlainText)

        # ----- Settings Buttons
        self.resetButtonLayout.setStretch(0, 1)
        self.resetButtonLayout.setStretch(1, 8)
        self.contentsLayout.addLayout(self.resetButtonLayout)

        # Reset button
        self.resetButton.setText("  Reset")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/restart-dark.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.resetButton.setIcon(icon)
        self.resetButton.setIconSize(QSize(16, 16))
        self.resetButton.setToolTip("Restore default settings")
        self.resetButtonLayout.addWidget(self.resetButton)

        # Spacer
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.resetButtonLayout.addItem(spacerItem)

        # ------ Dialog Buttons
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.mainLayout.addWidget(self.buttonBox)

        ######## SIGNALS #########
        self.buttonBox.accepted.connect(self.updateData)
        self.buttonBox.rejected.connect(self.reject)
        self.resetButton.clicked.connect(lambda: self.reset(True))

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

        # Updating Coloumns
        for i in range(6):
            cursor.execute(
                f"UPDATE Column SET Col = {self.columnSpins[i].value()} WHERE Field=\"{self.columnLabels[i].text()}\";")

        # Updating Range
        cursor.execute(
            f"UPDATE Range SET Start = {self.rangeStartSpin.value()}, End = {self.rangeEndSpin.value()} WHERE ID=0;")

        # Updating Message Format
        cursor.execute(f"UPDATE MessageFormat SET Format = \"{self.messagePlainText.toPlainText()}\" WHERE ID=0;")

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
        cursor.execute("CREATE TABLE Column (Field TEXT, Col INTEGER);")
        cursor.execute("CREATE TABLE Range (ID INTEGER, Start INTEGER, End INTEGER);")
        cursor.execute("CREATE TABLE MessageFormat (ID INTEGER, Format TEXT);")

        # Inserting current data
        # Columns
        for i in range(6):
            cursor.execute(
                f"INSERT INTO Column VALUES ('{self.columnLabels[i].text()}', {self.columnSpins[i].value()});")

        # Range
        cursor.execute(f"INSERT INTO Range VALUES (0, {self.rangeStartSpin.value()}, {self.rangeEndSpin.value()});")

        # Message Format
        cursor.execute(f"INSERT INTO MessageFormat VALUES (0, \"{self.messagePlainText.toPlainText()}\");")

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
            for i, row in enumerate(cols):
                self.columnSpins[i].setValue(row[1])

            # Retrieving Range
            cursor.execute("SELECT * FROM Range;")

            # Only one range
            ranges = cursor.fetchall()[0]
            self.rangeStartSpin.setValue(ranges[1])
            self.rangeEndSpin.setValue(ranges[2])

            # Retrieving Message Format
            cursor.execute("SELECT * FROM MessageFormat;")
            # Only one message format
            msg_format = cursor.fetchall()[0]
            self.messagePlainText.setPlainText(msg_format[1])

        except sqlite3.Error:
            # In case settings.db is deleted, we create a new one with defaults
            self.reset(False)
            self.createData()

        finally:
            connection.close()

    def reset(self, warn):
        # Columns
        if warn and QMessageBox.warning(self, "Reset Settings", "Are you sure to reset settings to default?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return
        # Warn before editing
        self.columnSpins[0].setValue(1)
        self.columnSpins[1].setValue(3)
        self.columnSpins[2].setValue(10)
        self.columnSpins[3].setValue(11)
        self.columnSpins[4].setValue(13)
        self.columnSpins[5].setValue(15)

        # Range (check all)
        self.rangeStartSpin.setValue(1)
        self.rangeEndSpin.setValue(1)

        # Message format
        self.messagePlainText.setPlainText("Assalamu Alaikum\n"
                                           "We'd like to remind you that *{student}*'s current course ended, "
                                           "alhamdulilah, and we're beginning the next one for *{month}*.\n"
                                           "\n"
                                           "_*New course details:*_\n"
                                           "*Student:* {student}\n"
                                           "*Course:* {course}\n"
                                           "*Start Date:* {startDate}\n"
                                           "*End Date:* {endDate}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = SettingsDialog()
    dialog.show()

    app.exec()
