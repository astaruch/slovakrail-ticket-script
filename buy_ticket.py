#!/usr/bin/python3.6
# coding=UTF-8

import os
import sys
import argparse
import datetime

from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def die(message,exitcode):
    sys.stderr.write("{}\n".format(message))
    sys.exit(exitcode)


def is_date(msg):
    try:
        datetime.datetime.strptime(msg, '%d.%m.%Y')
    except ValueError:
        die("Wrong date option!",2)


def is_time(msg):
    try:
        datetime.datetime.strptime(msg, '%H:%M')
    except ValueError:
        die("Wrong time option!",3)


def log_info(msg):
    sys.stdout.write(
        "{} INFO: {}\n".format(
            datetime.datetime.now(),
            msg
        )
    )

def load_user_credentials(filename):
    import imp
    f = open(filename)
    credentials = imp.load_source('person', '', f)
    f.close()
    return credentials


def buy_ticket(args):

    # FIREFOX DESTINATION FOLDER
    folder = os.path.dirname(os.path.realpath(__file__))

    # FIREFOX OPTIONS
    options = Options();
    options.headless = True

    # FIREFOX PROFILE
    profile = FirefoxProfile()
    profile.set_preference("browser.download.folderList",2);
    profile.set_preference("browser.download.manager.showWhenStarting", False);
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel");
    profile.set_preference("browser.download.dir",str(folder));
    log_info('browser.download.dir = "{}"'.format(str(folder)))

    # Launch Firefox web browser.
    driver = webdriver.Firefox(options=options, firefox_profile=profile)

    # Use full screen mode.
    # driver.maximize_window()

    # Logging information
    log_info("Opened {} (version {})".format(
            driver.capabilities["browserName"],
            driver.capabilities["browserVersion"]
        )
    )

    # Sets a sticky timeout to implicitly wait for an element to be found, or a command to complete.
    driver.implicitly_wait(30)

    # Load page 'Vyhľadanie spojenia'
    driver.get('https://ikvc.slovakrail.sk/esales/search')

    try:
        delay = 30  # wait seconds for web page to load, added more second

        WebDriverWait(driver, delay).until(
            EC.presence_of_all_elements_located(
                (By.ID, 'searchPanel')
            )
        )

        # Logging information
        log_info('Loaded page "Vyhľadanie spojenia"')

    except TimeoutException:
        log_info('Loading took too much time.')
        # TODO FIXME

    sleep(1)

    # Info
    log_info('Page title is "{}".'.format(driver.title))

    assert 'ZSSK' in driver.title

    # FROM
    elem_city_from = driver.find_element_by_id('fromInput')
    elem_city_from.clear()
    elem_city_from.send_keys(args.departure)
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[3]/div/div/form/div[1]/div/div[1]/div[1]/div[1]/ul/li/a'
    ).click
    log_info('Filling "Odkiaľ" in "Vyhľadanie spojenia" with "{}".'.format(args.departure))
    sleep(0.5)

    # TO
    elem_city_to = driver.find_element_by_id('toInput')
    elem_city_to.clear()
    elem_city_to.send_keys(args.arrival)
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[3]/div/div/form/div[1]/div/div[1]/div[1]/div[3]/ul/li/a'
    ).click
    log_info('Filling "Kam" in "Vyhľadanie spojenia" with "{}".'.format(args.arrival))
    sleep(0.5)

    # DATE
    elem_date = driver.find_element_by_id('departDate')
    elem_date.clear()
    elem_date.send_keys(args.date)
    driver.find_element_by_xpath('//html').click();
    log_info('Filling "Dátum cesty tam" in "Vyhľadanie spojenia" with "{}".'.format(args.date))
    sleep(0.5)

    # TIME
    elem_time = driver.find_element_by_id('departTime')
    elem_time.clear()
    elem_time.send_keys(args.time)
    driver.find_element_by_xpath('//html').click();
    log_info('Filling "Odchod" in "Vyhľadanie spojenia" with "{}".'.format(args.time))
    sleep(0.5)

    log_info('Filled train credentials in "Vyhľadanie spojenia".')

    # CONFIRM
    driver.find_element_by_id('actionSearchConnectionButton').click()
    log_info('Clicked on "Vyhľadať spojenie".')
    sleep(2)

    # CLICK ON FIRST
    driver.find_element_by_css_selector(
        'div.connection-group:nth-child(2) > div:nth-child(1)'
    ).click()
    log_info('Clicked on first train.')
    sleep(0.5)

    # BUY TICKET
    driver.find_element_by_xpath(
        '//*[@id="dayGroupLoop:0:eSalesConnectionLoop:0:j_idt302"]'
    ).click()
    log_info('Clicked on "Kúpiť lístok".')
    sleep(0.5)

    # PASSENGER TYPE SELECTION
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[3]/span/div/div[1]/form/div/div/div/div/div/div/div[1]/div[1]/div/div/div/div/a[1]/span[2]'
    ).click()
    log_info('Choosing passenger type.')
    sleep(0.5)

    # JUNIOR SELECTION
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[3]/span/div/div[1]/form/div/div/div/div/div/div/div[1]/div[1]/div/div/div[1]/div/a[1]/ul/li[3]'
    ).click()
    log_info('Selected "Mladý (16 - 25 r.)".')
    sleep(0.5)

    # DISCOUNT SELECTION
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[3]/span/div/div[1]/form/div/div/div/div/div/div/div[1]/div[1]/div/div/div/div/a[2]/span[2]'
    ).click()
    log_info('Choosing card type.')
    sleep(0.5)

    # CARD SELECTION
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[3]/span/div/div[1]/form/div/div/div/div/div/div/div[1]/div[1]/div/div/div[1]/div/a[2]/ul/li[2]'
    ).click()
    log_info('Selected "Preukaz pre žiaka/Študenta".')
    sleep(1)

    # ENABLED OPTION FOR FREE TICKET
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[3]/span/div/div[1]/form/div/div/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div/label'
    ).click()
    log_info('Checkbox enabled for "Nárok na bezplatnú prepravu".')
    sleep(0.5)

    # CONTINUE
    driver.find_element_by_xpath(
        '//*[@id="actionIndividualContinue"]'
    ).click()
    log_info('Clicked on "Pokračovať" at "Voľba cestujúcich".')
    sleep(2)

    # CONTINUE
    driver.find_element_by_xpath(
        '//*[@id="ticketsForm:connection-offer:final-price:j_idt198"]'
    ).click()
    log_info('Clicked on "Pokračovať" at "Voľba cestovného lístka".')
    sleep(1)

    # CONTINUE
    driver.find_element_by_xpath(
        '//*[@id="ticketsForm:j_idt97"]'
    ).click()
    log_info('Clicked on "Pokračovať" at "Doplnkové služby".')
    sleep(1)

    # CONTINUE
    driver.find_element_by_xpath(
        '//*[@id="cartForm:j_idt284"]'
    ).click()
    log_info('Clicked on "Pokračovať" at "Obsah košíka (1)".')
    sleep(1)

    # LOAD PERSONAL INFORMATION
    person = load_user_credentials('person.txt')

    # FILL EMAIL
    email = driver.find_element_by_id('email')
    email.clear()
    email.send_keys(person.email)
    log_info('Filling "Váš e-mail" at "Osobné údaje (2)".')

    # FILL NAME
    name = driver.find_element_by_id('cartItemLoop:0:connectionPersonal:passengerLoop:0:firstname')
    name.clear()
    name.send_keys(person.name)
    log_info('Filling "Meno" at "Osobné údaje (2)".')

    # FILL SURNAME
    surname = driver.find_element_by_id('cartItemLoop:0:connectionPersonal:passengerLoop:0:lastname')
    surname.clear()
    surname.send_keys(person.surname)
    log_info('Filling "Priezvisko" at "Osobné údaje (2)".')

    # FILL REGISTRATION NUMBER
    card_number = driver.find_element_by_id('cartItemLoop:0:connectionPersonal:passengerLoop:0:cislo-registracie-p1')
    card_number.clear()
    card_number.send_keys(person.train_card)
    log_info('Filling "Číslo registrácie:" at "Osobné údaje (2)".')

    log_info('All personal informations filled at "Osobné údaje (2)".')

    # CONTINUE
    driver.find_element_by_xpath(
        '//*[@id="j_idt177"]'
    ).click()
    log_info('Clicked on "Pokračovať" at "Osobné údaje (2)".')
    sleep(0.5)

    # I AGREE WITH THE TERMS AND CONDITIONS
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[3]/div[2]/div/form/div/div/div[1]/div/div/div/label'
    ).click()
    log_info('Checkbox enabled for "Súhlasím s obchodnými podmienkami " at "Výber platby (3)".')
    sleep(0.5)

    # CONTINUE
    driver.find_element_by_xpath(
        '//*[@id="j_idt107"]'
    ).click()
    log_info('Clicked on "Pokračovať" at "Výber platby (3)".')
    sleep(0.5)

    # PAY
    driver.find_element_by_xpath(
        '//*[@id="cartForm:j_idt240"]'
    ).click()
    log_info('Clicked on "Zaplatiť" at "Súhrn (4)".')
    sleep(0.5)

    """
    TODO

    # DOWNLOAD PDF
    log_info('DOWNLOAD: Clicked on "Uložiť lístok".')
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[3]/div[2]/div/form/div/div/div[3]/div[1]/a'
    ).click()

    log_info('DOWNLOAD: PDF downloaded to "{}".'.format(str(folder)))
    """

    # Close the web browser (Firefox).
    driver.close()

    # Info
    log_info("Closed {} (version {}).".format(
            driver.capabilities["browserName"],
            driver.capabilities["browserVersion"]
        )
    )


def main():

    # Info
    log_info("Running {}".format(str(__file__)))

    # Argument parser
    parser = argparse.ArgumentParser(
        description = (
            'Automated webticket buying for "slovakrail.sk". You have to specify\n'
            'departure and arrival stations, date and time in an exact form, like\n'
            'it is on the website of the "slovakrail.sk".\n'
        ),
        epilog = (
            'EXAMPLES\n'
            '       ./buy_ticket.py -de "Bratislava hl.st." -ar "Kúty" -t "05:16" -d "18.03.2019"\n'
            '       python buy_ticket.py -de "Bratislava hl.st." -ar "Kúty" -t "05:16" -d "18.03.2019"\n'
        ),
        formatter_class = argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--departure',
        '-de',
        help='Exact departure station. Example: Bratislava hl.st.'
    )
    parser.add_argument(
        '--arrival',
        '-ar',
        help='Exact arrival station. Example: Kúty'
    )
    parser.add_argument(
        '--time',
        '-t',
        help='Exact departure time in format: HH:MM. Example: 08:08'
    )
    parser.add_argument(
        '--date',
        '-d',
        help='Exact departure date in format: DD.MM.YYYY. Example: 16.03.2019'
    )

    # Argument parsing.
    args = parser.parse_args()

    # Date check
    is_date(args.date)
    log_info('DATE = {}'.format(args.date))

    # Time check
    is_time(args.time)
    log_info('TIME = {}'.format(args.time))

    # Departure destination check
    if isinstance(args.departure, str):
        log_info('DEPARTURE = {}'.format(args.departure))
    else:
        die("Wrong departure option!",4)

    # Arrival destination check
    if isinstance(args.arrival, str):
        log_info('ARRIVAL = {}'.format(args.arrival))
    else:
        die("Wrong arrival option!",5)

    # Buy ticket
    buy_ticket(args)

    # Info
    log_info("Terminating {}".format(str(__file__)))

    # Terminate the program with exit status 0.
    sys.exit(0)


if __name__ == '__main__':
    main()
