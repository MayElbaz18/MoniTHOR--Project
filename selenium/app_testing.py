import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException
import time , json
from utils import   get_url_status ,certificate_checks
# Full path to the ChromeDriver executable file
with open('config.json', 'r') as f:
    config = json.load(f)
url=f"{config['host']}:{config['port']}/"
# Initialize the WebDriver
driver = webdriver.Chrome()

def is_alert_present(): 
    try: 
        driver.switch_to.alert 
        return True 
    except NoAlertPresentException: 
        return False
    
def register(username,password1,paswword2):
    # Rgister user tester 
    driver.get(f"{url}/register")
    input_field = driver.find_element("id", "username")
    input_field.send_keys("tester")
    input_field = driver.find_element("id", "password1")
    input_field.send_keys("tester")
    input_field = driver.find_element("id", "password2")
    input_field.send_keys("tester")
    button = driver.find_element("class name", "register-submit")
    button.click()
    # waiting for alert to pop up before close
    while is_alert_present()==False: 
        time.sleep(1)

    alert = driver.switch_to.alert
    alert.accept()


def login(useraname,password):
    # login user teser 
    driver.get(f"{url}/login")    
    input_field = driver.find_element("id", "username")
    input_field.send_keys("tester")

    input_field = driver.find_element("id", "password")
    input_field.send_keys("tester")

    button = driver.find_element("class name", "login-submit")
    button.click()

def single_upload(domain):
        # settin single domain input    
    input_field = driver.find_element("id", "single")
    input_field.send_keys(domain)
    button = driver.find_element("class name", "single-submit")
    button.click()
    while is_alert_present()==False: 
        time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(5)
    
def verfiy_results(domain):
    # analysing results
    table_body = driver.find_element("id", "resultsBody")
    # Iterate through the rows of the table body
    rows = table_body.find_elements("tag name", "tr")
    for row in rows:
        # Extract cells (td elements) in the row
        cells = row.find_elements("tag name", "td")
        if domain==cells[0].text:
            # Extract text from each cell
            domain = cells[0].text
            status = cells[1].text
            expiration_date = cells[2].text
            issuer = cells[3].text            

    # getting validation data and compare compare with UI 
    status_validation = get_url_status(domain)
    if not  (status_validation =='OK' or status_validation =='FAILED'):     
        sys.exit(1)

    cert=certificate_checks(domain)
    if not (expiration_date == cert[0]):            
        sys.exit(1)    
    if not issuer == cert[1]:
        sys.exit(1)

def test_single_domain_upload_and_verifcation():
    # Rgister user tester 
    register('tester','tester','tester')
    login('tester','tester')
    single_upload(config['single-domain'])
    verfiy_results(config['single-domain'])    
   
   
    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    test_single_domain_upload_and_verifcation()