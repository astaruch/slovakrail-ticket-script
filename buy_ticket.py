#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser(description='Automated buying webticket \
                                 for slovak rails. You must specify origin\
                                 city and the destination, in exactly form,\
                                 like it is on the website\
                                 https://ikvc.slovakrail.sk/inet-sales-web/pages/connection/initSearch.xhtml.\n\
                                 You must specify, leaving time from origin\
                                 city, name of the train or his number. Only\
                                 one is required.')
parser.add_argument('FROM', help='From this city.')
parser.add_argument('TO', help='To this city.')
parser.add_argument('--time', '-t', help='Time when train is leaving \
                    origin station. Format HH:MM.')
parser.add_argument('--name', '-n', help='Exact name of the train,\
                    e.g. \'slovenská strela\', \'csárdás\', ...')
parser.add_argument('--number', '-nr', help='Number of the train,\
                    e.g. 270, 271, ...')

args = parser.parse_args()

city_from = (args.FROM)
city_to = (args.TO)
train_time = (args.time)
train_name = (args.name)
train_number = (args.number)

# Work only with one argument
train = ""
if train_number is not None:
    train = train_number
elif train_name is not None:
    train = train_name
else:
    train = train_time

print(city_from, city_to, train_time, train_name, train_number)

driver = webdriver.Firefox()
driver.get(
    "https://ikvc.slovakrail.sk/inet-sales-web/pages/connection/search.xhtml")

delay = 5  # wait seconds for web page to load
try:
    WebDriverWait(driver, delay)\
        .until(EC.presence_of_all_elements_located
               ((By.ID, "searchParamForm"))
               )
    print("Page is ready.")
except TimeoutException:
    print("Loading took too much time.")

assert "Železničný cestovný poriadok a predaj lístkov" in driver.title

elem_city_from = driver.find_element_by_id("searchParamForm:fromInput")
elem_city_to = driver.find_element_by_id("searchParamForm:toInput")

# Set from and to city and hit enter
elem_city_from.send_keys(city_from)
elem_city_to.send_keys(city_to)
elem_city_to.send_keys(Keys.RETURN)
sleep(2)

# There is now list of trains.
# 'Nakup dokladu'
driver.find_element_by_xpath(
    "//form[@id='searchForm']/div/table/tbody/tr[contains(.,\'" +
    train + "\')]/td[contains(.,'Nákup dokladu')]/a"
).click()
sleep(1)
# 'Cestovny listok'
driver.find_element_by_xpath(
    "//form[@id='searchForm']/div/table/tbody/tr[contains(.,\'" +
    train + "\')]/td[contains(.,'Nákup dokladu')]/div/a"
).click()
sleep(0.5)

# We are on specific train (based on name or number)
# 'Zvolte typ cestujuceho'
driver.find_element_by_xpath(
    "//table[@id='tmp-table-parameters']/tbody/tr[2]/td[1]/div/div"
).click()
sleep(0.5)

# 'Ziak/student'
driver.find_element_by_xpath(
    "//table[@id='tmp-table-parameters']/tbody/tr[2]/td[1]/div/ul/li[3]"
).click()
sleep(2)

# 'Pokracovat v nakupe'
driver.find_element_by_xpath(
    "//form[@id='ticketParam']/div[2]/a[2]"
).click()
sleep(3)

# We are on revision page with shoping basket
# 'Pokracovat v nakupe'
driver.find_element_by_xpath(
    "//form[@id='shoppingCart']/div/div[2]/div/a[2]"
).click()
sleep(1)

# 'Chcem zaplatit bez prihlasenia alebo registracie'
driver.find_element_by_xpath(
    "//form[@id='loginMode']/div/div[1]/div[3]/p/a/label"
).click()
sleep(2)

# We are on page with information about pasagiers
# Fillup info
