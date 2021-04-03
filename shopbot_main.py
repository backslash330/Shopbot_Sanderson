# Notes
# Program Requires installation of Selenium Chrome Webdriver to run
# Program Requires Windows 10 Notifications to run


# Imports
from selenium import webdriver
import PySimpleGUI as sg
import PySimpleGUIWx as sgx
import time
import multiprocessing as mp
from win10toast import ToastNotifier
import sys


def main():

    # Initialize webpages to check for stock
    dictionary = {}
    list = ["https://store.brandonsanderson.com/collections/signed-leatherbound-books/products/elantris-leather-bound-book?variant=32867344056400",
            "https://store.brandonsanderson.com/products/warbreaker-leatherbound-book?_pos=3&_sid=ff05dd89a&_ss=r&variant=32829680877648",
            "https://store.brandonsanderson.com/products/mistborn-leather-bound-book?_pos=4&_sid=27135f778&_ss=r&variant=32867379544144",
            "https://store.brandonsanderson.com/products/well-of-ascension-leather-bound-book?_pos=5&_sid=27135f778&_ss=r&variant=32872658141264",
            "https://store.brandonsanderson.com/products/the-hero-of-ages-leather-bound-book?_pos=6&_sid=27135f778&_ss=r&variant=32872552104016",
            "https://store.brandonsanderson.com/collections/all-products/products/snapshot-e-book"]

    # Initilize webpages as keys in a dictionary with zero'd values
    for i in range(len(list)):
        dictionary[list[i]] = 0

    # Initilze first PySimpleGui window where personal information is entered for purchasing
    window1 = window_1()
    while True:
        event, values = window1.read()
        if event == "OK":
            if values['-ELANTRIS-']:
                dictionary[list[0]] += 1
            if values['-WARBREAKER-']:
                dictionary[list[1]] += 1
            if values['-MISTBORN-']:
                dictionary[list[2]] += 1
            if values['-WELL-']:
                dictionary[list[3]] += 1
            if values['-HERO-']:
                dictionary[list[4]] += 1
            if values['-SNAP-']:
                dictionary[list[5]] += 1
            window1.close()
            break
        if event == sg.WIN_CLOSED:
            window1.close()
            quit()

    # Change values into variables
    name = values['-EMAIL-']
    first_name = values['-FIRST_NAME-']
    last_name = values['-LAST_NAME-']
    address = values['-ADDRESS-']
    city = values['-CITY-']
    country = values['-COUNTRY-']
    province = values['-PROVINCE-']
    zip_code = values['-ZIPCODE-']
    phone_number = values['-PHONE_NUMBER-']
    cc_number_1 = values['-CC_1-']
    cc_number_2 = values['-CC_2-']
    cc_number_3 = values['-CC_3-']
    cc_number_4 = values['-CC_4-']
    cc_name = values['-CC_NAME-']
    cc_month = values['-CC_MONTH-']
    cc_year = values['-CC_Year-']
    cc_security = values['-CC_SECURITY-']

    # Start two processes. One to search for books and another to run the system tray icon
    tray = mp.Process(target=tray_thread)
    tray.start()
    search = mp.Process(target=search_thread, args=(dictionary, list))
    search.start()
    # End the program if system tray process ends
    # TO DO: Figure out how to close selenium window when ending processes
    while True:
        if tray.is_alive():
            pass
        elif not tray.is_alive():
            toaster = ToastNotifier()
            toaster.show_toast(
                'WARNING', 'Remember to close the Webdriver Chrome Window!!!',
                threaded=True, duration=None)
            search.terminate()
            sys.exit()


def tray_thread():
    # Process and operation of the system tray icon
    # TO DO: add notification history as menu option
    # TO DO: allow change to purchase information
    # TO DO: menu option which shows run time and attempts
    menu_def = ['UNUSED', ['Information', 'End Program']]
    tray = sgx.SystemTray(
        menu=menu_def,
        data_base64=sgx.DEFAULT_BASE64_ICON,
        tooltip="Shopbot is running, right click for more info")
    while True:
        event = tray.read()
        if event == 'End Program':
            tray.close()
            quit()
        elif event == 'Information':
            tray.show_message(
                'Info',
                'The program is currently running. It will constantly check for inventory.'
                ' New Notifications will popup at key steps. Check your email for purchases!')


def search_thread(dictionary, list):
    # Initialize Webdriver
    # Correct Webdriver for Chrome Version must be installed at given path or path must be changed
    path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(path)
    # Iterate over webpages until all books are purchased
    while not (
            dictionary[list[0]] == 1
            and dictionary[list[1]] == 1
            and dictionary[list[2]] == 1
            and dictionary[list[3]] == 1
            and dictionary[list[4]] == 1):
        for i in range(len(list)):
            if dictionary[list[i]] == 1:
                pass
            else:
                driver.get(list[i])
                if "c-btn c-btn--full c-btn--primary product-single__add-btn js-product-add disabled" in driver.page_source:
                    pass
                else:
                    toaster = ToastNotifier()
                    toaster.show_toast("Info", "A book is available, ordering now.", threaded=True, duration=None)
                    dictionary[list[i]] += 1
                    purchase(driver, toaster)
    driver.close()


def purchase(driver, toaster):
    # Get through check out screen
    time.sleep(1)
    driver.find_element_by_name("add").click()
    time.sleep(1)
    driver.find_element_by_name("checkout").click()
    time.sleep(2)

    # Get through billing screen
    phonenumber = driver.find_element_by_id("checkout_email_or_phone")
    phonenumber.send_keys("newfake555@gmail.com")
    first_name = driver.find_element_by_id("checkout_billing_address_first_name")
    first_name.send_keys("Bob")
    last_name = driver.find_element_by_id("checkout_billing_address_last_name")
    last_name.send_keys("Jones")
    address = driver.find_element_by_id("checkout_billing_address_address1")
    address.send_keys("1234 Idecalreathumbwar ave")
    city = driver.find_element_by_id("checkout_billing_address_city")
    city.send_keys("balzac")
    country = driver.find_element_by_id("checkout_billing_address_country")
    country.send_keys("canada")
    province = driver.find_element_by_id("checkout_billing_address_province")
    province.send_keys("saskachewan")
    zip = driver.find_element_by_id("checkout_billing_address_zip")
    zip.send_keys("s0a 3l0")
    billing_phonenumber = driver.find_element_by_id("checkout_billing_address_phone")
    billing_phonenumber.send_keys("3034349536")
    driver.find_element_by_id("continue_button").click()

    # Get through credit card screen
    time.sleep(1)
    driver.find_element_by_xpath('//iframe[@title="Field container for: Card number"]').send_keys('4242')
    driver.find_element_by_xpath('//iframe[@title="Field container for: Card number"]').send_keys('4242')
    driver.find_element_by_xpath('//iframe[@title="Field container for: Card number"]').send_keys('4242')
    driver.find_element_by_xpath('//iframe[@title="Field container for: Card number"]').send_keys('4242')
    time.sleep(0.2)
    driver.find_element_by_xpath('//iframe[@title="Field container for: Name on card"]').send_keys('Bubba Gump')
    time.sleep(0.2)
    driver.find_element_by_xpath('//iframe[@title="Field container for: Expiration date (MM / YY)"]').send_keys(
        '09')
    driver.find_element_by_xpath('//iframe[@title="Field container for: Expiration date (MM / YY)"]').send_keys(
        '23')
    time.sleep(0.25)
    driver.find_element_by_xpath('//iframe[@title="Field container for: Security code"]').send_keys('321')
    time.sleep(0.25)
    # driver.find_element_by_xpath('//button[@id="continue_button"]').click()
    # time.sleep(10)
    # Prompt user to confirm their purchase via site email
    toaster.show_toast("Info", "A book has been purchased! Check your Email.", threaded=True, duration=None)


def window_1():
    # Input window Layout
    layout = [
                [sg.Text("North Star Automation")],
                [sg.Text("Books Already Owned")],
                [sg.Checkbox("Elantris", key='-ELANTRIS-')],
                [sg.Checkbox("Warbreaker", key='-WARBREAKER-')],
                [sg.Checkbox("Mistborn", key='-MISTBORN-')],
                [sg.Checkbox("Well of Acension", key='-WELL-')],
                [sg.Checkbox("Hero of Ages", key="-HERO-")],
                [sg.Checkbox("Snapshot", key="-SNAP-")],
                [sg.Text("Email"), sg. InputText(key='-EMAIL-')],
                [sg.Text("First Name"), sg.InputText(key='-FIRST_NAME-')],
                [sg.Text("Last Name"), sg.InputText(key='-LAST_NAME-')],
                [sg.Text("Address"), sg.InputText(key='-ADDRESS-')],
                [sg.Text("City"), sg.InputText(key='-CITY-')],
                [sg.Text("Country"), sg.InputText(key='-COUNTRY-')],
                [sg.Text("Province"), sg.InputText(key='-PROVINCE-')],
                [sg.Text("Zip Code"), sg.InputText(key='-ZIPCODE-')],
                [sg.Text("Phone Number"), sg.InputText(key='-PHONE_NUMBER-')],
                [sg.Text("Credit Card Number (Four Digits per line)")],
                [sg.InputText(key='-CC_1-')], [sg.InputText(key='-CC_2-')], [sg.InputText(key='-CC_3-')], [sg.InputText(key='-CC_4-')],
                [sg.Text("Name on Card")], [sg.InputText(key='-CC_NAME-')],
                [sg.Text("Expiry Date(Two Digits Per Line, MM Then YY)")], [sg.InputText(key='-CC_MONTH-')], [sg.InputText(key='-CC_Year-')],
                [sg.Text("Security Code(Three Digits)")], [sg.InputText(key='-CC_SECURITY-')],
                [sg.Button("OK")]
    ]
    return sg.Window("North Star Automation", layout)


if __name__ == '__main__':
    main()
