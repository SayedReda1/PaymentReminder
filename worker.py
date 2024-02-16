from data_fetcher import *
from PyQt6.QtCore import QObject, pyqtSignal
import sqlite3
import datetime
import os
from time import sleep


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


# Worker Class for Worker Thread
class MainWorker(QObject):
    # Signals
    finished = pyqtSignal()
    add_log_request = pyqtSignal(str, str)
    logs_row_change_request = pyqtSignal(int)
    database_error_raised = pyqtSignal()

    # Args
    spreadURL:str = ""
    worksheetName: str = ""

    def run(self):
        try:
        
            # Open spreadsheet and worksheet
            self.add_log_request.emit("Opening Spread Sheet...", "")
            self.spreadsheet = openSpreadSheet(self.spreadURL, ["https://www.googleapis.com/auth/spreadsheets"])
            self.worksheet = self.spreadsheet.worksheet(self.worksheetName)

            # Fetching data from database
            data = self.fetchSettings()
            if not data:
                return

            # WA Sender
            self.add_log_request.emit("Opening WhatsApp....", "")
            self.sender = whatsapp.WASession()

            # Configure range
            if all(x == 1 for x in data['range']):
                row, max = 1, self.worksheet.row_count
            else:
                row, max = data['range'][0], data['range'][1]

            # Start working
            while row <= max:
                try:
                    self.logs_row_change_request.emit(row)
                    
                    # Fetch message
                    message = fetchMessage(self.worksheet, row, data['cols'])

                    if isToday(message.startDate):
                        # Sending the message
                        message.send(self.sender, data['message'])
                        # Mark as sent
                        self.worksheet.update_cell(row, data['bot'], "Sent course details!")
                        self.add_log_request.emit(f"Sent reminder to {message.student}", "green")

                # API Exhaustion
                except gspread.exceptions.APIError as error:
                    # Only handle server exhaustion, otherwise raise
                    if error.response.status_code == 429:
                        self.add_log_request.emit("Server requests exhaustion, waiting for 120 secs...", "")
                        sleep(120)
                        self.add_log_request.emit("Continued ^_^", "")
                        row -= 1
                    else:
                        raise error
                    
                # WhatsApp Sender exceptions
                except (whatsapp.exceptions.NoGroupsFound, whatsapp.exceptions.ContactNotFound) as exception:
                    self.worksheet.update_cell(row, data['bot'], exception.__str__())
                    self.add_log_request.emit(f"{message.student}: {exception.__str__()}", "brown")

                finally:
                    row += 1

            # Done without errors
            self.add_log_request.emit("Done", "green")

        # Cannot open WhatsApp
        except whatsapp.exceptions.InvalidWhatsAppLogin:
            # Cannot log in to whatsapp
            self.add_log_request.emit("Couldn't login to WhatsApp", "red")

        # Input errors
        except gspread.exceptions.GSpreadException as error:
            # print error
            self.add_log_request.emit(error.__str__(), "red")

        finally:
            self.sender.quit()
            self.finished.emit()

    def fetchSettings(self):
        try:
            # Getting path to ./config/settings.db
            dir = os.path.abspath("./config")
            connection = sqlite3.connect(os.path.join(dir, 'settings.db'))
            cursor = connection.cursor()

            # data {
            #   cols:   [5]
            #   range:  [2]
            #   bot:    int
            #   message:str
            # }
            data: dict = dict()

            # Columns
            cursor.execute("SELECT * FROM Column")
            rows = cursor.fetchall()

            # 'Student', 'Course', 'Start date', 'End date', 'Phone number'
            data.update({"bot": rows[5][1]})
            rows.pop()

            data.update({'cols': [col for _, col in rows]})

            # Range
            cursor.execute("SELECT * FROM Range")
            row1 = cursor.fetchall()[0]

            data['range'] = [row1[1], row1[2]]

            # Message Format
            cursor.execute("SELECT * FROM MessageFormat")
            row1 = cursor.fetchall()[0]

            data['message'] = row1[1]

            # Close connect
            connection.close()
            return data

        except sqlite3.Error:
            connection.close()
            self.database_error_raised.emit()
            return None



