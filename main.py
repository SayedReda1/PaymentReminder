"""
Name:           main
Purpose:        fetches data column by column and send the message

Author:         Sayed Reda
Last edited:    7/2/2024
"""

import time
import pyinputplus as pyip
from data_fetcher import *



# Spreadsheet opening scopes
SCOPES: list[str] = ["https://www.googleapis.com/auth/spreadsheets"]
# [studentCol, courseCol, startDateCol, endDateCol, phoneCol]
COLS: list[int] = [1, 3, 10, 11, 13]
# The column number where to put the note
NOTE = 15

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

def main(spreadsheetURL: str, worksheetName: str, range: range) -> None:
    """
        The main function that fetches each message and check it
        then, if it's today send it and make a note, otherwise skip

        Input:      spreadsheet URL, worksheet in the spreadsheet, the range to be checkout
        Output:     None
    """
    
    global SCOPES, COLS, NOTE

    try:
        # Opening spreadsheet
        print("Opening spread sheet...")
        spreadsheet = openSpreadSheet(spreadsheetURL, SCOPES)

        # Opening worksheet
        print(f"Opening '{worksheetName}' worksheet...")
        worksheet = spreadsheet.worksheet(worksheetName)

        # Starting the sender
        print("Starting sender...")
        sender = whatsapp.WASession()

        # Sending Messages
        for row in range:
            done = False

            # To make sure that current row is check out
            while not done:
                try:
                    # Fetch ReminderMessage
                    message = fetchMessage(worksheet, row, COLS)

                    if message.startDate != '' and isToday(message.startDate):
                        message.send(sender)
                        # Mark as sent
                        worksheet.update_cell(row, NOTE, "Sent course details!")

                    done = True

                ########### Errors related to current message only ###########
                # Handling Quota exceed
                except gspread.exceptions.APIError as error:
                    if error.response.status_code == 429:
                        # Will not mark done as True to resent the message
                        print("Quota exceeded, waiting for a min...")
                        time.sleep(60)
                    else:
                        raise error
                
                # WhatsApp Sender exceptions
                except (whatsapp.exceptions.NoGroupsFound, whatsapp.exceptions.ContactNotFound) as exception:
                    worksheet.update_cell(row, NOTE, exception.__str__())
                    done = True     # To continue to rest of the rows
    
    ############# Errors related to the whole app #############
    # Credentials file is not found
    except FileNotFoundError:
        print("Credentials file is not found")
    # Invalid URL
    except gspread.SpreadsheetNotFound:
        print("Cannot find spreadsheet, check out URL")
    # Invalid WorkSheet Name
    except gspread.WorksheetNotFound:
        print(f"Worksheet '{worksheetName}' is not found")
    # Cannot open WhatsApp
    except whatsapp.exceptions.InvalidWhatsAppLogin:
        print("Cannot login to WhatsApp")
    # Input errors
    except gspread.exceptions.GSpreadException as exception:
        print(exception)

    # except:
    #     print("Unexpected error")


if __name__ == '__main__':
    spreadSheetURL = pyip.inputURL("Enter spreadsheet URL: ")
    worksheetName = pyip.inputStr("Enter worksheet name: ")
    workRange = range(*map(int, input("Enter range separated by space: ").split()))

    main(spreadSheetURL, worksheetName, workRange)
