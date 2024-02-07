"""
Name:           Exceptions
Purpose:        Custom exceptions for the project structure
Author:         Sayed Reda
Last edited:    4/2/2024
"""


class InvalidWhatsAppLogin(Exception):
    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return f"Cannot login to WhatsApp.\n"


class ContactNotFound(Exception):
    def __init__(self, phone):
        super().__init__(self)
        self.phone = phone

    def __str__(self):
        return f"Contact is not found, try saving it to your contacts.\n"


class NoGroupsFound(Exception):
    def __init__(self, contact):
        super().__init__(self)
        self.contact = contact

    def __str__(self):
        return f"No groups in common.\n"
