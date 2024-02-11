from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QStatusBar
from PyQt6.QtGui import QIcon
import resources_rc

class MainWindow(QMainWindow):
    def __init__(self, parent:QMainWindow = None):
        super().__init__(parent)

        # Central widget
        self.centralStackedWidget = QStackedWidget(parent=self)

        # Status Bar
        self.statusbar = QStatusBar(parent=self)

        self.setupUi()
        
    def setupUi(self):
        # MainWindow
        self.setWindowIcon(QIcon(":/icons/icon.ico"))
        self.setWindowTitle("Payment Reminder")

        # Central stacked widget
        self.setCentralWidget(self.centralStackedWidget)

        # Setting status bar
        self.setStatusBar(self.statusbar)


if __name__ == "__main__":
    app = QApplication([])

    main = MainWindow()
    main.show()

    app.exec()
