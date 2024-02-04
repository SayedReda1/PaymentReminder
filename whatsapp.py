import os
import keyword
from time import sleep

import keyboard
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

    def sendGroupMessage(self, phone: str, msg: str) -> str:
        # Opening WA & Start search
        try:
            # Waiting for WhatsApp to open up
            search_bar = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@role="textbox"][@title="Search input textbox"]'))
            )
            # Find the contact
            search_bar.send_keys(phone)
            search_bar.send_keys(Keys.ENTER)
        except TimeoutException:
            return f"{phone}: Cannot open WhatsApp"

        # Open group info
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//div[@class="_2pr2H"][@role="button"][@title="Profile Details"]'))
            ).click()
        except TimeoutException:
            return f"{phone}: Contact not found"

        # Finding first group in common & Sending the message
        try:
            # Waiting for contact to show up
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//div[@class="lhggkp7q ln8gz9je rx9719la"][@style="z-index: 0; transition: none 0s ease 0s; height: 68px; transform: translateY(0px);"]'))
            ).click()

            # Send Message
            chat_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@title="Type a message"][@role="textbox"][@contenteditable="true"]'))
            )

            # Sending each multi-line messages
            lines: list[str] = msg.split('\n')
            for line in lines:
                chat_box.send_keys(line)
                chat_box.send_keys(Keys.SHIFT, Keys.ENTER)
            sleep(1)
            chat_box.send_keys(Keys.ENTER)
            sleep(1)
        except TimeoutException:
            return f"{phone}: No groups in common"

        # Reset search bar & close chat
        keyboard.press_and_release("esc")
        search_bar.send_keys(Keys.CONTROL + 'a')
        search_bar.send_keys(Keys.BACK_SPACE)

        return f"{phone}: Message has been sent successfully"

    def sendPrivateMessage(self, phone: str, msg: str):
        # Opening WA & Start search
        try:
            # Waiting for WhatsApp to open up
            search_bar = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@role="textbox"][@title="Search input textbox"]'))
            )
            # Find the contact
            search_bar.send_keys(phone)
            search_bar.send_keys(Keys.ENTER)
        except TimeoutException:
            return f"{phone}: Cannot open WhatsApp"

        try:
            # Send Message
            chat_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@title="Type a message"][@role="textbox"][@contenteditable="true"]'))
            )

            # Sending each multi-line messages
            lines: list[str] = msg.split('\n')
            for line in lines:
                chat_box.send_keys(line)
                chat_box.send_keys(Keys.SHIFT, Keys.ENTER)
            sleep(1)
            chat_box.send_keys(Keys.ENTER)
            sleep(1)
        except TimeoutException:
            return f"{phone}: Contact not found"

        # Reset search bar & close chat
        keyboard.press_and_release("esc")
        search_bar.send_keys(Keys.CONTROL + 'a')
        search_bar.send_keys(Keys.BACK_SPACE)

        return f"{phone}: Message has been sent successfully"

    def quit(self):
        self.driver.close()


if __name__ == "__main__":
    s = "Testing\nNew Line"
    sender = WASession()
    print(sender.sendGroupMessage("01126696747", s))
    print(sender.sendPrivateMessage("01145082486", "Hi there!"))
    print(sender.sendPrivateMessage("01135782486", "Hi there!"))
    print(sender.sendGroupMessage("01145082486", s))


# TODO: Nested Try