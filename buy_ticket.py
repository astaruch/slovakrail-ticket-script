#!/usr/bin/python3.6
# coding=UTF-8


import sys
import argparse
import datetime

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


def log_info(msg):
    sys.stdout.write(
        "{} INFO: {}\n".format(
            datetime.datetime.now(),
            msg
        )
    )

def encode(key, string):
    encoded_chars = []
    for i in xrange(string):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string)


def decode(key, string):
    encoded_chars = []
    for i in xrange(string):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string)


def getPersonFromFile(filename):
    import imp
    f = open(filename)
    global person
    person = imp.load_source('person', '', f)
    f.close()


def buy_ticket(args):

    # Loading values from arguments to variables
    city_to = args.to_city
    city_from = args.from_city
    train_time = args.time
    train_date = args.date
    train_name = args.name
    train_number = args.number

    # Work only with one argument
    train = ''
    if train_number is not None:
        train = train_number
    elif train_name is not None:
        train = train_name
    else:
        train = train_time

    # Launch Firefox web browser.
    driver = webdriver.Firefox()

    # Logging information
    log_info("Opened {} (version {}).".format(
            driver.capabilities["browserName"],
            driver.capabilities["browserVersion"]
        )
    )

    # Use full screen mode.
    driver.maximize_window()

    # Sets a sticky timeout to implicitly wait for an element to be found, or a command to complete.
    driver.implicitly_wait(30)

    # get tickets throught zssk - date can be entered
    driver.get('https://www.zssk.sk/')

    try:
        delay = 30  # wait seconds for web page to load, added more second

        WebDriverWait(driver, delay).until(
            EC.presence_of_all_elements_located(
                (By.ID, 'vlak_form')
            )
        )

        # Logging information
        log_info('Page is ready.')

    except TimeoutException:
        log_info('Loading took too much time.')

    assert 'SK | ZSSK Slovakrail' in driver.title

    sleep(1)

    # Input elements selected by CSS #id selector from the web page.
    elem_city_from = driver.find_element_by_id('TrainSearchFormFrom')
    elem_city_to = driver.find_element_by_id('TrainSearchFormTo')
    elem_date = driver.find_element_by_id('date_vlak')
    elem_time = driver.find_element_by_id('vlak_time')

    # Set from and to city and hit enter
    elem_city_from.clear()
    elem_city_from.send_keys(city_from)
    sleep(0.5)
    elem_city_to.clear()
    elem_city_to.send_keys(city_to)
    sleep(0.5)
    elem_date.clear()
    elem_date.send_keys(train_date)
    sleep(0.5)
    elem_time.clear()
    elem_time.send_keys(train_time)
    sleep(0.5)
    elem_city_to.send_keys(Keys.RETURN)

    # Logging information
    log_info("Filled train credentials.")

    sleep(3)

    # There is now list of trains.
    # 'Nakup dokladu'
    driver.find_element_by_xpath(
        "//form[@id='searchForm']/div/table/tbody/tr[contains(.,\'" + train + "\')]/td[contains(.,'Nákup lístka')]/a"
    ).click()
    log_info("Nakup dokladu.")
    sleep(1)

    # 'Cestovny listok'
    driver.find_element_by_xpath(
        "//form[@id='searchForm']/div/table/tbody/tr[contains(.,\'" + train + "\')]/td[contains(.,'Lístok')]/div/a"
    ).click()
    log_info("Cestovny listok.")
    sleep(0.5)

    # We are on specific train (based on name or number).
    # 'Zvolte typ cestujuceho'
    driver.find_element_by_xpath(
        "//table[@id='tmp-table-parameters']/tbody/tr[2]/td[1]/div/div"
    ).click()
    log_info("Zvolte typ cestujuceho.")
    sleep(0.5)

    # 'Ziak/student' -> is option li[3]. If you are not student, edit it to appropriate value.
    driver.find_element_by_xpath(
        "//table[@id='tmp-table-parameters']/tbody/tr[2]/td[1]/div/ul/li[3]"
    ).click()
    log_info("Ziak/student.")
    sleep(2)

    # 'Pokracovat v nakupe'
    driver.find_element_by_xpath(
        "//form[@id='ticketParam']/div[2]/div/a[2]"
    ).click()
    log_info("Pokracovat v nakupe.")
    sleep(1.5)

    # We are on revision page with shoping basket
    # 'Pokracovat v nakupe'
    driver.find_element_by_xpath(
        "//form[@id='shoppingCart']/div/div[2]/div/a[2]"
    ).click()
    log_info("Pokracovat v nakupe - kontrola.")
    sleep(1)

    # 'Chcem zaplatit bez prihlasenia alebo registracie'
    driver.find_element_by_xpath(
        "//form[@id='loginMode']/div/div[1]/div[3]/p/a/label"
    ).click()
    sleep(2)

    # We are on page with information about passengers
    # Load info about person from external person.txt

    getPersonFromFile('person.txt')

    # Fillup info in webpage from file

    # 'Email'
    driver.find_element_by_id(
        'personalData:payerItemsList:0:field'
    ).send_keys(person.email)

    # 'Name'
    driver.find_element_by_id(
        'personalData:shoppingCartItemList:0:travellerItemsList:0:field'
    ).send_keys(person.name)

    # 'Surname'
    driver.find_element_by_id(
        'personalData:shoppingCartItemList:0:travellerItemsList:1:fieldRegId'
    ).send_keys(person.surname)

    # 'Registration number'
    driver.find_element_by_id(
        'personalData:shoppingCartItemList:0:travellerItemsList:2:fieldRegId'
    ).send_keys(person.train_card)

    log_info("Filled account credentials.")

    sleep(1)

    # 'Pokracovat v platbe'
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//form[@id='personalData']/div/div[2]/a[2]")
        )
    )
    log_info("Pokracovat v platbe.")
    sleep(1)

    driver.find_element_by_xpath(
        "//form[@id='personalData']/div/div[2]/a[2]"
    ).click()
    log_info("Click ONE.")
    sleep(1)

    # BUG FIX: zssk page has a bug that requires another click
    driver.find_element_by_xpath(
        "//form[@id='personalData']/div/div[2]/a[2]"
    ).click()
    log_info("Click TWO.")
    sleep(1)

    # 'Suhlas s obchodnymi podmienkami'
    driver.find_element_by_xpath(
        "//div[@id='tmp-payment']/div[1]/div[4]/p[2]/label"
    ).click()
    log_info("Suhlas s obchodnymi podmienkami.")
    sleep(1)

    # 'Pokracovat v nakupe'
    driver.find_element_by_xpath(
        "//div[@id='tmp-payment']/div[2]/a[2]"
    ).click()
    log_info("Pokracovat v nakupe.")

    log_info("Stránka s PDF.")

    sleep(3)

    # Close the web browser (Firefox).
    driver.close()

    # Logging information
    log_info("Closed {} (version {}).".format(
            driver.capabilities["browserName"],
            driver.capabilities["browserVersion"]
        )
    )


def main():

    # Logging information
    log_info("Running {}".format(
        __file__
        )
    )

    parser = argparse.ArgumentParser(
        description = '''
Automated buying webticket for slovak rails. You must specify origin city
and the destination, in exactly form, like it is on the website of the zssk.
https://ikvc.slovakrail.sk/inet-sales-web/pages/connection/initSearch.xhtml.
You must specify, leaving time from origin city, name of the train or his
number. Only one is required.''',

        epilog = '''
EXAMPLES
    python buy_ticket.py create --txt person
        Create simple encrypted file with info about person needed in forms.

    python buy_ticket.py create --txt card
        Create simple encrypted file with info about credit card.

    python buy_ticket.py buy -f 'Bratislava hl.st.' -to Kúty -t 04:55
        Buy ticket from Bratislava to Kúty for a train which is leaving
        Bratislava at 04:55 and then send ticket to the email.

    python buy_ticket.py buy -f Kúty -to 'Bratislava hl.st.' --name Slovan
        Buy ticket from Kuty to Bratsilava for a train named Slovan and
        then send ticket to the email.
''',

        formatter_class = argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'OPTION',
        help='This will determine run of\
        program. \n If you are running for the first time,\
        run with option "create" following --txt card/person.\
        Program will create card.txt or person.txt, which uses\
        later. \n \n Otherwise use option "buy" with other\
        arguments. For further info see examples.'
    )

    parser.add_argument(
        '--from-city',
        '-f',
        help='From this city.'
    )

    parser.add_argument(
        '--to-city',
        '-to',
        help='To this city.'
    )

    parser.add_argument(
        '--time',
        '-t',
        help='Time when train is leaving from origin station. Format HH:MM.'
    )

    parser.add_argument(
        '--date',
        '-d',
        help='Date when train is leaving from origin station. Format: DD.MM.YYYY.'
    )

    parser.add_argument(
        '--name',
        '-n',
        help='Exact name of the train, e.g. \'slovenská strela\', \'csárdás\', ...'
    )

    parser.add_argument(
        '--number',
        '-nr',
        help='Number of the train, e.g. 270, 271, ...'
    )

    parser.add_argument(
        '--txt',
        help='Create credit card ("card") or person ("person").'
    )

    # Argument parsing.
    args = parser.parse_args()

    if args.OPTION == 'buy':
        buy_ticket(args)
    elif args.OPTION == 'create':
        if args.OPTION == 'card':
            pass
        elif args.OPTION == 'person':
            pass
        else:
            log_info('Wrong argument for creating text file. Try again.')
    else:
        log_info('You missed argument to create text file/buying ticket. Try again.')

    # Logging information
    log_info("Terminating {}".format(
        __file__
        )
    )

    # Terminate the program with exit status 0.
    sys.exit(0)


if __name__ == '__main__':
    main()
