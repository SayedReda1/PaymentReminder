"""
Name:           WhatsApp
Purpose:        A script to send WA messages in private or to the first group in common
Author:         Sayed Reda
Last edited:    4/2/2024
"""

import os
import sys
import exceptions
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


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

        # Waiting for WhatsApp to open up
        try:
            self.search_bar = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@role="textbox"][@title="Search input textbox"]'))
            )
        except TimeoutException:
            raise exceptions.InvalidWhatsAppLogin

    def sendGroupMessage(self, phone: str, msg: str) -> None:
        # Reset search bar & close previous chat
        self.closeCurrentChat()
        self.search_bar.send_keys(Keys.CONTROL + 'a')
        self.search_bar.send_keys(Keys.BACK_SPACE)
        sleep(1)
        
        # Find the contact
        self.search_bar.send_keys(phone, Keys.ENTER)

        # Open contact info
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//div[@class="_2pr2H"][@role="button"][@title="Profile Details"]'))
            ).click()
        except TimeoutException:
            raise exceptions.ContactNotFound(phone)

        # Finding first group in common & Sending the message
        try:
            # Waiting for group to show up
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//div[@class="lhggkp7q ln8gz9je rx9719la"][@style="z-index: 0; transition: none 0s ease 0s; height: 68px; transform: translateY(0px);"]'))
            ).click()

            # Droping the message in the chat box
            self.dropMessage(msg)

        except TimeoutException:
            raise exceptions.NoGroupsFound(phone)

    def sendPrivateMessage(self, phone: str, msg: str):
        # Reset search bar & close previous chat
        self.closeCurrentChat()
        self.search_bar.send_keys(Keys.CONTROL + 'a')
        self.search_bar.send_keys(Keys.BACK_SPACE)
        sleep(1)

        try:
            # Find the contact
            self.search_bar.send_keys(phone, Keys.ENTER)

            # Drop the message in chat box
            self.dropMessage(msg)

        except TimeoutException:
            # raising exception to be handled
            raise exceptions.ContactNotFound(phone)

    def dropMessage(self, msg):
        # Finding chat box
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@title="Type a message"][@role="textbox"][@contenteditable="true"]'))
        ).click()

        for line in msg.split('\n'):
            webdriver.ActionChains(self.driver).send_keys(line).perform()
            webdriver.ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        webdriver.ActionChains(self.driver).send_keys(Keys.RETURN).perform()
        sleep(1)

    def closeCurrentChat(self):
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        sleep(1)
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def quit(self):
        self.driver.close()


if __name__ == "__main__":
    s = "Testing"
    sender = WASession()
    contacts = ["1121580543", "1145082486", "115616546", "1126696747"]

    for contact in contacts:
        try:
            sender.sendGroupMessage(contact, s)
            sleep(10)

        except Exception as e:
            sys.stderr.write(e.__str__())

    sender.quit()
