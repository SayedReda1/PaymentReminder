import whatsapp
from data_fetcher import *



def main():
    # Fetching data
    try:
        data = fetchData("https://docs.google.com/spreadsheets/d/1jQuoxYS6utICkmwbWg3e-pu7y8-i7cDu-9_sbAzmBx0/edit?usp=sharing",
                            "Sheet1", range(2, 57+1))
    
        # Starting WhatsApp sender object
        sender = whatsapp.WASession()

        # Sending messages
        for message in data:
            try:
                message.send(sender)
            except Exception as error:
                print(error)
    
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
        print("Invalid row or column input, try again")
        print(f"Message: {error.args[0]['message']}")
    
    except whatsapp.InvalidWhatsAppLogin as error:
        print(error)
    
    except:
        print("Unexpected error")

if __name__ == '__main__':
    main()
