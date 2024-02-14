from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import QSize
from data_fetcher import gspread, openSpreadSheet
from settingsdialog import SettingsDialog
import resources_rc
import sys


class HomeWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        # Saving parent reference
        self.m_parent = parent

        # Main widget
        self.mainLayout = QVBoxLayout(self)

        # Header widgets
        self.headerLayout = QHBoxLayout()
        self.mainIcon = QLabel(parent=self)
        self.mainLabel = QLabel(parent=self)
        self.settingsButton = QPushButton(parent=self)

        # Middle body widgets
        self.middleBodyFrame = QFrame(parent=self)
        self.bodyLayout = QVBoxLayout(self.middleBodyFrame)
        self.spreadsheetLabel = QLabel(parent=self.middleBodyFrame)
        self.spreadsheetLine = QLineEdit(parent=self.middleBodyFrame)
        self.worksheetLabel = QLabel(parent=self.middleBodyFrame)
        self.worksheetLine = QLineEdit(parent=self.middleBodyFrame)

        # Control buttons widgets
        self.horizontalLayout = QHBoxLayout()
        self.copyMail = QPushButton(parent=self)
        self.beginButton = QPushButton(parent=self)

        self.setupUi()

    def setupUi(self):
        # ------- Main widget
        self.mainLayout.setContentsMargins(20, 15, 20, 15)

        # ------- Header widgets
        # Icon
        self.mainIcon.setMinimumSize(QSize(50, 50))
        self.mainIcon.setMaximumSize(QSize(50, 50))
        self.mainIcon.setPixmap(QPixmap(":/icons/icon.ico"))
        self.mainIcon.setScaledContents(True)
        self.headerLayout.addWidget(self.mainIcon)

        # Header Label
        self.mainLabel.setText("Payment Reminder")
        font = QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(14)
        self.mainLabel.setFont(font)
        self.headerLayout.addWidget(self.mainLabel)

        # Header horizontal spacer
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.headerLayout.addItem(spacerItem)

        # Settings button
        self.settingsButton.setMinimumSize(QSize(30, 30))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/settings-white.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.settingsButton.setIcon(icon)
        self.settingsButton.setIconSize(QSize(20, 20))
        self.settingsButton.setToolTip("Open settings")
        self.headerLayout.addWidget(self.settingsButton)

        # Adding header layout
        self.mainLayout.addLayout(self.headerLayout)


        # ------- Middle Body Widgets
        # Middle body frame
        self.middleBodyFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.middleBodyFrame.setFrameShadow(QFrame.Shadow.Raised)

        # Middle body vertical layout
        self.bodyLayout.setContentsMargins(0, -1, 0, -1)

        # Spacer 1
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.bodyLayout.addItem(spacerItem1)

        # Spread Sheet Label
        self.spreadsheetLabel.setText("Spread Sheet")
        font = QFont()
        font.setPointSize(8)
        self.spreadsheetLabel.setFont(font)
        self.bodyLayout.addWidget(self.spreadsheetLabel)

        # Spread Sheet LineEdit
        self.spreadsheetLine.setPlaceholderText("Enter your Google Sheets URL")
        self.bodyLayout.addWidget(self.spreadsheetLine)

        # Spacer 2
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.bodyLayout.addItem(spacerItem2)

        # Work Sheet Label
        self.worksheetLabel.setText("Work Sheet")
        self.worksheetLabel.setFont(font)
        self.bodyLayout.addWidget(self.worksheetLabel)

        # Work Sheet LineEdit
        self.worksheetLine.setPlaceholderText("Enter your Work Sheet name")
        self.bodyLayout.addWidget(self.worksheetLine)

        # Spacer 3
        spacerItem3 = QSpacerItem(478, 23, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.bodyLayout.addItem(spacerItem3)

        # Adding middle body frame to main
        self.mainLayout.addWidget(self.middleBodyFrame)


        # ------ Control buttons layout
        # Copy Mail Button
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/icons/copy-white.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.copyMail.setIcon(icon1)
        self.copyMail.setIconSize(QSize(20, 20))
        self.copyMail.setToolTip("Copy mail to add in the spreadsheet")
        self.horizontalLayout.addWidget(self.copyMail)

        # middle spacer
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)

        # Begin button
        self.beginButton.setText("Begin")
        self.horizontalLayout.addWidget(self.beginButton)

        # Layout settings
        self.horizontalLayout.setStretch(1, 8)
        self.horizontalLayout.setStretch(2, 4)
        self.mainLayout.addLayout(self.horizontalLayout)

        ############ SIGNALS #############
        self.settingsButton.clicked.connect(self.onSettingsButton)
        self.beginButton.clicked.connect(self.onBeginButton)
        self.copyMail.clicked.connect(self.onCopyMail)


    ########## SLOTS #########
    def onSettingsButton(self):
        # Start settings window
        dialog = SettingsDialog(self)
        dialog.exec()

    def onBeginButton(self):
        self.beginButton.setDisabled(True)
        self.m_parent.updateStatus("Loading Spread Sheet...")
        try:
            spreadSheet = openSpreadSheet(self.spreadsheetLine.text(), ["https://www.googleapis.com/auth/spreadsheets"])
            workSheet = spreadSheet.worksheet(self.worksheetLine.text())



        except FileNotFoundError:
            QMessageBox.critical(self, "Credentials Not Found", "Couldn't get credentials\n'account-credentials.json' is missing")
        except gspread.exceptions.SpreadsheetNotFound:
            QMessageBox.critical(self, "Invalid Spread Sheet", "Cannot find Spread Sheet\nCheck out URL")
        except gspread.exceptions.WorksheetNotFound:
            QMessageBox.critical(self, "Invalid Work Sheet", "Work Sheet name is not found in Spread Sheet")
        except Exception as error:
            QMessageBox.critical(self, "Error", error.__str__())

        finally:
            # Enable the button
            self.beginButton.setDisabled(False)
            
        # Clearing message before starting
        self.m_parent.statusbar.clearMessage()

        # Pass worksheet to main begin function
        self.m_parent.run(workSheet)

    def onCopyMail(self):
        QApplication.clipboard().setText("hamelelquran-payment-reminder@hamelelquran-paymentreminder.iam.gserviceaccount.com")
        self.m_parent.updateStatus("Email copied to clipboard!", 1500)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = HomeWidget()
    window.show()

    app.exec()
