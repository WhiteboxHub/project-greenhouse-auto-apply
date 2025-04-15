
import os
import glob
import time
import random
import csv
import yaml
import json
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException,
    ElementNotInteractableException, StaleElementReferenceException
)
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def list_users(credentials_dir="config"):
    yaml_files = glob.glob(os.path.join(credentials_dir, "*.yaml"))
    users = [os.path.splitext(os.path.basename(file))[0] for file in yaml_files]
    return users

def load_user_config(username, credentials_dir="config"):
    config_file = os.path.join(credentials_dir, f"{username}.yaml")
    return load_config(config_file)

def load_user_resume(username, resume_dir="resume"):
    resume_file = os.path.join(resume_dir, f"{username}.pdf")
    if not os.path.exists(resume_file):
        print(f"Error: Resume file '{resume_file}' not found for user '{username}'.")
        return None
    return os.path.abspath(resume_file)

def load_config(filename):
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
    return text.strip().lower().replace("*", "").replace(".", "").replace(" ", "")

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

def load_locators(filename="locators.json"):
    if not os.path.exists(filename):
        print(f"Error: Locators file '{filename}' not found!")
        return {}
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

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

def apply_greenhouse(driver, url, qa_pairs, locators):
    print(f"\n🔹 Applying to: {url}")
    driver.get(url)
    random_sleep()

    try:
        apply_button_selectors = locators.get("apply_buttons", [])
        apply_button_clicked = False
        for selector in apply_button_selectors:
            try:
                apply_button = driver.find_element(By.XPATH, selector)
                driver.execute_script("arguments[0].scrollIntoView();", apply_button)
                apply_button.click()
                print(f"'Apply' button clicked using selector: {selector}")
                apply_button_clicked = True
                break
            except (NoSuchElementException, ElementNotInteractableException):
                continue
        if not apply_button_clicked:
            print("No 'Apply' button found. Proceeding with form filling.")
        random_sleep()

        fields = locators.get("fields", {})
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
            location_input = driver.find_element(By.ID, locators.get("location_input", ""))
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
            resume_input = driver.find_element(By.CSS_SELECTOR, locators.get("resume_input", ""))
            driver.execute_script("arguments[0].scrollIntoView();", resume_input)
            resume_input.send_keys(JOB_APP["resume"])
            print("Resume uploaded.")
        except NoSuchElementException:
            print("Resume upload field not found. Skipping.")

        random_sleep()

        text_areas = driver.find_elements(By.CSS_SELECTOR, locators.get("textareas", "textarea"))
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
                continue

        input_fields = driver.find_elements(By.CSS_SELECTOR, locators.get("input_fields", ""))
        for field in input_fields:
            try:
                aria_label = field.get_attribute("aria-label")
                if not aria_label:
                    continue
                normalized_question = normalize_text(aria_label)
                if normalized_question in qa_pairs:
                    print(f"Filling input field: {aria_label}")
                    field.clear()
                    field.send_keys(qa_pairs[normalized_question])
                else:
                    print(f"No answer found for input field: {aria_label}")
            except Exception as e:
                print(f"Error filling input field: {e}")

        submit_button_selectors = locators.get("submit_buttons", [])
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
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                        submit_button.click()
                        print(f"'Submit' button clicked using selector: {selector}")
                        submit_button_clicked = True
                        break
                    except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                        continue
                if not submit_button_clicked:
                    print("No 'Submit' button found.")
                time.sleep(8)
                error_elements = driver.find_elements(By.CSS_SELECTOR, locators.get("error_messages", ""))
                if not error_elements:
                    print("All required fields filled. Proceeding with submission.")
                    break
                if wait_time == 0:
                    print("\nSome required fields are missing! Please fill them manually.")
                random_sleep(15, 30)
                wait_time += 20
                if wait_time >= 60:
                    print(f"Waiting... {wait_time} seconds elapsed.")
            except Exception as e:
                print(f"Error checking required fields: {e}")

        try:
            WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
            print("Application submitted successfully.")
            log_result_to_csv(results_filename, url, "Success")
        except TimeoutException:
            try:
                confirmation_xpath = locators.get("confirmation_xpath", "")
                confirmation_message = driver.find_element(By.XPATH, confirmation_xpath)
                if confirmation_message:
                    print("Application submitted (confirmation message found).")
                    log_result_to_csv(results_filename, url, "Success")
            except NoSuchElementException:
                print("Submission failed.")
                log_result_to_csv(results_filename, url, "Failed")

    except Exception as e:
        print(f"Error while submitting: {e}")
        log_result_to_csv(results_filename, url, "Failed")

if __name__ == "__main__":
    users = list_users()
    user_mapping = {str(i+1): user for i, user in enumerate(users)}
    print("Available users:", ", ".join([f"{num}-{user}" for num, user in user_mapping.items()]))

    selected_number = input("Select a user by number: ").strip()
    if selected_number not in user_mapping:
        print(f"Error: User number '{selected_number}' not found.")
        exit(1)

    selected_user = user_mapping[selected_number]
    JOB_APP = load_user_config(selected_user)
    if not JOB_APP:
        exit(1)

    resume_path = load_user_resume(selected_user)
    if not resume_path:
        exit(1)
    JOB_APP["resume"] = resume_path

    logs_directory = "logs"
    os.makedirs(logs_directory, exist_ok=True)
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    results_filename = os.path.join(logs_directory, f"job_application_{selected_user}_{today_date}.csv")
    initialize_csv(results_filename)

    job_urls = load_job_urls()
    qa_pairs = load_qa_pairs()
    locators = load_locators()
    print(f"\nFound {len(job_urls)} job(s) to apply for.\n")

    for index, job_url in enumerate(job_urls, start=1):
        print(f"\nApplying for job {index}/{len(job_urls)}: {job_url}")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        try:
            apply_greenhouse(driver, job_url, qa_pairs, locators)
        except Exception as e:
            print(f"Error applying to {job_url}: {e}")
            log_result_to_csv(results_filename, job_url, "Failed")
        driver.quit()
        random_sleep()

    print("All applications completed!")
