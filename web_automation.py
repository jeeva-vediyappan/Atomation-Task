from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

Subjects = {
    "Software"  :10249,
    "Java"      :10244,
    "IT"        :10250,
    "Database"  :10246,
    "OS"        :10245,
    "CA"        :10251
    }

page = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 

page.get("https://learn.srmonline.in/d2l/login")

page.find_element(By.XPATH,'//*[@id="userName"]').send_keys("jv6108@srmist.edu.in")
page.find_element(By.XPATH,'//*[@id="password"]').send_keys("chemistry@3D")
page.find_element(By.CLASS_NAME,'d2l-button').click()
time.sleep(5)
page.find_element(By.XPATH,f'//*[@href="/d2l/home/{Subjects["Database"]}"]').click()

time.sleep(10)

