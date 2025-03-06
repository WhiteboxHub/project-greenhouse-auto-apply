# Greenhouse Job Application Automation

## Overview

This Python script automates the job application process on Greenhouse using Selenium. It extracts job listings from a file and dynamically fills out application forms, including uploading resumes and handling OTP verification.

## Features

- Reads job URLs from **`jobs\linkedin_jobs_date_time.csv`** for fetching the job URL path
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

## Usage

1. Place your job URLs in the file **`jobs\linkedin_jobs_date_time.csv`** (one URL per line).
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
│-- jobs/            # Directory containing job listings
│   └── linkedin_jobs_date_time.csv  # CSV file with job URLs
│-- resume/          # Directory containing resume files
│   ├── resume.txt   # Resume text file
│   ├── resume.pdf   # Resume PDF file
│   ├── resume.json  # Resume JSON file
│-- requirements.txt # Python dependencies
│-- venv/            # Virtual environment (if created)
│-- README.md        # Project documentation
```

## Notes

- Ensure your resume files (`resume.txt`, `resume.pdf`, `resume.json`) are in the `resume/` directory.
- If OTP verification is enabled, ensure you configure email credentials for fetching OTPs.
- The script handles most fields dynamically, but some manual intervention may be required.
- When prompted for OTP input, manually check your email and enter the code in the script to proceed.

---

**Credits: whitebox-learning! 🚀**
