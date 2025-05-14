# Automated Greenhouse Job Application Bot

This Python project automates the process of applying to jobs hosted on the Greenhouse job platform. It uses Selenium to interact with job application forms, filling out necessary details, uploading resumes, and logging the result of each application.

---

## 📁 Project Structure

```
project/
├── apply.py
├── locators.json
├── requirements.txt
├── config/
│   ├── answers.csv
│   ├── *.yaml                # User config files (malathi.yaml, etc.)
│   └── linkedin_jobs_date_time.csv
├── logs/
│   └── job_application_*.csv
├── resume/
│   └── *.pdf                 # User resumes (malathi.pdf, etc.)
├── venv/                     # Python virtual environment
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Karimulla79/Greenhouse_Bot.git
cd Greenhouse_Bot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuration

### YAML User Files (`config/*.yaml`)

Each user should have a `.yaml` file inside the `config` folder with details like name, email, etc.

### Resume Files (`resume/*.pdf`)

Make sure each user has a corresponding `.pdf` file in the `resume/` directory.

### Locators

Ensure `locators.json` is present in the **project root** (not inside `config/`). This file contains the CSS/XPath locators for the job application form.

### Job URLs

The `jobs/linkedin_jobs_date_time.csv` should contain job links (Greenhouse platform only is supported).

### QA Pairs

The `config/answers.csv` file maps form questions to automated answers.

---

## 🚀 Running the Script

```bash
python apply.py
```

You will be prompted to choose a user. The script will then apply to all Greenhouse jobs listed in the CSV.

---

## 🧾 Logs

Application logs are stored under the `logs/` folder in CSV format, with timestamps and statuses.

---

## ✅ Features

- Select user by number
- Resume and answer upload
- Field auto-fill with fallbacks
- Smart form locator support
- Retry mechanisms and logging

---

## 🧹 Notes

- Resume file names and user config names **must match**.
- Only Greenhouse jobs are supported currently.

---

## 😄whitebox-learning
