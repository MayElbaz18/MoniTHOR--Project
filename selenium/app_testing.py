import datetime
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
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
    
def alert_wait_and_click():
        while is_alert_present()==False: 
            time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()

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
    alert_wait_and_click()



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
    alert_wait_and_click()
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
    

def test_file_upload():
    register('tester','tester','tester')    
    login('tester','tester')    
    file_input = driver.find_element("id", "bulk")
    file_path = os.path.abspath('./Domains_for_upload.txt')
    
    file_input.send_keys(file_path)
    
   
    
    upload_button = driver.find_element("class name", "bulk-submit") 
    time.sleep(1)
    upload_button.click()
    time.sleep(1)
    
    alert_wait_and_click()
    alert_wait_and_click()

    time.sleep(15)

    
    

def remove_all_doamins():
    # # Locate the list group by its id attribute

    # list_group = driver.find_element("id", "domains")

    # # Find all list items (li elements) within the list group
    # list_items = list_group.find_elements("class name", "list-group-item")

    # # Iterate through the list items and click the close button in each one
    # for item in list_items:
    #     #domain_name = item.text.split("\n")[0]  # Extract the domain name text
    #     #print(f"Closing domain: {domain_name}")
    #     close_button = item.find_element("class name", "close")
    #     close_button.click()        
    #     alert_wait_and_click()
    #     print("**")
    #     time.sleep(10)

        
# Locate the list group by its id attribute

#def remove_all_domains():
    list_group = driver.find_element("id", "domains")
    while True:
        try:
            # Find all list items (li elements) within the list group
            list_items = list_group.find_elements("class name", "list-group-item")
            
            if not list_items:
                break

            for item in list_items:
                try:
                    domain_name = item.text.split("\n")[0]  # Extract the domain name text
                    print(f"Closing domain: {domain_name}")

                    # Re-locate the close button each time to avoid stale element reference
                    close_button = item.find_element("class name", "close")
                    close_button.click()
                    alert_wait_and_click()
                    
                    # Wait a little for the DOM to update after removing an item
                    time.sleep(1)

                except StaleElementReferenceException:
                    print("StaleElementReferenceException caught! Re-locating elements.")
                    break  # Exit the loop to re-locate all elements

        except StaleElementReferenceException:
            print("Outer StaleElementReferenceException caught! Re-locating the list group and items.")
            list_group = driver.find_element("id", "domains")
            continue  # Re-locate the list group and re-enter the loop
    


   
# Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    test_single_domain_upload_and_verifcation()
    test_file_upload()  
    remove_all_doamins()