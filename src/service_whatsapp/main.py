import time
import webbrowser as web

import pyautogui as pg
import pywhatkit as kit

from service_whatsapp.errors import NotLoggedInException


def check_login_whatsapp():
    print("Checking login WhatsApp.")
    web.open("https://web.whatsapp.com/")
    time.sleep(7)  # Espera para que la página se cargue completamente

    # Intenta localizar la imagen 'check.png' en la pantalla
    try:
        location = pg.locateOnScreen('src/service_whatsapp/check.png')
        if location is None:
            print("Login successful.")
            pg.hotkey('ctrl', 'w')  # Cierra la página de WhatsApp Web
            print("WhatsApp Web page closed.")
            time.sleep(3)
            return
        else:
            print("Please login to WhatsApp Web.")
            pg.hotkey('ctrl', 'w')  # Cierra la página de WhatsApp Web
            raise NotLoggedInException("Not logged in at WhatsApp Web")
    except pg.ImageNotFoundException:
        print("Image not found. Assuming login successful.")
        pg.hotkey('ctrl', 'w')  # Cierra la página de WhatsApp Web
        print("WhatsApp Web page closed.")


def send_whatsapp_message(phone, message):
    # Specify the phone number (with country code) and the message
    phone_number = phone
    message = message

    # Send the message instantly using PyWhatKit
    kit.sendwhatmsg_instantly(phone_number, message)
    time.sleep(1)
    pg.click(x=1000, y=960)  # Adjust the coordinates based on your screen
    time.sleep(1)
    pg.press("Enter")
    time.sleep(1)
    pg.hotkey('ctrl', 'w')
