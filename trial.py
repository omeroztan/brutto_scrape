from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import pandas as pd
import time, requests, json, math, logging, os
from tenacity import retry, wait_fixed, stop_after_attempt, RetryError

options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument('--disable-logging')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
link = "https://www.brutto-netto-rechner.info/"
driver.get(link) # our address that we want to scrape