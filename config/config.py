"""
===========================================================
Project : NaukriBot
Module  : config.py
Author  : Gulshan Singh
Version : 3.0.0
===========================================================
"""

from pathlib import Path
from datetime import datetime
import os

from dotenv import load_dotenv


# ===========================================================
# Base Directory
# ===========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ===========================================================
# Load Environment Variables
# ===========================================================

ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


# ===========================================================
# Project Information
# ===========================================================

PROJECT_NAME = "NaukriBot"

VERSION = "3.0.0"

AUTHOR = "Gulshan Singh"

PROJECT_START_TIME = datetime.now()


# ===========================================================
# Folder Structure
# ===========================================================

CONFIG_DIR = BASE_DIR / "config"

SRC_DIR = BASE_DIR / "src"

LOG_DIR = BASE_DIR / "Logs"

BACKUP_DIR = BASE_DIR / "Backup"

SCREENSHOT_DIR = BASE_DIR / "Screenshots"

TEMP_DIR = BASE_DIR / "Temp"

RESUME_DIR = BASE_DIR / "Resume"

PROFILE_DIR = BASE_DIR / "ChromeProfile"

REPORT_DIR = BASE_DIR / "Reports"

DOWNLOAD_DIR = BASE_DIR / "Downloads"


# ===========================================================
# Auto Create Required Folders
# ===========================================================

for folder in (

    LOG_DIR,

    BACKUP_DIR,

    SCREENSHOT_DIR,

    TEMP_DIR,

    REPORT_DIR,

    DOWNLOAD_DIR,

):

    folder.mkdir(
        parents=True,
        exist_ok=True
    )


# ===========================================================
# Resume Detection
# ===========================================================

SUPPORTED_EXTENSIONS = (

    ".pdf",

    ".doc",

    ".docx",

)

RESUME_PREFIX = os.getenv(
    "RESUME_PREFIX",
    "Gulshan"
)

resume_files = []

for ext in SUPPORTED_EXTENSIONS:

    resume_files.extend(
        RESUME_DIR.glob(
            f"{RESUME_PREFIX}*{ext}"
        )
    )

resume_files = sorted(
    resume_files,
    key=lambda file: file.stat().st_mtime,
    reverse=True
)

RESUME_FILE = resume_files[0] if resume_files else None


# ===========================================================
# Log Files
# ===========================================================

APP_LOG = LOG_DIR / "app.log"

ERROR_LOG = LOG_DIR / "error.log"


# ===========================================================
# Cookie File
# ===========================================================

COOKIE_FILE = BASE_DIR / "naukri_cookies.pkl"


# ===========================================================
# URLs
# ===========================================================

NAUKRI_HOME = "https://www.naukri.com"

PROFILE_URL = "https://www.naukri.com/mnjuser/profile?id=&altresid"


# ===========================================================
# Gmail Configuration
# ===========================================================

GMAIL_USER = os.getenv(
    "GMAIL_USER",
    ""
)

GMAIL_APP_PASSWORD = os.getenv(
    "GMAIL_APP_PASSWORD",
    ""
)

RECIPIENT_EMAIL = os.getenv(
    "RECIPIENT_EMAIL",
    ""
)


# ===========================================================
# Browser Settings
# ===========================================================

SHOW_BROWSER = True

HEADLESS = not SHOW_BROWSER

WINDOW_WIDTH = 1920

WINDOW_HEIGHT = 1080

PAGE_LOAD_TIMEOUT = 60

ELEMENT_TIMEOUT = 30

SHORT_WAIT = 5

LONG_WAIT = 10


# ===========================================================
# Chrome Options
# ===========================================================

CHROME_OPTIONS = [

    "--disable-notifications",

    "--disable-popup-blocking",

    "--start-maximized",

    "--disable-blink-features=AutomationControlled",

    "--disable-infobars",

    "--disable-dev-shm-usage",

    "--disable-gpu",

    "--window-size=1920,1080",

    "--no-first-run",

    "--no-default-browser-check",

]

# ===========================================================
# Retry Settings
# ===========================================================

MAX_RETRY = 3

REFRESH_COUNT = 2


# ===========================================================
# Automation Settings
# ===========================================================

ENABLE_EMAIL = True

ENABLE_SCREENSHOT = True

ENABLE_LOGGER = True

ENABLE_HEALTH_CHECK = True


# ===========================================================
# Naukri Profile Settings
# ===========================================================

KEY_SKILL = "Monitoring"


# ===========================================================
# Weekly Automation Schedule
# ===========================================================

WEEKLY_SCHEDULE = {

    "Monday": "resume_upload",

    "Tuesday": "profile_summary",

    "Wednesday": "keyskills",

    "Thursday": "resume_headline",

    "Friday": "employment",

    "Saturday": "resume_upload",

    "Sunday": None,

}


# ===========================================================
# Scheduler Timing
# ===========================================================

MORNING_RUN = "09:00"

EVENING_RUN = "17:00"


# ===========================================================
# Module Names
# ===========================================================

MODULES = {

    "resume_upload": "Resume Upload",

    "profile_summary": "Profile Summary",

    "keyskills": "Key Skills",

    "resume_headline": "Resume Headline",

    "employment": "Employment",

}


# ===========================================================
# Time Formats
# ===========================================================

DATE_FORMAT = "%d-%m-%Y"

TIME_FORMAT = "%I:%M:%S %p"

DATETIME_FORMAT = "%d-%m-%Y %I:%M:%S %p"


# ===========================================================
# Default Wait
# ===========================================================

DEFAULT_SLEEP = 2


# ===========================================================
# Screenshot Names
# ===========================================================

SCREENSHOT_PREFIX_SUCCESS = "success"

SCREENSHOT_PREFIX_FAILED = "failed"


# ===========================================================
# Mail Subjects
# ===========================================================

MAIL_SUBJECT_SUCCESS = "✅ NaukriBot Automation SUCCESS"

MAIL_SUBJECT_FAILED = "❌ NaukriBot Automation FAILED"


# ===========================================================
# Exit Codes
# ===========================================================

EXIT_SUCCESS = 0

EXIT_FAILED = 1


# ===========================================================
# Debug Information
# ===========================================================

print()

print("=" * 70)

print(f"[CONFIG] Project           : {PROJECT_NAME}")

print(f"[CONFIG] Version           : {VERSION}")

print(f"[CONFIG] Author            : {AUTHOR}")

print(f"[CONFIG] Resume Prefix     : {RESUME_PREFIX}")

if RESUME_FILE:

    print(f"[CONFIG] Resume Selected   : {RESUME_FILE.name}")

else:

    print("[CONFIG] Resume Selected   : NOT FOUND")

print(f"[CONFIG] Browser Visible   : {SHOW_BROWSER}")

print(f"[CONFIG] Headless Mode     : {HEADLESS}")

print(f"[CONFIG] Health Check      : {ENABLE_HEALTH_CHECK}")

print(f"[CONFIG] Email Enabled     : {ENABLE_EMAIL}")

print(f"[CONFIG] Screenshot        : {ENABLE_SCREENSHOT}")

print(f"[CONFIG] Logger            : {ENABLE_LOGGER}")

print(f"[CONFIG] Morning Run       : {MORNING_RUN}")

print(f"[CONFIG] Evening Run       : {EVENING_RUN}")

print("=" * 70)

print()