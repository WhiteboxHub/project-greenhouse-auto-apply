
# K:\GreenHouse_Bot\apply.py
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# Load job URLs from a text file
def load_job_urls(filename="job_links.txt"):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Random sleep function
def random_sleep(min_time=2, max_time=8):
    sleep_time = random.uniform(min_time, max_time)
    print(f"⏳ Sleeping for {round(sleep_time, 2)} seconds...")
    time.sleep(sleep_time)

# Job application details
JOB_APP = {
    "first_name": "Foo",
    "last_name": "Bar",
    "email": "elonmusk@gmail.com",
    "phone": "123-456-7890",
    "resume": os.path.abspath("resume/resume.pdf"),
    "linkedin": "https://www.linkedin.com/in/foobar",
    "location": "San Francisco, CA, USA",
    "school": "MIT",
    "degree": "Bachelor's",
    "work_auth": "Authorized to work for any employer"
}

def submit_button_click(driver):
    """Attempts to click the 'Submit application' button."""
    try:
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
        submit_button.click()
        print("✅ 'Submit application' button clicked.")
    except NoSuchElementException:
        print("❌ 'Submit application' button not found. Skipping this job.")
    except ElementClickInterceptedException:
        print("⚠️ Submit button not clickable immediately, retrying...")
        driver.execute_script("arguments[0].click();", submit_button)

    random_sleep()

def apply_greenhouse(driver, url):
    print(f"\n🔹 Applying to: {url}")
    driver.get(url)
    random_sleep()

    try:
        # Click 'Apply' button if available
        try:
            apply_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]")
            apply_button.click()
            print("✅ 'Apply' button found and clicked.")
        except NoSuchElementException:
            print("❌ No 'Apply' button found.")

        random_sleep()

        # Define fields to fill
        fields = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "phone": "phone",
            "linkedin": "linkedin",
            "location": "job_application_location"
        }

        # Fill out known fields
        for key, field_id in fields.items():
            try:
                field = driver.find_element(By.ID, field_id)
                field.clear()
                field.send_keys(JOB_APP[key])
                print(f"✅ {key} filled.")
            except NoSuchElementException:
                print(f"⚠️ {key} field not found. It might be optional.")

        random_sleep()
        

        # Upload Resume Automatically
        try:
            resume_input = driver.find_element(By.XPATH, "//input[@type='file']")
            driver.execute_script("arguments[0].scrollIntoView();", resume_input)
            resume_input.send_keys(JOB_APP["resume"])
            print("✅ Resume uploaded automatically.")
        except NoSuchElementException:
            print("⚠️ Resume upload field not found. Skipping resume upload.")

        random_sleep()

        # ✅ **OTP Handling - Added Here**
        otp_fields = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'security-input-')]")
        if otp_fields:
            print("🔒 OTP verification detected. Fetching OTP...")
            otp_code = fetch_latest_otp(JOB_APP["email"], JOB_APP["email_password"], JOB_APP["imap_server"])
            if otp_code:
                enter_otp(driver, otp_code)

        # Wait for manual input if required fields are missing
        wait_time = 0
        while True:
            try:
                print("error code is getting called ------------------------------------")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
                driver.execute_script("arguments[0].scrollIntoView();", submit_button)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
                submit_button.click()
                try:
                    submit_button.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", submit_button)
                print("--------------------iam waiting 8 sec-0-----------------------")
                time.sleep(8)

                error_elements = driver.find_elements(By.CLASS_NAME, "helper-text--error")
                print(error_elements )
                if not error_elements:
                    print("✅ All required fields filled. Proceeding with submission.")
                    break  # Exit loop when no errors found

                if wait_time == 0:
                    print("\n🛑 Some required fields are missing! Please fill them manually.")

                random_sleep(15, 30)  # Wait between 15-30 seconds before checking again
                wait_time += 20

                if wait_time >= 60:  # Maximum wait time of 60 seconds
                    print(f"⏳ Waiting... {wait_time} seconds elapsed. Fill the missing details.")

            except Exception as e:
                print(f"⚠️ Error checking required fields: {e}")

        # Click the 'Submit application' button
        submit_button_click(driver)

    except Exception as e:
        print(f"⚠️ Error while submitting: {e}")


if __name__ == "__main__":
    job_urls = load_job_urls()
    print(f"\n✅ Found {len(job_urls)} job(s) to apply for.\n")

    for index, job_url in enumerate(job_urls, start=1):
        print(f"\n🔹 Applying for job {index}/{len(job_urls)}: {job_url}")

        # Start a new browser session for each application
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        try:
            apply_greenhouse(driver, job_url)
            print("✅ Application submitted successfully.")
        except Exception as e:
            print(f"⚠️ Error while applying for {job_url}: {e}")

        driver.quit()  # Close browser before moving to the next job
        print("⏳ Waiting before next application...\n")
        random_sleep()

    print("✅ All applications completed!")

