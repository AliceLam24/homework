import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

service_obj = Service('./chromedriver')
driver = webdriver.Chrome(service=service_obj)

try:
    # Navigate to the URL
    url = "https://www.ctgoodjobs.hk/"
    driver.get(url)

    # Locate the search keyword input and type "admin"
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-keyword-m"))
    )
    search_input.send_keys("admin")

    # Click the search button using the updated XPath
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='btn-txt']"))
    )
    search_button.click()

    # Click the "More Options" button using the updated XPath
    more_options_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='more-opt']"))
    )
    more_options_button.click()

    # Click the "All Employment" dropdown using the updated CSS selector and select "Full Time" using the updated XPath
    employment_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-msg-default='All Employment Terms']"))
    )
    employment_dropdown.click()
    full_time_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Full-time')]"))
    )
    full_time_option.click()

    # Click the "All Career Level" dropdown using the updated CSS selector and select "Entry Level" using the updated XPath
    career_level_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-msg-default='All Career Levels']"))
    )
    career_level_dropdown.click()
    
    # Adding an explicit wait to ensure the dropdown options are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Entry level')]"))
    )
    
    entry_level_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Entry level')]"))
    )
    entry_level_option.click()

    # Click the search button again
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='btn-txt']"))
    )
    search_button.click()

    # Click the "Relevance" label
    relevance_label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Relevance']"))
    )
    relevance_label.click()

    # Wait for the search results to load
    search_results = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section[@class='jl-list jl-prev']"))
    )

    # Loop through the job elements to extract job details, skipping the first one and including the 11th
    for index in range(1, 11): # the first job element is a promoted job ad (irrelevant) --> skip
        job_element_css = f"div[id='mCSB_1_container'] > div:nth-child({index + 1})"
        job_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, job_element_css))
        )
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", job_element)
            driver.execute_script("arguments[0].click();", job_element)
        except StaleElementReferenceException:
            job_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, job_element_css))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", job_element)
            driver.execute_script("arguments[0].click();", job_element)

        print(f"job element {index}")

        # Wait for the job details to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@id='jd-job-title']"))
        )

        # Extract and print the job title, company name, and job details
        job_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@id='jd-job-title']"))
        ).text
        print(f"Job Title: {job_title}")

        company_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='jd-company-name']"))
        ).text
        print(f"Company Name: {company_name}")

        job_details = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='jd-job-body']"))
        ).text
        print(f"Job Details: {job_details}")

        # Add a line separator
        print("----")

finally:
    # Wait for 3 seconds before closing the WebDriver
    time.sleep(3)
    driver.quit()