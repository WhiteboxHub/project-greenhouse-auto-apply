

import os
import time
import random
import csv
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import datetime

def load_config(filename="config/credentials.yaml"):
    if not os.path.exists(filename):
        print(f"Error: Config file '{filename}' not found!")
        return None

    with open(filename, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

        if "JOB_APP" not in config:
            print("Error: 'JOB_APP' section missing in config file.")
            return None

        job_app = config["JOB_APP"]

        base_dir = os.path.dirname(os.path.abspath(__file__))
        job_app["resume"] = os.path.abspath(os.path.join(base_dir, job_app["resume"]))

        return job_app

JOB_APP = load_config()

if not JOB_APP:
    print("Error: Unable to load configuration. Exiting.")
    exit(1)

def load_job_urls(filename="jobs/linkedin_jobs_date_time.csv"):
    job_urls = []

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            platform = row["platform"].strip().lower()
            company = row["company"].strip().replace(" ", "").lower()
            job_id = row["job_id"].strip()
            platform_link = row["platform_link"].strip()

            if platform != "greenhouse":
                continue

            job_url = None

            if company and job_id:
                job_url = f"https://boards.greenhouse.io/{company}/jobs/{job_id}"
            elif platform_link:
                job_url = platform_link

            if job_url:
                job_urls.append(job_url)
            else:
                print(f"Skipping job with missing data: {row}")

    return job_urls

def normalize_text(text):
    return text.strip().lower().replace("*", "").replace(".", "")

def load_qa_pairs(filename="config/answers.csv"):
    qa_pairs = {}
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return qa_pairs

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                question = row[0].strip()
                answer = row[1].strip()
                qa_pairs[normalize_text(question)] = answer
    return qa_pairs

PREDEFINED_ANSWERS = load_qa_pairs()

def random_sleep(min_time=2, max_time=8):
    sleep_time = random.uniform(min_time, max_time)
    print(f"Sleeping for {round(sleep_time, 2)} seconds")
    time.sleep(sleep_time)

def log_result_to_csv(filename, url, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, mode='a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([url, status, timestamp])

def initialize_csv(filename):
    with open(filename, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Status", "Timestamp"])

# Ensure the logs directory exists
logs_directory = "logs"
os.makedirs(logs_directory, exist_ok=True)

# Define the path for the results file
results_filename = os.path.join(logs_directory, "job_application_results.csv")

# Initialize the CSV file with headers
initialize_csv(results_filename)

def apply_greenhouse(driver, url, qa_pairs):
    print(f"\n🔹 Applying to: {url}")
    driver.get(url)
    random_sleep()

    try:
        apply_button_selectors = [
            "//button[contains(text(), 'Apply')]",
            "//button[contains(text(), 'Apply Now')]",
            "//a[@id='apply_button']"
        ]

        apply_button_clicked = False
        for selector in apply_button_selectors:
            try:
                apply_button = driver.find_element(By.XPATH, selector)
                driver.execute_script("arguments[0].scrollIntoView();", apply_button)
                apply_button.click()
                print(f"'Apply' button found and clicked using selector: {selector}")
                apply_button_clicked = True
                break
            except (NoSuchElementException, ElementNotInteractableException):
                continue

        if not apply_button_clicked:
            print("No 'Apply' button found. Proceeding with form filling.")

        random_sleep()

        fields = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "phone": "phone",
            "linkedin": "linkedin",
            "location": "job_application_location"
        }

        for key, field_id in fields.items():
            try:
                field = driver.find_element(By.ID, field_id)
                field.clear()
                field.send_keys(JOB_APP[key])
                print(f"{key} filled.")
            except NoSuchElementException:
                print(f"{key} field not found. It might be optional.")

        random_sleep()

        try:
            location_input = driver.find_element(By.ID, "candidate-location")
            location_input.clear()
            location_input.send_keys(JOB_APP["location"])
            time.sleep(2)
            location_input.send_keys(Keys.ARROW_DOWN)
            location_input.send_keys(Keys.RETURN)
            print(f"Location set to {JOB_APP['location']} (dropdown selected)")
        except NoSuchElementException:
            print("Location input field not found. Skipping.")

        random_sleep()

        try:
            resume_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            driver.execute_script("arguments[0].scrollIntoView();", resume_input)
            resume_input.send_keys(JOB_APP["resume"])
            print("Resume uploaded automatically.")
        except NoSuchElementException:
            print("Resume upload field not found. Skipping.")

        random_sleep()

        text_areas = driver.find_elements(By.CSS_SELECTOR, "textarea")
        for text_area in text_areas:
            try:
                label = driver.find_element(By.CSS_SELECTOR, f"label[for='{text_area.get_attribute('id')}']")
                question_text = label.text.strip()
                normalized_question = normalize_text(question_text)
                if normalized_question in qa_pairs:
                    print(f"Filling text area: {question_text}")
                    text_area.send_keys(qa_pairs[normalized_question])
                else:
                    print(f"No answer found for question: {question_text}")
            except NoSuchElementException:
                print("Text area label not found. Skipping.")

        input_fields = driver.find_elements(By.CSS_SELECTOR, "input")
        for field in input_fields:
            try:
                question_text = field.get_attribute("aria-label") or field.get_attribute("autocomplete")
                if question_text:
                    normalized_question = normalize_text(question_text)
                    if normalized_question in qa_pairs:
                        print(f"Filling input field: {question_text}")
                        field.send_keys(qa_pairs[normalized_question])
                    else:
                        print(f"No answer found for input field: {question_text}")
            except NoSuchElementException:
                print("Input field label not found. Skipping.")

        submit_button_selectors = [
            "button[type='submit']",
            "input#submit_app[type='button']",
            "input[type='button'][value='Submit Application']"
        ]

        wait_time = 0
        while True:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                submit_button_clicked = False
                for selector in submit_button_selectors:
                    try:
                        submit_button = driver.find_element(By.CSS_SELECTOR, selector)
                        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
                        submit_button.click()
                        print(f"'Submit' button clicked using selector: {selector}")
                        submit_button_clicked = True
                        break
                    except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                        continue

                if not submit_button_clicked:
                    print("No 'Submit' button found.")

                time.sleep(8)

                error_elements = driver.find_elements(By.CSS_SELECTOR, ".helper-text--error")
                if not error_elements:
                    print("All required fields filled. Proceeding with submission.")
                    break

                if wait_time == 0:
                    print("\nSome required fields are missing! Please fill them manually.")

                random_sleep(15, 30)
                wait_time += 20

                if wait_time >= 60:
                    print(f"Waiting... {wait_time} seconds elapsed. Fill the missing details.")

            except Exception as e:
                print(f"Error checking required fields: {e}")

        # Verify submission
        try:
            WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
            print("Application submitted successfully.")
            log_result_to_csv(results_filename, url, "Success")
        except TimeoutException:
            try:
                confirmation_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Thank you for applying') or contains(text(), 'Application submitted')]")
                if confirmation_message:
                    print("Application submitted successfully based on confirmation message.")
                    log_result_to_csv(results_filename, url, "Success")
                else:
                    print("Application submission failed. Please check the form manually.")
                    log_result_to_csv(results_filename, url, "Failed")
            except NoSuchElementException:
                print("Application submission failed. Please check the form manually.")
                log_result_to_csv(results_filename, url, "Failed")

    except Exception as e:
        print(f"Error while submitting: {e}")
        log_result_to_csv(results_filename, url, "Failed")

if __name__ == "__main__":
    job_urls = load_job_urls()
    qa_pairs = load_qa_pairs()
    print(f"\nFound {len(job_urls)} job(s) to apply for.\n")

    for index, job_url in enumerate(job_urls, start=1):
        print(f"\n Applying for job {index}/{len(job_urls)}: {job_url}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        try:
            apply_greenhouse(driver, job_url, qa_pairs)
        except Exception as e:
            print(f"Error applying to {job_url}: {e}")
            log_result_to_csv(results_filename, job_url, "Failed")

        driver.quit()
        random_sleep()

    print("All applications completed!")
