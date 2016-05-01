#!/usr/bin/python
# -*- coding: utf-8 -*-
# import requests
# import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# driver = webdriver.Firefox()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()

city_from = "Kúty"
city_to = "BRATISLAVA"

driver = webdriver.Firefox()
driver.get(
    "https://ikvc.slovakrail.sk/inet-sales-web/pages/connection/search.xhtml")

delay = 5  # wait seconds for web page to load
try:
    WebDriverWait(driver, delay)\
        .until(EC.presence_of_all_elements_located
               (driver.find_element_by_id('searchParamForm')))
    print("Page is ready.")
except TimeoutException:
    print("Loading took too much time.")

assert "Železničný cestovný poriadok a predaj lístkov" in driver.title

elem_city_from = driver.find_element_by_id("searchParamForm:fromInput")
elem_city_to = driver.find_element_by_id("searchParamForm:toInput")

elem_city_from.send_keys(city_from)
elem_city_to.send_keys(city_to)
elem_city_to.send_keys(Keys.RETURN)
