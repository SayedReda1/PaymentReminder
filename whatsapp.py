import os
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class WASession:
    """
        ? Sends a message and returns result, whether success of failure
    """

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(
            f"user-data-dir=C:\\Users\\{os.environ.get('username')}\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        self.driver = webdriver.Chrome(self.options)
        self.driver.get("https://web.whatsapp.com")

    def sendGroupMessage(self, group_name: str, msg: str) -> str:
        """
            ? send a message to a group via group name
        """

        # Opening WA & Start search
        try:
            # Waiting for WhatsApp to open up
            search_bar = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@role="textbox"][@title="Search input textbox"]'))
            )
            # Find the group
            search_bar.send_keys(group_name)
            search_bar.send_keys(Keys.ENTER)
        except TimeoutException:
            return "Cannot open WhatsApp"

        # Finding group & Sending the message
        try:
            # Waiting for contact to show up
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div/div[1]'))
            ).click()

            # Send Message
            chat_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@title="Type a message"][@role="textbox"][@contenteditable="true"]'))
            )

            # Sending each multiline messages
            lines: list[str] = msg.split('\n')
            for line in lines:
                chat_box.send_keys(line)
                chat_box.send_keys(Keys.SHIFT, Keys.ENTER)
            sleep(1)
            chat_box.send_keys(Keys.ENTER)
            sleep(2)
        except TimeoutException:
            return "Cannot find contact"

        # Reset search bar
        search_bar.send_keys(Keys.CONTROL + 'a')
        search_bar.send_keys(Keys.BACK_SPACE)

        return "Message has been sent successfully"

    def sendPrivateMessage(self, phone_num: str, msg: str):
        pass

    def quit(self):
        self.driver.close()


if __name__ == "__main__":
    s = "Hello my friend {name}\nI'm texting your at {time}\nplease call me as soon as your get up\nThank you 🌹"
    sender = WASession()
    s = s.format(name="Sayed", time="23:00")

    sender.sendGroupMessage(msg=s, group_name="Testing")