from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import QSize
from widgets.settingsdialog import SettingsDialog
from widgets import resources_rc
import sys


class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # -------- GUI Settings ----------
        # Saving parent reference
        self.m_parent = parent

        # Main widget
        self.main_layout = QVBoxLayout(self)

        # Header widgets
        self.top_layout = QHBoxLayout()
        self.main_icon = QLabel(self)
        self.main_label = QLabel(self)
        self.settings_button = QPushButton(self)

        # Middle body widgets
        # self.middleBodyFrame = QFrame(parent=self)
        self.body_layout = QVBoxLayout()
        self.spreadsheet_label = QLabel(self)
        self.spreadsheet_line = QLineEdit(self)
        self.worksheet_label = QLabel(self)
        self.worksheet_line = QLineEdit(self)

        # Control buttons widgets
        self.bottom_layout = QHBoxLayout()
        self.copy_mail_button = QPushButton(self)
        self.begin_button = QPushButton(self)

        self.setupUi()

    def setupUi(self):
        # ------- Main widget
        self.main_layout.setContentsMargins(20, 15, 20, 15)

        # ------- Header widgets
        # Icon
        self.main_icon.setMinimumSize(QSize(40, 40))
        self.main_icon.setMaximumSize(QSize(40, 40))
        self.main_icon.setPixmap(QPixmap(":/icons/icon.ico"))
        self.main_icon.setScaledContents(True)
        self.top_layout.addWidget(self.main_icon)

        # Header Label
        self.main_label.setText("Payment Reminder")
        font = QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(14)
        self.main_label.setFont(font)
        self.top_layout.addWidget(self.main_label)

        # Header horizontal spacer
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.top_layout.addItem(spacer_item)

        # Settings button
        self.settings_button.setMinimumSize(QSize(30, 30))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/settings-dark.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings_button.setIcon(icon)
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.setToolTip("Open settings")
        self.top_layout.addWidget(self.settings_button)

        # Adding header layout
        self.main_layout.addLayout(self.top_layout)

        # ------- Middle Body Widgets
        # Middle body vertical layout
        self.body_layout.setContentsMargins(0, -1, 0, -1)

        # Spacer 1
        spacer_item1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.body_layout.addItem(spacer_item1)

        # Spread Sheet Label
        self.spreadsheet_label.setText("Spread Sheet")
        font = QFont()
        font.setPointSize(8)
        self.spreadsheet_label.setFont(font)
        self.body_layout.addWidget(self.spreadsheet_label)

        # Spread Sheet LineEdit
        self.spreadsheet_line.setPlaceholderText("Enter your Google Sheets URL")
        self.body_layout.addWidget(self.spreadsheet_line)

        # Spacer 2
        spacer_item2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.body_layout.addItem(spacer_item2)

        # Work Sheet Label
        self.worksheet_label.setText("Work Sheet")
        self.worksheet_label.setFont(font)
        self.body_layout.addWidget(self.worksheet_label)

        # Work Sheet LineEdit
        self.worksheet_line.setPlaceholderText("Enter your Work Sheet name")
        self.body_layout.addWidget(self.worksheet_line)

        # Spacer 3
        spacer_item3 = QSpacerItem(478, 23, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.body_layout.addItem(spacer_item3)

        # Adding body layout to main
        self.main_layout.addLayout(self.body_layout)

        # ------ Control buttons layout
        # Copy Mail Button
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/icons/copy-dark.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_mail_button.setIcon(icon1)
        self.copy_mail_button.setIconSize(QSize(20, 20))
        self.copy_mail_button.setToolTip("Copy mail to add in the spreadsheet")
        self.bottom_layout.addWidget(self.copy_mail_button)

        # middle spacer
        spacer_item4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.bottom_layout.addItem(spacer_item4)

        # Begin button
        self.begin_button.setText("Begin")
        self.bottom_layout.addWidget(self.begin_button)

        # Layout settings
        self.bottom_layout.setStretch(1, 8)
        self.bottom_layout.setStretch(2, 4)
        self.main_layout.addLayout(self.bottom_layout)

        # --------- SIGNALS -----------
        self.begin_button.clicked.connect(self.onBeginButton)
        self.settings_button.clicked.connect(
            lambda: SettingsDialog(self).exec()
        )
        self.copy_mail_button.clicked.connect(
            lambda: QApplication.clipboard().setText(
                "hamelelquran-payment-reminder@hamelelquran-paymentreminder.iam.gserviceaccount.com"
            )
        )

    # --------- SLOTS ----------
    def onBeginButton(self):
        self.m_parent.startWorking(self.spreadsheet_line.text(), self.worksheet_line.text())
        self.resetFields()

    def resetFields(self):
        self.spreadsheet_line.clear()
        self.worksheet_line.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = HomeWidget()
    window.show()

    app.exec()
