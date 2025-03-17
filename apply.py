
# # # # # K:\GreenHouse_Bot\apply.py
# # # # import os
# # # # import time
# # # # import random
# # # # import csv
# # # # from selenium import webdriver
# # # # from selenium.webdriver.common.by import By
# # # # from selenium.webdriver.chrome.service import Service
# # # # from selenium.webdriver.support.ui import WebDriverWait
# # # # from selenium.webdriver.support import expected_conditions as EC
# # # # from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
# # # # from webdriver_manager.chrome import ChromeDriverManager

# # # # # # Load job URLs from a text file
# # # # # def load_job_urls(filename="jobs\linkedin_jobs_date_time.csv"):
# # # # #     with open(filename, "r") as file:
# # # # #         return [line.strip() for line in file.readlines() if line.strip()]

# # # # # Function to construct job URLs from CSV file
# # # # def load_job_urls(filename="jobs/linkedin_jobs_date_time.csv"):
# # # #     job_urls = []

# # # #     # Check if file exists before reading
# # # #     if not os.path.exists(filename):
# # # #         print(f" Error: The file '{filename}' was not found.")
# # # #         return []

# # # #     with open(filename, "r", encoding="utf-8") as file:
# # # #         reader = csv.reader(file)
# # # #         next(reader, None)  # Skip header row if present

# # # #         for row in reader:
# # # #             if len(row) >= 4:  
# # # #                 company = row[2].strip().replace(" ", "").lower()  
# # # #                 job_id = row[3].strip()
# # # #                 job_url = f"https://boards.greenhouse.io/{company}/jobs/{job_id}"
# # # #                 job_urls.append(job_url)

# # # #     return job_urls

# # # # # Random sleep function
# # # # def random_sleep(min_time=2, max_time=8):
# # # #     sleep_time = random.uniform(min_time, max_time)
# # # #     print(f" Sleeping for {round(sleep_time, 2)} seconds...")
# # # #     time.sleep(sleep_time)

# # # # # Job application details
# # # # JOB_APP = {
# # # #     "first_name": "Foo",
# # # #     "last_name": "Bar",
# # # #     "email": "pkarimulla9@gmail.com",
# # # #     "phone": "123-456-7890",
# # # #     "resume": os.path.abspath("resume/resume.pdf"),
# # # #     "linkedin": "https://www.linkedin.com/in/foobar",
# # # #     "location": "San Francisco, CA, USA",
# # # #     "school": "MIT",
# # # #     "degree": "Bachelor's",
# # # #     "work_auth": "Authorized to work for any employer"
# # # # }

# # # # def submit_button_click(driver):
# # # #     """Attempts to click the 'Submit application' button."""
# # # #     try:
# # # #         submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
# # # #         driver.execute_script("arguments[0].scrollIntoView();", submit_button)
# # # #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
# # # #         submit_button.click()
# # # #         print(" 'Submit application' button clicked.")
# # # #     except NoSuchElementException:
# # # #         print(" 'Submit application' button not found. Skipping this job.")
# # # #     except ElementClickInterceptedException:
# # # #         print(" Submit button not clickable immediately, retrying...")
# # # #         driver.execute_script("arguments[0].click();", submit_button)

# # # #     random_sleep()

# # # # def apply_greenhouse(driver, url):
# # # #     print(f"\n🔹 Applying to: {url}")
# # # #     driver.get(url)
# # # #     random_sleep()

# # # #     try:
# # # #         # Click 'Apply' button if available
# # # #         try:
# # # #             apply_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]")
# # # #             apply_button.click()
# # # #             print(" 'Apply' button found and clicked.")
# # # #         except NoSuchElementException:
# # # #             print(" No 'Apply' button found.")

# # # #         random_sleep()

# # # #         # Define fields to fill
# # # #         fields = {
# # # #             "first_name": "first_name",
# # # #             "last_name": "last_name",
# # # #             "email": "email",
# # # #             "phone": "phone",
# # # #             "linkedin": "linkedin",
# # # #             "location": "job_application_location"
# # # #         }

# # # #         # Fill out known fields
# # # #         for key, field_id in fields.items():
# # # #             try:
# # # #                 field = driver.find_element(By.ID, field_id)
# # # #                 field.clear()
# # # #                 field.send_keys(JOB_APP[key])
# # # #                 print(f" {key} filled.")
# # # #             except NoSuchElementException:
# # # #                 print(f" {key} field not found. It might be optional.")

# # # #         random_sleep()
        

# # # #         # Upload Resume Automatically
# # # #         try:
# # # #             resume_input = driver.find_element(By.XPATH, "//input[@type='file']")
# # # #             driver.execute_script("arguments[0].scrollIntoView();", resume_input)
# # # #             resume_input.send_keys(JOB_APP["resume"])
# # # #             print(" Resume uploaded automatically.")
# # # #         except NoSuchElementException:
# # # #             print(" Resume upload field not found. Skipping resume upload.")

# # # #         random_sleep()

# # # #         #  **OTP Handling - Added Here**
# # # #         otp_fields = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'security-input-')]")
# # # #         if otp_fields:
# # # #             print(" OTP verification detected. Fetching OTP...")
# # # #             otp_code = fetch_latest_otp(JOB_APP["email"], JOB_APP["email_password"], JOB_APP["imap_server"])
# # # #             if otp_code:
# # # #                 enter_otp(driver, otp_code)

# # # #         # Wait for manual input if required fields are missing
# # # #         wait_time = 0
# # # #         while True:
# # # #             try:
# # # #                 print("error code is getting called ------------------------------------")
# # # #                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# # # #                 time.sleep(2)
# # # #                 submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
# # # #                 driver.execute_script("arguments[0].scrollIntoView();", submit_button)
# # # #                 WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
# # # #                 submit_button.click()
# # # #                 try:
# # # #                     submit_button.click()
# # # #                 except Exception:
# # # #                     driver.execute_script("arguments[0].click();", submit_button)
# # # #                 print("--------------------iam waiting 8 sec-0-----------------------")
# # # #                 time.sleep(8)

# # # #                 error_elements = driver.find_elements(By.CLASS_NAME, "helper-text--error")
# # # #                 print(error_elements )
# # # #                 if not error_elements:
# # # #                     print(" All required fields filled. Proceeding with submission.")
# # # #                     break  # Exit loop when no errors found

# # # #                 if wait_time == 0:
# # # #                     print("\n Some required fields are missing! Please fill them manually.")

# # # #                 random_sleep(15, 30)  
# # # #                 wait_time += 20

# # # #                 if wait_time >= 60:  
# # # #                     print(f" Waiting... {wait_time} seconds elapsed. Fill the missing details.")

# # # #             except Exception as e:
# # # #                 print(f" Error checking required fields: {e}")

# # # #         # Click the 'Submit application' button
# # # #         submit_button_click(driver)

# # # #     except Exception as e:
# # # #         print(f" Error while submitting: {e}")


# # # # if __name__ == "__main__":
# # # #     job_urls = load_job_urls()
# # # #     print(f"\n Found {len(job_urls)} job(s) to apply for.\n")

# # # #     for index, job_url in enumerate(job_urls, start=1):
# # # #         print(f"\n🔹 Applying for job {index}/{len(job_urls)}: {job_url}")

# # # #         # Start a new browser session for each application
# # # #         service = Service(ChromeDriverManager().install())
# # # #         driver = webdriver.Chrome(service=service)

# # # #         try:
# # # #             apply_greenhouse(driver, job_url)
# # # #             print(" Application submitted successfully.")
# # # #         except Exception as e:
# # # #             print(f" Error while applying for {job_url}: {e}")

# # # #         driver.quit()  # Close browser before moving to the next job
# # # #         print(" Waiting before next application...\n")
# # # #         random_sleep()

# # # #     print(" All applications completed!")

# # # # -------------------------------------------------------------------------------------------------------------


# # K:\GreenHouse_Bot\apply.py
# import os
# import time
# import random
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys


# # Function to construct job URLs from CSV file
# def load_job_urls(filename="jobs/linkedin_jobs_date_time.csv"):
#     job_urls = []

#     # Check if file exists before reading
#     if not os.path.exists(filename):
#         print(f" Error: The file '{filename}' was not found.")
#         return []

#     with open(filename, "r", encoding="utf-8") as file:
#         reader = csv.reader(file)
#         next(reader, None)  

#         for row in reader:
#             if len(row) >= 4 and row[1].strip().lower() == "greenhouse":  
#                 company = row[2].strip().replace(" ", "").lower()  
#                 job_id = row[3].strip()
#                 job_url = f"https://boards.greenhouse.io/{company}/jobs/{job_id}"
#                 job_urls.append(job_url)

#     return job_urls

# # Random sleep function
# def random_sleep(min_time=2, max_time=8):
#     sleep_time = random.uniform(min_time, max_time)
#     print(f" Sleeping for {round(sleep_time, 2)} seconds")
#     time.sleep(sleep_time)

# # Job application details
# JOB_APP = {
#     "first_name": "Foo",
#     "last_name": "Bar",
#     "email": "pkarimulla9@gmail.com",
#     "phone": "123-456-7890",
#     "resume": os.path.abspath("resume/resume.pdf"),
#     "linkedin": "https://www.linkedin.com/in/foobar",
#     "location": "San Francisco, CA, USA",
#     "school": "MIT",
#     "degree": "Bachelor's",
#     "work_auth": "Authorized to work for any employer"
# }

# def submit_button_click(driver):
#     """Attempts to click the 'Submit application' button."""
#     try:
#         submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
#         driver.execute_script("arguments[0].scrollIntoView();", submit_button)
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
#         submit_button.click()
#         print(" 'Submit application' button clicked.")
#     except NoSuchElementException:
#         print(" 'Submit application' button not found. Skipping this job.")
#     except ElementClickInterceptedException:
#         print(" Submit button not clickable immediately, retrying...")
#         driver.execute_script("arguments[0].click();", submit_button)

#     random_sleep()

# def apply_greenhouse(driver, url):
#     print(f"\n🔹 Applying to: {url}")
#     driver.get(url)
#     random_sleep()

#     try:
#         # Click 'Apply' button if available
#         try:
#             apply_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]")
#             apply_button.click()
#             print(" 'Apply' button found and clicked.")
#         except NoSuchElementException:
#             print(" No 'Apply' button found.")

#         random_sleep()

#         # Define fields to fill
#         fields = {
#             "first_name": "first_name",
#             "last_name": "last_name",
#             "email": "email",
#             "phone": "phone",
#             "linkedin": "linkedin",
#             "location": "job_application_location"
#         }

#         # Fill out known fields
#         for key, field_id in fields.items():
#             try:
#                 field = driver.find_element(By.ID, field_id)
#                 field.clear()
#                 field.send_keys(JOB_APP[key])
#                 print(f" {key} filled.")
#             except NoSuchElementException:
#                 print(f" {key} field not found. It might be optional.")

#         random_sleep()

#         # **Handle Location Field with Dropdown**
#         try:
#             location_input = driver.find_element(By.ID, "candidate-location")
#             location_input.clear()
#             location_input.send_keys(JOB_APP["location"])
#             time.sleep(2)  
            
#             # Press Arrow Down and Enter to select the first suggestion
#             location_input.send_keys(Keys.ARROW_DOWN)
#             location_input.send_keys(Keys.RETURN)

#             print(f" Location set to {JOB_APP['location']} (dropdown selected)")
#         except NoSuchElementException:
#             print(" Location input field not found. It might be optional.")

#         random_sleep()

#         # Upload Resume Automatically
#         try:
#             resume_input = driver.find_element(By.XPATH, "//input[@type='file']")
#             driver.execute_script("arguments[0].scrollIntoView();", resume_input)
#             resume_input.send_keys(JOB_APP["resume"])
#             print(" Resume uploaded automatically.")
#         except NoSuchElementException:
#             print(" Resume upload field not found. Skipping resume upload.")

#         random_sleep()

#         #  **OTP Handling - Added Here**
#         otp_fields = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'security-input-')]")
#         if otp_fields:
#             print(" OTP verification detected. Fetching OTP...")
#             otp_code = fetch_latest_otp(JOB_APP["email"], JOB_APP["email_password"], JOB_APP["imap_server"])
#             if otp_code:
#                 enter_otp(driver, otp_code)

#         # Wait for manual input if required fields are missing
#         wait_time = 0
#         while True:
#             try:
#                 print("error code is getting called ------------------------------------")
#                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(2)
#                 submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
#                 driver.execute_script("arguments[0].scrollIntoView();", submit_button)
#                 WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
#                 submit_button.click()
#                 try:
#                     submit_button.click()
#                 except Exception:
#                     driver.execute_script("arguments[0].click();", submit_button)
#                 print("--------------------iam waiting 8 sec-0-----------------------")
#                 time.sleep(8)

#                 error_elements = driver.find_elements(By.CLASS_NAME, "helper-text--error")
#                 print(error_elements )
#                 if not error_elements:
#                     print(" All required fields filled. Proceeding with submission.")
#                     break  

#                 if wait_time == 0:
#                     print("\n Some required fields are missing! Please fill them manually.")

#                 random_sleep(15, 30)  
#                 wait_time += 20

#                 if wait_time >= 60:  
#                     print(f" Waiting... {wait_time} seconds elapsed. Fill the missing details.")

#             except Exception as e:
#                 print(f" Error checking required fields: {e}")

#         # Click the 'Submit application' button
#         submit_button_click(driver)

#     except Exception as e:
#         print(f" Error while submitting: {e}")

# if __name__ == "__main__":
#     job_urls = load_job_urls()
#     print(f"\n Found {len(job_urls)} job(s) to apply for.\n")

#     for index, job_url in enumerate(job_urls, start=1):
#         print(f"\n🔹 Applying for job {index}/{len(job_urls)}: {job_url}")

#         # Start a new browser session for each application
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service)

#         try:
#             apply_greenhouse(driver, job_url)
#             print(" Application submitted successfully.")
#         except Exception as e:
#             print(f" Error while applying for {job_url}: {e}")

#         # Close browser before moving to the next job
#         driver.quit()  
#         print(" Waiting before next application...\n")
#         random_sleep()

#     print(" All applications completed!")






# ---------------------------------------------------------------------- 12-3-2025 i updated belwo code -----------------




# # K:\GreenHouse_Bot\apply.py
# import os
# import time
# import random
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys


# # Function to construct job URLs from CSV file
# def load_job_urls(filename="jobs/linkedin_jobs_date_time.csv"):
#     job_urls = []

#     # Check if file exists before reading
#     if not os.path.exists(filename):
#         print(f" Error: The file '{filename}' was not found.")
#         return []

#     with open(filename, "r", encoding="utf-8") as file:
#         reader = csv.reader(file)
#         next(reader, None)  

#         for row in reader:
#             if len(row) >= 4 and row[1].strip().lower() == "greenhouse":  
#                 company = row[2].strip().replace(" ", "").lower()  
#                 job_id = row[3].strip()
#                 job_url = f"https://boards.greenhouse.io/{company}/jobs/{job_id}"
#                 job_urls.append(job_url)

#     return job_urls

# # Random sleep function
# def random_sleep(min_time=2, max_time=8):
#     sleep_time = random.uniform(min_time, max_time)
#     print(f" Sleeping for {round(sleep_time, 2)} seconds")
#     time.sleep(sleep_time)

# # Job application details
# JOB_APP = {
#     "first_name": "Foo",
#     "last_name": "Bar",
#     "email": "pkarimulla9@gmail.com",
#     "phone": "123-456-7890",
#     "resume": os.path.abspath("resume/resume.pdf"),
#     "linkedin": "https://www.linkedin.com/in/foobar",
#     "location": "San Francisco, CA, USA",
#     "school": "MIT",
#     "degree": "Bachelor's",
#     "work_auth": "Authorized to work for any employer"
# }

# # def submit_button_click(driver):
# #     """Attempts to click the 'Submit application' button."""
# #     try:
# #         submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
# #         driver.execute_script("arguments[0].scrollIntoView();", submit_button)
# #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
# #         submit_button.click()
# #         print(" 'Submit application' button clicked.")
# #     except NoSuchElementException:
# #         print(" 'Submit application' button not found. Skipping this job.")
# #     except ElementClickInterceptedException:
# #         print(" Submit button not clickable immediately, retrying...")
# #         driver.execute_script("arguments[0].click();", submit_button)

# #     random_sleep()


# # def submit_button_click(driver):
# #     """Attempts to click the 'Submit application' button using multiple selectors."""
# #     submit_button_selectors = [
# #         "//button[contains(text(), 'Submit application')]",
# #         "//input[@id='submit_app']"  # New selector provided by user
# #     ]

# #     for selector in submit_button_selectors:
# #         try:
# #             submit_button = driver.find_element(By.XPATH, selector)
# #             driver.execute_script("arguments[0].scrollIntoView();", submit_button)
# #             WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
# #             submit_button.click()
# #             print(f" 'Submit application' button clicked using selector: {selector}")
# #             random_sleep()
# #             return
# #         except NoSuchElementException:
# #             continue  # Try the next selector
# #         except ElementClickInterceptedException:
# #             print(f" Submit button not clickable immediately, retrying with script for selector: {selector}")
# #             driver.execute_script("arguments[0].click();", submit_button)
# #             random_sleep()
# #             return

# #     print(" 'Submit application' button not found. Skipping this job.")

# def apply_greenhouse(driver, url):
#     print(f"\n🔹 Applying to: {url}")
#     driver.get(url)
#     random_sleep()

#     try:
#         # Possible 'Apply' button selectors
#         apply_button_selectors = [
#             "//button[contains(text(), 'Apply')]",
#             "//button[contains(text(), 'Apply Now')]",
#             "//a[@id='apply_button']"  # Added selector for the 'Apply Now' button
#         ]

#         # Click 'Apply' button if available
#         apply_button_clicked = False
#         for selector in apply_button_selectors:
#             try:
#                 apply_button = driver.find_element(By.XPATH, selector)
#                 apply_button.click()
#                 print(f" 'Apply' button found and clicked using selector: {selector}")
#                 apply_button_clicked = True
#                 break  
#             except NoSuchElementException:
#                 continue  

#         if not apply_button_clicked:
#             print(" No 'Apply' button found.")

#         random_sleep()

#         # Define fields to fill
#         fields = {
#             "first_name": "first_name",
#             "last_name": "last_name",
#             "email": "email",
#             "phone": "phone",
#             "linkedin": "linkedin",
#             "location": "job_application_location"
#         }

#         # Fill out known fields
#         for key, field_id in fields.items():
#             try:
#                 field = driver.find_element(By.ID, field_id)
#                 field.clear()
#                 field.send_keys(JOB_APP[key])
#                 print(f" {key} filled.")
#             except NoSuchElementException:
#                 print(f" {key} field not found. It might be optional.")

#         random_sleep()

#         # **Handle Location Field with Dropdown**
#         try:
#             location_input = driver.find_element(By.ID, "candidate-location")
#             location_input.clear()
#             location_input.send_keys(JOB_APP["location"])
#             time.sleep(2)  
            
#             # Press Arrow Down and Enter to select the first suggestion
#             location_input.send_keys(Keys.ARROW_DOWN)
#             location_input.send_keys(Keys.RETURN)

#             print(f" Location set to {JOB_APP['location']} (dropdown selected)")
#         except NoSuchElementException:
#             print(" Location input field not found. It might be optional.")

#         random_sleep()

#         # Upload Resume Automatically
#         try:
#             resume_input = driver.find_element(By.XPATH, "//input[@type='file']")
#             driver.execute_script("arguments[0].scrollIntoView();", resume_input)
#             resume_input.send_keys(JOB_APP["resume"])
#             print(" Resume uploaded automatically.")
#         except NoSuchElementException:
#             print(" Resume upload field not found. Skipping resume upload.")

#         random_sleep()

#         #  **OTP Handling - Added Here**
#         otp_fields = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'security-input-')]")
#         if otp_fields:
#             print(" OTP verification detected. Fetching OTP...")
#             otp_code = fetch_latest_otp(JOB_APP["email"], JOB_APP["email_password"], JOB_APP["imap_server"])
#             if otp_code:
#                 enter_otp(driver, otp_code)

#         # Wait for manual input if required fields are missing
#         wait_time = 0
#         while True:
#             try:
#                 print("error code is getting called ------------------------------------")
#                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(2)
#                 submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
#                 driver.execute_script("arguments[0].scrollIntoView();", submit_button)
#                 WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
#                 submit_button.click()
#                 try:
#                     submit_button.click()
#                 except Exception:
#                     driver.execute_script("arguments[0].click();", submit_button)
#                 print("--------------------iam waiting 8 sec-0-----------------------")
#                 time.sleep(8)

#                 error_elements = driver.find_elements(By.CLASS_NAME, "helper-text--error")
#                 print(error_elements )
#                 if not error_elements:
#                     print(" All required fields filled. Proceeding with submission.")
#                     break  

#                 if wait_time == 0:
#                     print("\n Some required fields are missing! Please fill them manually.")

#                 random_sleep(15, 30)  
#                 wait_time += 20

#                 if wait_time >= 60:  
#                     print(f" Waiting... {wait_time} seconds elapsed. Fill the missing details.")

#             except Exception as e:
#                 print(f" Error checking required fields: {e}")

#         # Click the 'Submit application' button
#         # submit_button_click(driver)

#     except Exception as e:
#         print(f" Error while submitting: {e}")

# if __name__ == "__main__":
#     job_urls = load_job_urls()
#     print(f"\n Found {len(job_urls)} job(s) to apply for.\n")

#     for index, job_url in enumerate(job_urls, start=1):
#         print(f"\n🔹 Applying for job {index}/{len(job_urls)}: {job_url}")

#         # Start a new browser session for each application
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service)

#         try:
#             apply_greenhouse(driver, job_url)
#             print(" Application submitted successfully.")
#         except Exception as e:
#             print(f" Error while applying for {job_url}: {e}")

#         # Close browser before moving to the next job
#         driver.quit()  
#         print(" Waiting before next application...\n")
#         random_sleep()

#     print(" All applications completed!")


# K:\GreenHouse_Bot\apply.py


# working ************************************
# import os
# import time
# import random
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys


# # Function to construct job URLs from CSV file
# def load_job_urls(filename="jobs/linkedin_jobs_date_time.csv"):
#     job_urls = []

#     # Check if file exists before reading
#     if not os.path.exists(filename):
#         print(f" Error: The file '{filename}' was not found.")
#         return []

#     with open(filename, "r", encoding="utf-8") as file:
#         reader = csv.reader(file)
#         next(reader, None)  

#         for row in reader:
#             if len(row) >= 4 and row[1].strip().lower() == "greenhouse":  
#                 company = row[2].strip().replace(" ", "").lower()  
#                 job_id = row[3].strip()
#                 job_url = f"https://boards.greenhouse.io/{company}/jobs/{job_id}"
#                 job_urls.append(job_url)

#     return job_urls

# # Random sleep function
# def random_sleep(min_time=2, max_time=8):
#     sleep_time = random.uniform(min_time, max_time)
#     print(f" Sleeping for {round(sleep_time, 2)} seconds")
#     time.sleep(sleep_time)

# # Job application details
# JOB_APP = {
#     "first_name": "Foo",
#     "last_name": "Bar",
#     "email": "pkarimulla9@gmail.com",
#     "phone": "123-456-7890",
#     "resume": os.path.abspath("resume/resume.pdf"),
#     "linkedin": "https://www.linkedin.com/in/foobar",
#     "location": "San Francisco, CA, USA",
#     "school": "MIT",
#     "degree": "Bachelor's",
#     "work_auth": "Authorized to work for any employer"
# }

# def apply_greenhouse(driver, url):
#     print(f"\n🔹 Applying to: {url}")
#     driver.get(url)
#     random_sleep()

#     try:
#         # Possible 'Apply' button selectors
#         apply_button_selectors = [
#             "//button[contains(text(), 'Apply')]",
#             "//button[contains(text(), 'Apply Now')]",
#             "//a[@id='apply_button']"
#         ]

#         # Click 'Apply' button if available
#         apply_button_clicked = False
#         for selector in apply_button_selectors:
#             try:
#                 apply_button = driver.find_element(By.XPATH, selector)
#                 apply_button.click()
#                 print(f" 'Apply' button found and clicked using selector: {selector}")
#                 apply_button_clicked = True
#                 break  
#             except NoSuchElementException:
#                 continue  

#         if not apply_button_clicked:
#             print(" No 'Apply' button found.")

#         random_sleep()

#         # Define fields to fill
#         fields = {
#             "first_name": "first_name",
#             "last_name": "last_name",
#             "email": "email",
#             "phone": "phone",
#             "linkedin": "linkedin",
#             "location": "job_application_location"
#         }

#         # Fill out known fields
#         for key, field_id in fields.items():
#             try:
#                 field = driver.find_element(By.ID, field_id)
#                 field.clear()
#                 field.send_keys(JOB_APP[key])
#                 print(f" {key} filled.")
#             except NoSuchElementException:
#                 print(f" {key} field not found. It might be optional.")

#         random_sleep()

#         # **Handle Location Field with Dropdown**
#         try:
#             location_input = driver.find_element(By.ID, "candidate-location")
#             location_input.clear()
#             location_input.send_keys(JOB_APP["location"])
#             time.sleep(2)  
            
#             # Press Arrow Down and Enter to select the first suggestion
#             location_input.send_keys(Keys.ARROW_DOWN)
#             location_input.send_keys(Keys.RETURN)

#             print(f" Location set to {JOB_APP['location']} (dropdown selected)")
#         except NoSuchElementException:
#             print(" Location input field not found. It might be optional.")

#         random_sleep()

#         # Upload Resume Automatically
#         try:
#             resume_input = driver.find_element(By.XPATH, "//input[@type='file']")
#             driver.execute_script("arguments[0].scrollIntoView();", resume_input)
#             resume_input.send_keys(JOB_APP["resume"])
#             print(" Resume uploaded automatically.")
#         except NoSuchElementException:
#             print(" Resume upload field not found. Skipping resume upload.")

#         random_sleep()

#         # **OTP Handling - Added Here**
#         otp_fields = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'security-input-')]")
#         if otp_fields:
#             print(" OTP verification detected. Fetching OTP...")
#             otp_code = fetch_latest_otp(JOB_APP["email"], JOB_APP["email_password"], JOB_APP["imap_server"])
#             if otp_code:
#                 enter_otp(driver, otp_code)

#         # **Submit Button Handling - Modified Here**
#         submit_button_selectors = [
#             "//button[contains(text(), 'Submit application')]",  
#             "//input[@id='submit_app' and @type='button']"  
#         ]

#         wait_time = 0
#         while True:
#             try:
#                 print(" Scrolling to bottom to find the submit button...")
#                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(2)

#                 submit_button_clicked = False
#                 for selector in submit_button_selectors:
#                     try:
#                         submit_button = driver.find_element(By.XPATH, selector)
#                         driver.execute_script("arguments[0].scrollIntoView();", submit_button)
#                         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
#                         submit_button.click()
#                         print(f" 'Submit' button found and clicked using selector: {selector}")
#                         submit_button_clicked = True
#                         break
#                     except NoSuchElementException:
#                         continue  

#                 if not submit_button_clicked:
#                     print(" No 'Submit' button found.")

#                 print(" Waiting for submission processing...")
#                 time.sleep(8)

#                 error_elements = driver.find_elements(By.CLASS_NAME, "helper-text--error")
#                 if not error_elements:
#                     print(" All required fields filled. Proceeding with submission.")
#                     break  

#                 if wait_time == 0:
#                     print("\n Some required fields are missing! Please fill them manually.")

#                 random_sleep(15, 30)  
#                 wait_time += 20

#                 if wait_time >= 60:  
#                     print(f" Waiting... {wait_time} seconds elapsed. Fill the missing details.")

#             except Exception as e:
#                 print(f" Error checking required fields: {e}")

#     except Exception as e:
#         print(f" Error while submitting: {e}")

# if __name__ == "__main__":
#     job_urls = load_job_urls()
#     print(f"\n Found {len(job_urls)} job(s) to apply for.\n")

#     for index, job_url in enumerate(job_urls, start=1):
#         print(f"\n🔹 Applying for job {index}/{len(job_urls)}: {job_url}")

#         # Start a new browser session for each application
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service)

#         try:
#             apply_greenhouse(driver, job_url)
#             print(" Application submitted successfully.")
#         except Exception as e:
#             print(f" Error while applying for {job_url}: {e}")

#         # Close browser before moving to the next job
#         driver.quit()  
#         print(" Waiting before next application...\n")
#         random_sleep()

#     print(" All applications completed!")



# ******************************************
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
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


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

        # Convert the relative resume path to an absolute path based on script location
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        job_app["resume"] = os.path.abspath(os.path.join(base_dir, job_app["resume"]))

        return job_app 
      
# Load job application details
JOB_APP = load_config()

if not JOB_APP:
    print("Error: Unable to load configuration. Exiting.")
    exit(1)

# Function to construct job URLs from CSV file
def load_job_urls(filename="jobs/linkedin_jobs_date_time.csv"):
    job_urls = []

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) >= 4 and row[1].strip().lower() == "greenhouse":
                company = row[2].strip().replace(" ", "").lower()
                job_id = row[3].strip()
                job_url = f"https://boards.greenhouse.io/{company}/jobs/{job_id}"
                job_urls.append(job_url)

    return job_urls


# Random sleep function
def random_sleep(min_time=2, max_time=8):
    sleep_time = random.uniform(min_time, max_time)
    print(f"Sleeping for {round(sleep_time, 2)} seconds")
    time.sleep(sleep_time)


def apply_greenhouse(driver, url):
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
                apply_button.click()
                print(f"'Apply' button found and clicked using selector: {selector}")
                apply_button_clicked = True
                break
            except NoSuchElementException:
                continue

        if not apply_button_clicked:
            print("No 'Apply' button found.")

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
            print("Location input field not found. It might be optional.")

        random_sleep()

        try:
            resume_input = driver.find_element(By.XPATH, "//input[@type='file']")
            driver.execute_script("arguments[0].scrollIntoView();", resume_input)
            resume_input.send_keys(JOB_APP["resume"])
            print("Resume uploaded automatically.")
        except NoSuchElementException:
            print("Resume upload field not found. Skipping resume upload.")

        random_sleep()

        submit_button_selectors = [
            "//button[contains(text(), 'Submit application')]",
            "//input[@id='submit_app' and @type='button']"
        ]

        wait_time = 0
        while True:
            try:
                print("Scrolling to bottom to find the submit button...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                submit_button_clicked = False
                for selector in submit_button_selectors:
                    try:
                        submit_button = driver.find_element(By.XPATH, selector)
                        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button))
                        submit_button.click()
                        print(f"'Submit' button found and clicked using selector: {selector}")
                        submit_button_clicked = True
                        break
                    except NoSuchElementException:
                        continue

                if not submit_button_clicked:
                    print("No 'Submit' button found.")

                print("Waiting for submission processing...")
                time.sleep(8)

                error_elements = driver.find_elements(By.CLASS_NAME, "helper-text--error")
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

    except Exception as e:
        print(f"Error while submitting: {e}")


if __name__ == "__main__":
    job_urls = load_job_urls()
    print(f"\nFound {len(job_urls)} job(s) to apply for.\n")

    for index, job_url in enumerate(job_urls, start=1):
        print(f"\n🔹 Applying for job {index}/{len(job_urls)}: {job_url}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        try:
            apply_greenhouse(driver, job_url)
            print("Application submitted successfully.")
        except Exception as e:
            print(f"Error while applying for {job_url}: {e}")

        driver.quit()
        print("Waiting before next application...\n")
        random_sleep()

    print("All applications completed!")
