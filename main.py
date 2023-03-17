from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

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
df = pd.DataFrame(columns=['title','company_name','company_link','location','description'])

while True: #traversing through all job cards in every page and parsing data from each
    try:
        job_postings = driver.find_elements(By.CSS_SELECTOR,'#mosaic-provider-jobcards > ul > li > div.cardOutline')
       
        print('job postings found',job_postings)
        for el in job_postings:
            action_chains.scroll_to_element(el).perform()
            el.click()
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'jobsearch-JobComponent')))
            job_detail_html = driver.find_element(By.CLASS_NAME,'jobsearch-JobComponent').get_attribute('innerHTML')
            soup = BeautifulSoup(job_detail_html,'lxml')
            title = soup.find(class_='jobsearch-JobInfoHeader-title').select_one('span').contents[0]
            company_name = soup.select_one('div[data-company-name="true"]').a.string
            company_link = soup.select_one('div[data-company-name="true"]').a.get('href')
            location = soup.select_one('.css-6z8o9s.eu4oa1w0').div.string
            description = soup.select_one('.jobsearch-jobDescriptionText').get_text()
            #adding extracted data to dataframe
            new_row = {'title':title,'company_name':company_name,'company_link':company_link,'location':location,'description':description}
            new_df = pd.DataFrame([new_row])
            df = pd.concat([df,new_df],ignore_index=True)
            time.sleep(3)#timeout before next click to not get captcha verif
        
    except NoSuchElementException as e:
        print(f'{e} --- No jobs found')
        driver.close()
        break
    try:  #go next page
        next_button = driver.find_element(By.CSS_SELECTOR,'a[data-testid="pagination-page-next"][aria-label="Next Page"]')
        next_button.click()
    except NoSuchElementException:
        print("No next button")
        driver.close()
        break

print(df)
df.to_csv('data/jobs.csv',index=False) # output to csv
