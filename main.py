from widgets import *
from worker import MainWorker
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread


class MainApp(QMainWindow):
    def __init__(self, parent:QMainWindow = None):
        super().__init__(parent)

        ############ GUI Settings ##############
        # Central widget
        self.centralStackedWidget = QStackedWidget(parent=self)

        # Home & Logs Widget
        self.home = HomeWidget(self)
        self.logs = LogsWidget(self)

        # Adding widgets
        self.centralStackedWidget.addWidget(self.home)
        self.centralStackedWidget.addWidget(self.logs)

        # Status Bar
        self.statusbar = QStatusBar(parent=self)

        self.setupUi()

    def setupUi(self):
        # MainWindow
        self.switchWidget(0)
        self.setWindowIcon(QIcon(":/icons/icon.ico"))
        self.setWindowTitle("Payment Reminder")

        # Central stacked widget
        self.setCentralWidget(self.centralStackedWidget)

        # Setting status bar
        self.setStatusBar(self.statusbar)


    def startWorking(self, spreadURL: str, worksheetName: str):
        # Worker and thread
        self.worker = MainWorker()
        self.thread = QThread()
        self.worker.spreadURL = spreadURL
        self.worker.worksheetName = worksheetName

        # Moving to thread
        self.worker.moveToThread(self.thread)

        # Signals
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.add_log_request.connect(self.logs.addLog)
        self.worker.logs_row_change_request.connect(self.logs.updateRow)
        self.worker.database_error_raised.connect(
            lambda: QMessageBox.critical(self, "Database Error", "Database file is missing or corrupted\nGo to settings and reconfigure")
        )
        self.thread.start()

        # Others
        self.switchWidget(1)
        self.logs.start()
        self.thread.finished.connect(self.logs.end)


    def switchWidget(self, i):
        self.centralStackedWidget.setCurrentIndex(i)


    def updateStatus(self, status: str, msecs:int = -1):
        if (msecs == -1):
            self.statusbar.showMessage(status)
        else:
            self.statusbar.showMessage(status, msecs)



if __name__ == "__main__":
    app = QApplication([])

    main = MainApp()
    main.show()

    app.exec()
