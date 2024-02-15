from widgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject, QThread
import whatsapp
from data_fetcher import fetchMessage
import sqlite3
import datetime
import time


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
		self.centralStackedWidget.setCurrentIndex(0)

		# Status Bar
		self.statusbar = QStatusBar(parent=self)

		############# Worker Settings #############
		self.workerThread = QThread()
		self.worker = MainWorker()

		self.setupUi()

	def setupUi(self):
		# MainWindow
		self.setWindowIcon(QIcon(":/icons/icon.ico"))
		self.setWindowTitle("Payment Reminder")

		# Central stacked widget
		self.setCentralWidget(self.centralStackedWidget)

		# Setting status bar
		self.setStatusBar(self.statusbar)

		############ Worker ###############
		self.worker.moveToThread(self.workerThread)
		self.worker.add_log_request.connect(self.logs.addLog)
		self.worker.switch_widget_request.connect(self.switchWidget)
		self.worker.logs_row_change_request.connect(self.logs.changeRow)
		self.worker.database_error_raised.connect(
			lambda: QMessageBox.critical(self, "Database Error", 
								"'settings.db', is deleted or corrupted\nReturn to settings in Home and reconfigure")
		)

	def startWorker(self, worksheet:gspread.worksheet):
		# Home Window will start this window
		self.worker.run(worksheet)

	def switchWidget(self, i):
		self.centralStackedWidget.setCurrentIndex(i)

	def updateStatus(self, status: str, msecs:int = -1):
		if (msecs == -1):
			self.statusbar.showMessage(status)
		else:
			self.statusbar.showMessage(status, msecs)


# Worker Class for Worker Thread
class MainWorker(QObject):
	# Signals
	finished = PYQT_SIGNAL()
	switch_widget_request = PYQT_SIGNAL(int)
	add_log_request = PYQT_SIGNAL(str, str)
	logs_row_change_request = PYQT_SIGNAL(int)
	database_error_raised = PYQT_SIGNAL()

	def run(self, worksheet:gspread.worksheet):
		try:
			self.switch_widget_request.emit(1)

			# Fetching data from database
			self.add_log_request.emit("Fetching data from database...", "")
			data = self.fetchData()
			if not data:
				return

			# WA Sender
			self.add_log_request.emit("Opening WhatsApp sender....", "")
			self.sender = whatsapp.WASession()

			# Configure range
			if data["range"] == [1, 1]:
				rows = range(1, worksheet.row_count+1)
			else:
				rows = range(data["range"][0], data["range"][1])

			# Start working
			self.add_log_request.emit("Starting to search...", "")
			for row in rows:
				try:
					self.logs_row_change_request.emit(row)
					
					# Fetch message
					message = fetchMessage(worksheet, row, data["cols"][:5])

					if isToday(message.startDate):
						# Sending the message
						message.send(self.sender, data["message_format"])
						# Mark as sent
						worksheet.update_cell(row, data["cols"][5], "Sent course details!")
						self.logs.addLog(f"Send reminder to {message.student}", "green")

				# API Exhaustion
				except gspread.exceptions.APIError as error:
					# Only handle server exhaustion, otherwise raise
					if error.response.status_code == 429:
						self.add_log_request.emit("Server requests exhaustion, waiting for 70 secs...")
						time.sleep(70)
						self.add_log_request.emit("Continued ^_^")

					else:
						raise error
				# WhatsApp Sender exceptions
				except (whatsapp.exceptions.NoGroupsFound, whatsapp.exceptions.ContactNotFound) as exception:
					worksheet.update_cell(row, data["cols"][5], exception.__str__())
					self.add_log_request.emit(f"[{row}]: {message.student} -> {exception.__str__()}", "yellow")

			# Done without errors
			self.add_log_request.emit("Done", "green")

		# Cannot open WhatsApp
		except whatsapp.exceptions.InvalidWhatsAppLogin:
			# Cannot login to whatsapp
			self.add_log_request.emit("Couldn't login to WhatsApp", "red")

		# Input errors
		except gspread.exceptions.GSpreadException as error:
			# print error
			self.add_log_request.emit(error.__str__(), "red")

		finally:
			self.add_log_request.emit("Ending...")
			self.sender.quit()
			self.finished.emit()


	def fetchData(self):
		try:
			connection = sqlite3.connect("config/settings.db")
			cursor = connection.cursor()

			data: dict = dict()

			# Columns
			cursor.execute("SELECT * FROM Column")
			rows = cursor.fetchall()
			# student, course, startDate, endDate, phone, bot
			cols = list()
			for row in rows:
				cols.append(row[1])
			data["cols"] = cols

			# Range
			cursor.execute("SELECT * FROM Range")
			row1 = cursor.fetchall()[0]

			data["range"] = [row1[1], row1[2]]

			# Message Format
			cursor.execute("SELECT * FROM MessageFormat")
			row1 = cursor.fetchall()[0]

			data["message_format"] = row1[1]

			# Close connect
			connection.close()

			return data

		except sqlite3.Error:
			connection.close()
			self.database_error_raised.emit()
			return None


def isToday(date_str: str):
	"""
		Checks if the given date string in "DD/MM/YYYY" format is today.

		Input:      date string
		Output:     True if the date is today, False otherwise
	"""
	try:
		# Parse the date string
		date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()  # Use .date() to extract the date part

		# Get today's date
		today = datetime.date.today()

		# Check if the dates are equal
		return date_obj == today

	except ValueError:
		# Invalid date format
		return False


if __name__ == "__main__":
	app = QApplication([])

	main = MainApp()
	main.show()

	app.exec()
