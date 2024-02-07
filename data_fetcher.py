"""
Name:           Data Fetcher
Purpose:        A script to fetch requested data from google spreadsheet
Author:         Sayed Reda
Last edited:    7/2/2024
"""

import time
import datetime
import gspread
import whatsapp
from google.oauth2.service_account import Credentials

# Spreadsheet opening scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# Cols numbers for each property
studentCol, courseCol, startDateCol, endDateCol, phoneCol = 1, 3, 10, 11, 13

class ReminderMessage:
    """
        A class representing each message or reminder

        Input:      studentName, course, startDate, endDate, phoneNumber
        Output:     ReminderMessage object
    """
    def __init__(self, student, course: str, startDate: str, endDate: str, phone: str):
        self.student = student
        self.course = course
        self.startDate = startDate
        self.endDate = endDate
        self.phone = phone
    
    def value(self) -> str:
        """
            Returns the message value to be sent
        """
        return f"""Assalamu Alaikum
We'd like to remind you that *{self.student}'s* current course  ended Alhamdulilah and we're begining the next one for *{datetime.date.today().strftime("%B")}*

_*New course details:*_
*Student:* {self.student}
*Course:* {self.course}
*Start Date:* {self.startDate}
*End Date:* {self.endDate}
        """

    def send(self, sender: whatsapp.WASession) -> None:
        sender.sendGroupMessage(self.phone, self.value())


def openSpreadSheet(url: str, scopes: list[str]) -> gspread.spreadsheet:
    """
        Opens a spreadsheet of the given link and return the object
    """
    # Authentication
    creds = Credentials.from_service_account_file("account-credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    
    # Opening spreadsheet
    ssheet = client.open_by_url(url)
    return ssheet


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


def fetchData(spreadsheeturl: str, wsheetName: str, range: range) -> list[ReminderMessage]:
    """
        Fetches the students data from given sheet 
        which their course start date is today

        Input:      spreadsheet URL, worksheet name, range of rows
        Output:     Array of ReminderMessage objects ready to be sent
    """
    global SCOPES, studentCol, courseCol, startDateCol, endDateCol, phoneCol

    # Opening spreadsheet
    print("Opening spread sheet...")
    ssheet = openSpreadSheet(spreadsheeturl, SCOPES)

    # Opening worksheet
    print(f"Opening {wsheetName} worksheet...")
    wsheet = ssheet.worksheet(wsheetName)

    # Fetching data
    print("Fetching data...")
    data: list[ReminderMessage] = list()

    for row in range:
        checked = False

        # Try until current value is checked out
        while not checked:
            try:
                startDate = wsheet.cell(row, startDateCol).value
                if startDate is not None and isToday(startDate):
                    name, course, endDate, phone = (
                        wsheet.cell(row, studentCol).value, wsheet.cell(row, courseCol).value,
                        wsheet.cell(row, endDateCol).value, wsheet.cell(row, phoneCol).value)
                    data.append(ReminderMessage(name, course, startDate, endDate, phone))
                
                # Mark as done
                checked = True

            # Handling Quota exceed
            except gspread.exceptions.APIError as error:
                    if error.args[0]["code"] == 429:
                        print("Quota exceeded, waiting for a min...")
                        time.sleep(60)
                    else:
                        raise error
    
    # Return
    return data


if __name__ == "__main__":
    # Handle everything here...
    try:
        data = fetchData("https://docs.google.com/spreadsheets/d/1jQuoxYS6utICkmwbWg3e-pu7y8-i7cDu-9_sbAzmBx0/",
                          "Sheet1", range(2, 58))
        for message in data:
            print(message.value())
            print("*"*50)

    # Credentials not found
    except FileNotFoundError:
        print("App credentials not found")
    
    # Invalid spreadsheet url
    except gspread.exceptions.SpreadsheetNotFound:
        print("Invalid URL")

    # Invalid Worksheet Name
    except gspread.exceptions.WorksheetNotFound:
        print("Invalid worksheet name")

    # Invalid col or row num
    except gspread.exceptions.APIError as error:
        print("Invalid row or column input")
        print(f"Message: {error.args[0]['message']}")

    # Otherwise
    except:
        print("Unexpected error")