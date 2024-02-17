from widgets import *
from worker import MainWorker
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread


class MainApp(QMainWindow):
    def __init__(self, parent: QMainWindow = None):
        super().__init__(parent)

        # --------- GUI Settings ----------
        # Central widget
        self.central_stacked_widget = QStackedWidget(parent=self)

        # Home & Logs Widget
        self.home_widget = HomeWidget(self)
        self.logs_widget = LogsWidget(self)

        # Adding widgets
        self.central_stacked_widget.addWidget(self.home_widget)
        self.central_stacked_widget.addWidget(self.logs_widget)

        # Status Bar
        self.statusbar = QStatusBar(parent=self)

        self.setupUi()

    def setupUi(self):
        # MainWindow
        self.switchWidget(0)
        self.setWindowIcon(QIcon(":/icons/icon.ico"))
        self.setWindowTitle("Payment Reminder")

        # Central stacked widget
        self.setCentralWidget(self.central_stacked_widget)

        # Setting status bar
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Developer: Sayed Reda")

    def startWorking(self, spread_url: str, worksheet_name: str):
        # Worker and thread
        self.worker = MainWorker(spread_url, worksheet_name)
        self.thread = QThread()

        # Moving to thread
        self.worker.moveToThread(self.thread)

        # Signals
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.add_log_request.connect(self.logs_widget.addLog)
        self.worker.logs_row_change_request.connect(self.logs_widget.updateRow)
        self.worker.database_error_raised.connect(
            lambda: QMessageBox.critical(self, "Database Error",
                                         "Database file is missing or corrupted\nGo to settings and reconfigure")
        )
        self.thread.start()

        # Others
        self.switchWidget(1)
        self.logs_widget.start()
        self.worker.finished.connect(self.logs_widget.end)
        self.worker.finished.connect(QApplication.beep)

    def switchWidget(self, i):
        self.central_stacked_widget.setCurrentIndex(i)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("fusion")

    main = MainApp()
    main.show()

    app.exec()
