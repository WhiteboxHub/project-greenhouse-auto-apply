# Greenhouse Job Application Automation

## Overview
This Python script automates the job application process on Greenhouse using Selenium. It extracts job listings from a file and dynamically fills out application forms, including uploading resumes and handling OTP verification.

## Features
- Reads job URLs from a text file (`job_links.txt`)
- Automatically fills required fields (name, email, phone, location, etc.)
- Uploads a resume
- Handles OTP verification for secure job applications
- Detects missing required fields and prompts for manual input
- Uses randomized sleep intervals to mimic human behavior

## Setup
### 1. Clone the Repository
```bash
git clone https://github.com/Karimulla79/Greenhouse_Bot.git
cd Greenhouse_Bot
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
Ensure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```

### 4. ChromeDriver Setup
The script uses `webdriver-manager` to automatically download and set up the Chrome WebDriver.

## Usage
1. Place your job URLs in a file named `jobs.txt` (one URL per line).
2. Customize your job application details in the `JOB_APP` dictionary inside `apply.py`.
3. Run the script:
   ```bash
   python apply.py
   ```
4. The script will apply to each job sequentially, handling necessary form fields and submitting applications.
5. If OTP verification is required, the script will pause and prompt the user to manually enter the OTP sent to their email before proceeding with the application submission.

## File Structure
```
GreenHouse_Bot/
│-- apply.py         # Main script for job applications
│-- jobs.txt         # List of Greenhouse job application URLs
│-- resume.pdf       # Resume file to be uploaded
│-- requirements.txt # Python dependencies
│-- venv/            # Virtual environment (if created)
│-- README.md        # Project documentation
```

## Notes
- Ensure your resume file (`resume.pdf`) is in the project directory.
- If OTP verification is enabled, ensure you configure email credentials for fetching OTPs.
- The script handles most fields dynamically, but some manual intervention may be required.
- When prompted for OTP input, manually check your email and enter the code in the script to proceed.




---
**Credits: whitebox-learning! 🚀**

