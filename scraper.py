import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

POSITION_TITLE = 'C#'
POSITION_LOCATION = 'Chernivtsi'


def initialize_driver():
    """
    Initialize the WebDriver for Chrome.
    """
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    driver.maximize_window()
    return driver


def close_popups(driver):
    """
    Close google login and cookie popups.
    """
    cookie_popup_selector = "#onetrust-reject-all-handler"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, cookie_popup_selector)
        )
    )
    driver.find_element(
        By.CSS_SELECTOR, cookie_popup_selector
    ).click()

    google_popup_selector = (
        "#google-Only-Modal > div > div.google-Only-Modal-Upper-Row > button"
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, google_popup_selector)
        )
    )
    driver.find_element(
        By.CSS_SELECTOR, google_popup_selector
    ).click()


def get_job_postings(driver):
    """
    Get a list of job postings elements from the page.
    """
    return driver.find_elements(
        By.CSS_SELECTOR,
        '#mosaic-provider-jobcards > ul > li > div.cardOutline'
    )


def scrape_job_details(driver, job):
    """
    Scrape job details from a job posting element.
    """
    action_chains = ActionChains(driver)
    action_chains.scroll_to_element(job).perform()
    job.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'jobsearch-JobComponent')
        )
    )
    job_detail_html = driver.find_element(
        By.CLASS_NAME, 'jobsearch-JobComponent'
    ).get_attribute('innerHTML')
    soup = BeautifulSoup(job_detail_html, 'lxml')
    title = soup.find(class_='jobsearch-JobInfoHeader-title').select_one('span').contents[0]
    company_name = soup.select_one('div[data-company-name="true"]').a.string
    company_link = soup.select_one('div[data-company-name="true"]').a.get('href')
    location = soup.select_one('.css-6z8o9s.eu4oa1w0').div.string
    description = soup.select_one('.jobsearch-jobDescriptionText').get_text()
    return title, company_name, company_link, location, description


def main():
    driver = initialize_driver()
    driver.get("https://www.indeed.com")

    what_field = driver.find_element(By.ID, "text-input-what")
    where_field = driver.find_element(By.ID, "text-input-where")
    search_button = driver.find_element(By.CLASS_NAME,
                                        "yosegi-InlineWhatWhere-primaryButton")
    time.sleep(2)
    what_field.send_keys(POSITION_TITLE)
    where_field.send_keys(POSITION_LOCATION)
    search_button.send_keys(Keys.RETURN)
    close_popups(driver)

    scraped_data = []

    while True:
        try:
            job_postings = get_job_postings(driver)
            print('job postings found', job_postings)
            for job in job_postings:
                (title, company_name, company_link,
                 location, description) = scrape_job_details(driver, job)
                new_row = {
                    'title': f'"{title}"',
                    'company_name': f'"{company_name}"',
                    'company_link': f'"{company_link}"',
                    'location': f'"{location}"',
                    'description': f'"{description}"'
                }
                scraped_data.append(new_row)
                time.sleep(3)  # avoid captcha 

        except NoSuchElementException as e:
            print(e)
            print("No jobs found")
            driver.close()
            break

        try:
            next_button_selector = (
                'a[data-testid="pagination-page-next"][aria-label="Next Page"]'
            )
            driver.find_element(By.CSS_SELECTOR, next_button_selector).click()
        except NoSuchElementException:
            print("No next button")
            driver.close()
            break

    headers = ['title', 'company_name', 'company_link', 'location',
               'description']
    df = pd.DataFrame(scraped_data, columns=headers)
    df.to_csv('data/jobs.csv', index=False, sep=',', encoding='utf-8')


if __name__ == "__main__":
    main()
