"""
Name:           Data Fetcher
Purpose:        A script to open spreadsheets and fetch requested data from them
                and return those data in form of ReminderMessage obj

Author:         Sayed Reda
Last edited:    7/2/2024
"""

import datetime
import gspread
import whatsapp
from google.oauth2.service_account import Credentials


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
    
    def value(self, format:str) -> str:
        """
            Returns the message value to be sent
        """
        return format.format(student=self.student, course=self.course, 
                             startDate=self.startDate, endDate=self.endDate, month=datetime.date.today().strftime("%B"))
    

    def send(self, sender: whatsapp.WASession, format:str) -> None:
        """
            Sends the message [self.value()] to the group using the phone number

            Input:      WASession object
            Output:     None
        """
        sender.sendGroupMessage(self.phone, self.value(format))


def openSpreadSheet(url: str, scopes: list[str]) -> gspread.spreadsheet:
    """
        Opens a spreadsheet of the given link and return the object
    """

    # Authentication
    creds = Credentials.from_service_account_file("config/account-credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    
    # Opening spreadsheet
    spreadsheet = client.open_by_url(url)
    return spreadsheet


def fetchMessage(worksheet: gspread.worksheet, row: int, cols: list[int]) -> ReminderMessage:
    """
        Fetches the student data from given worksheet 
        and return message reminder object

        Input:      worksheet obj, row number, array of 
                    [studentCol, courseCol, startDateCol, endDateCol, phoneCol]
        
        Output:     ReminderMessage object ready to be sent
    """
    
    try:
        rowValues: list[str] = worksheet.row_values(row)
        rowValues.extend([''] * (worksheet.col_count - len(rowValues)))     # in case it's trimed

        msg = ReminderMessage(rowValues[cols[0]-1], rowValues[cols[1]-1], rowValues[cols[2]-1], rowValues[cols[3]-1], 
                               rowValues[cols[4]-1])
        return msg
    
    except gspread.exceptions.APIError as error:
        raise error
    except IndexError:
        raise gspread.exceptions.GSpreadException("one of COLS is invalid or out of range")


if __name__ == "__main__":
    spread = openSpreadSheet("https://docs.google.com/spreadsheets/d/1jQuoxYS6utICkmwbWg3e-pu7y8-i7cDu-9_sbAzmBx0/", 
                            ["https://www.googleapis.com/auth/spreadsheets"])
    worksheet = spread.worksheet("Sheet1")

    print(fetchMessage(worksheet, 43, [1, 3, 10, 11, 13]).value())

