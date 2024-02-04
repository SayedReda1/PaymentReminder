"""
Name:           WhatsApp
Purpose:        A script to send WA messages in private or to the first group in common
Author:         Sayed Reda
Last edited:    4/2/2024
"""

import os
import sys
import pyautogui
from time import sleep
from exceptions import *
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

        # Waiting for WhatsApp to open up
        try:
            self.search_bar = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@role="textbox"][@title="Search input textbox"]'))
            )
        except TimeoutException:
            raise InvalidWhatsAppLogin

    def sendGroupMessage(self, phone: str, msg: str) -> None:
        try:
            # Find the contact
            self.search_bar.send_keys(phone)
            self.search_bar.send_keys(Keys.ENTER)

            # Open contact info
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//div[@class="_2pr2H"][@role="button"][@title="Profile Details"]'))
                ).click()
            except TimeoutException:
                raise ContactNotFound(phone)

            # Finding first group in common & Sending the message
            try:
                # Waiting for group to show up
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
                chat_box.send_keys(Keys.ENTER)
                sleep(1)
            except TimeoutException:
                raise NoGroupsFound(phone)
        except Exception as error:
            raise error

        finally:
            # Reset search bar & close chat
            pyautogui.press('esc', presses=2)
            self.search_bar.send_keys(Keys.CONTROL + 'a')
            self.search_bar.send_keys(Keys.BACK_SPACE)
            sleep(1)

    def sendPrivateMessage(self, phone: str, msg: str):
        try:
            # Find the contact
            self.search_bar.send_keys(phone)
            self.search_bar.send_keys(Keys.ENTER)

            # Sending the message
            try:
                # Waiting for chat-box to send message
                chat_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@title="Type a message"][@role="textbox"][@contenteditable="true"]'))
                )

                # Sending each separate line
                lines: list[str] = msg.split('\n')
                for line in lines:
                    chat_box.send_keys(line)
                    chat_box.send_keys(Keys.SHIFT, Keys.ENTER)
                chat_box.send_keys(Keys.ENTER)
                sleep(1)
            except TimeoutException:
                raise ContactNotFound(phone)

        except Exception as error:
            raise error

        finally:
            # Reset search bar & close chat
            pyautogui.press('esc', presses=2)
            self.search_bar.send_keys(Keys.CONTROL + 'a')
            self.search_bar.send_keys(Keys.BACK_SPACE)
            sleep(1)
            
    def quit(self):
        self.driver.close()


if __name__ == "__main__":
    s = "Testing\nNew Line"
    sender = WASession()
    contacts = ["01121580543", "011498482486", "01126696747", "01145082486"]

    for contact in contacts:
        try:
            sender.sendGroupMessage(contact, s)

        except Exception as e:
            sys.stderr.write(e.__str__())

    sender.quit()
