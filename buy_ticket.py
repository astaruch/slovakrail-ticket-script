#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse

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

elem_city_from.send_keys(city_from)
elem_city_to.send_keys(city_to)
elem_city_to.send_keys(Keys.RETURN)

# There is now list of trains.
delay = 5
driver.find_element_by_xpath(
    "//form[@id='searchForm']/div/table/tbody/tr[contains(.,\'" +
    train_number + "\')]/td[contains(.,'Nákup dokladu')]/a"
).click()
delay = 5
driver.find_element_by_xpath(
    "//form[@id='searchForm']/div/table/tbody/tr[contains(.,\'" +
    train_number + "\')]/td[contains(.,'Nákup dokladu')]/div/a"
).click()
