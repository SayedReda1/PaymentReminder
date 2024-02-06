"""
Name:           Data Fetcher
Purpose:        A script to fetch requested data from google spreadsheet
Author:         Sayed Reda
Last edited:    4/6/2024
"""

import datetime
import time
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class ReminderMessage:
    """
        A class representing each message or reminder
    """
    def __init__(self, student, course: str, startDate: str, endDate: str, phone: str):
        self.student = student
        self.course = course
        self.startDate = startDate
        self.endDate = endDate
        self.phone = phone
    
    def value(self) -> str:
        return f"""Assalamu Alaikum
We'd like to remind you that *{self.student}'s* current course  ended Alhamdulilah and we're begining the next one for *{datetime.date.today().strftime("%B")}*
_New course details:_
*Student: * {self.student}
*Course:* {self.course}
*Start Date:* {self.startDate}
*End Date: * {self.endDate}
        """

    def sendMessage(self) -> None:
        pass


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


def fetchData(spreadsheeturl: str, wsheetName: str) -> list[ReminderMessage]:
    global SCOPES

    # Opening worksheet with given scopes
    print("Opening spread sheet...")
    ssheet = openSpreadSheet(spreadsheeturl, SCOPES)
    wsheet = ssheet.worksheet(wsheetName)

    # Fetching data
    print("Fetching data...")
    data: list[ReminderMessage] = list()

    for row in range(2, wsheet.row_count):
        try:
            startDate = wsheet.cell(row, 10).value
            if startDate is not None and isToday(startDate):
                name, course, endDate, phone = (
                    wsheet.cell(row, 1).value, wsheet.cell(row, 3).value,
                    wsheet.cell(row, 11).value, wsheet.cell(row, 13).value)
                data.append(ReminderMessage(name, course, startDate, endDate, phone))

        # Handling going out of Quota
        except gspread.exceptions.APIError:
            print("Exceeded Quota :), freezing for 60 sec...")
            time.sleep(60)
    
    # Return
    return data


if __name__ == "__main__":
    data = fetchData("https://docs.google.com/spreadsheets/d/1jQuoxYS6utICkmwbWg3e-pu7y8-i7cDu-9_sbAzmBx0/", "Sheet1")
    for message in data:
        print(message.value())
        print("*"*50)