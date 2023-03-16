from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.indeed.com")
what_field = driver.find_element(By.ID,"text-input-what")
where_field = driver.find_element(By.ID,"text-input-where")
search_button = driver.find_element(By.CLASS_NAME,"yosegi-InlineWhatWhere-primaryButton")
what_field.send_keys("python developer")
where_field.send_keys("Lviv")
search_button.send_keys(Keys.RETURN)
driver.find_element(By.CSS_SELECTOR,("#google-Only-Modal > div > div.google-Only-Modal-Upper-Row > button")).click() # close google login popup
driver.find_element(By.CSS_SELECTOR,("#onetrust-reject-all-handler")).click() # close cookie alert
action_chains = ActionChains(driver)


# print(len(job_postings))

while True:
    count = 0
    try:
        job_postings = driver.find_elements(By.CSS_SELECTOR,'#mosaic-provider-jobcards > ul > li > div.cardOutline')
        print('job postings found')
        for el in job_postings:
            count += 1
            # print(f"Element number {index}")
            action_chains.scroll_to_element(el).perform()
            el.click()
            time.sleep(3)
    except NoSuchElementException:
        print('No jobs found')
        driver.close()
        break
    time.sleep(3)
    try: 
        next_button = driver.find_element(By.CSS_SELECTOR,'a[data-testid="pagination-page-next"][aria-label="Next Page"]')
        next_button.click()
    except NoSuchElementException:
        print("No next button")
        driver.close()
        break


    
time.sleep(2)