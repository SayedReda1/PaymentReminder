from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, QRect, Qt
import sys
import resources_rc

class SettingsDialog(QDialog):
	def __init__(self, parent:QWidget=None):
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

		self.studentLabel = QLabel(parent=self.colsBox)
		self.studentColSpin = QSpinBox(parent=self.colsBox)

		self.startDateLabel = QLabel(parent=self.colsBox)
		self.startDateColSpin = QSpinBox(parent=self.colsBox)

		self.endDateLabel = QLabel(parent=self.colsBox)
		self.endDateColSpin = QSpinBox(parent=self.colsBox)

		self.courseLabel = QLabel(parent=self.colsBox)
		self.courseColSpin = QSpinBox(parent=self.colsBox)

		self.phoneLabel = QLabel(parent=self.colsBox)
		self.phoneColSpin = QSpinBox(parent=self.colsBox)

		self.botLabel = QLabel(parent=self.colsBox)
		self.botColSpin = QSpinBox(parent=self.colsBox)

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
		self.settingsButtonsLayout = QHBoxLayout()
		self.restoreDefaultsButton = QPushButton(parent=self.scrollAreaWidgetContents)

		# Dialog buttons
		self.buttonBox = QDialogButtonBox(parent=self)


		# Modifiers
		self.setupUi()
		self.restoreDefaults()

	def setupUi(self):
		# ------ Main
		self.setWindowTitle("Settings")
		self.setWindowIcon(QIcon(":\icons\settings-dark.png"))
		self.resize(500, 300)

		# ------ Scroll Area
		self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
		self.scrollArea.setFrameShadow(QFrame.Shadow.Sunken)
		self.scrollArea.setWidgetResizable(True)
		self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 491, 454))
		self.scrollAreaWidgetContents.setStyleSheet("QWidget {\n"
	"    background-color: None;\n"
	"}")
		self.mainLayout.addWidget(self.scrollArea)
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		
		# ------ Columns Group Box
		self.colsBox.setMinimumSize(QSize(0, 130))
		self.colsBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
		self.colsBox.setFlat(True)
		self.colsBox.setTitle("Columns")
		self.contentsLayout.addWidget(self.colsBox)

		# Student
		self.studentLabel.setText("Student")
		self.studentColSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.studentColSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
		self.studentColSpin.setMinimum(1)
		self.studentColSpin.setMaximum(100000)
		self.colsLayout.addWidget(self.studentLabel, 1, 0, 1, 1)
		self.colsLayout.addWidget(self.studentColSpin, 2, 0, 1, 1)
		
		# Start Date
		self.startDateLabel.setText("Start date")
		self.startDateColSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.startDateColSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
		self.startDateColSpin.setMinimum(1)
		self.startDateColSpin.setMaximum(100000)
		self.colsLayout.addWidget(self.startDateLabel, 1, 4, 1, 1)
		self.colsLayout.addWidget(self.startDateColSpin, 2, 4, 1, 1)

		# End Date
		self.endDateLabel.setText("End date")
		self.endDateColSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.endDateColSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
		self.endDateColSpin.setMinimum(1)
		self.endDateColSpin.setMaximum(100000)
		self.colsLayout.addWidget(self.endDateLabel, 1, 5, 1, 1)
		self.colsLayout.addWidget(self.endDateColSpin, 2, 5, 1, 1)

		# Course
		self.courseLabel.setText("Course")
		self.courseColSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.courseColSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
		self.courseColSpin.setMinimum(1)
		self.courseColSpin.setMaximum(100000)
		self.colsLayout.addWidget(self.courseLabel, 3, 0, 1, 1)
		self.colsLayout.addWidget(self.courseColSpin, 4, 0, 1, 1)

		# Phone
		self.phoneLabel.setText("Phone number")
		self.phoneColSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.phoneColSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
		self.phoneColSpin.setMinimum(1)
		self.phoneColSpin.setMaximum(100000)
		self.colsLayout.addWidget(self.phoneLabel, 3, 4, 1, 1)
		self.colsLayout.addWidget(self.phoneColSpin, 4, 4, 1, 1)

		# Bot notes
		self.botLabel.setText("Bot notes")
		self.botColSpin.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.botColSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
		self.botColSpin.setMinimum(1)
		self.botColSpin.setMaximum(100000)
		self.colsLayout.addWidget(self.botColSpin, 4, 5, 1, 1)
		self.colsLayout.addWidget(self.botLabel, 3, 5, 1, 1)


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
		self.settingsButtonsLayout.setStretch(0, 1)
		self.settingsButtonsLayout.setStretch(1, 8)
		self.contentsLayout.addLayout(self.settingsButtonsLayout)

		# Defaults button
		self.restoreDefaultsButton.setText("Restore defaults")
		icon = QIcon()
		icon.addPixmap(QPixmap(":/icons/restart-white.png"), QIcon.Mode.Normal, QIcon.State.Off)
		self.restoreDefaultsButton.setIcon(icon)
		self.restoreDefaultsButton.setIconSize(QSize(20, 20))
		self.restoreDefaultsButton.setToolTip("Restore default settings")
		self.settingsButtonsLayout.addWidget(self.restoreDefaultsButton)

		# Spacer
		spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.settingsButtonsLayout.addItem(spacerItem)

		# ------ Dialog Buttons
		self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
		self.mainLayout.addWidget(self.buttonBox)


		######## SIGNALS #########
		self.buttonBox.accepted.connect(self.saveData)
		self.buttonBox.rejected.connect(self.reject)
		self.restoreDefaultsButton.clicked.connect(self.restoreDefaults)

	def saveData(self):
		self.accept()

	def restoreDefaults(self):
		QApplication.beep()
		
		# Columns
		self.studentColSpin.setValue(1)
		self.courseColSpin.setValue(3)
		self.startDateColSpin.setValue(10)
		self.endDateColSpin.setValue(11)
		self.phoneColSpin.setValue(13)
		self.botColSpin.setValue(15)
		
		# Range (check all)
		self.rangeStartSpin.setValue(1)
		self.rangeEndSpin.setValue(1)
		
		# Message format
		self.messagePlainText.setPlainText("Assalamu Alaikum\n"
											"We'd like to remind you that *{student}*'s current course ended, alhamdulilah, and we're begining the next one for *{month}*.\n"
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
