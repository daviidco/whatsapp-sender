import time
import webbrowser as web

import pyautogui as pg
import pywhatkit as kit

from service_whatsapp.handle_errors import NotLoggedInException


def check_login_whatsapp() -> None:
    """
    Checks if the user is logged in to WhatsApp.

    Raises: pg.ImageNotFoundException: If the image 'check.png' is not found on the screen.
    """
    print("Checking WhatsApp login.")
    web.open("https://web.whatsapp.com/")
    time.sleep(7)  # Waiting for the page to load completely.

    # Try to locate the image 'check.png' on the screen.
    try:
        location = pg.locateOnScreen('src/service_whatsapp/check.png')
        if location is None:
            print("Login successful.")
            pg.hotkey('ctrl', 'w')  # Closes the WhatsApp Web page.
            print("WhatsApp Web page closed.")
            time.sleep(3)
            return
        else:
            print("Please login to WhatsApp Web.")
            pg.hotkey('ctrl', 'w')  # Closes the WhatsApp Web page.
            raise NotLoggedInException("Not logged in at WhatsApp Web")
    except pg.ImageNotFoundException:
        print("Image not found. Assuming login successful.")
        pg.hotkey('ctrl', 'w')  # Cierra la página de WhatsApp Web
        print("WhatsApp Web page closed.")


def send_whatsapp_message(phone: str, message: str) -> None:
    """
    Sends a WhatsApp message specified by the phone number and message content.

    Args:
        phone (str): The phone number with country code.
        message (str): The message content to be sent.
    """
    # Specify the phone number (with country code) and the message
    phone_number = phone
    message = message

    # Send the message instantly using PyWhatKit
    kit.sendwhatmsg_instantly(phone_number, message)
    time.sleep(1)
    pg.hotkey('ctrl', 'w')
