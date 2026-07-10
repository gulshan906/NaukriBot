"""
===========================================================
Project : NaukriBot
Module  : utils.py
Author  : Gulshan Singh
Version : 1.0.0
===========================================================
"""

import time
from datetime import datetime
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import (
    SCREENSHOT_DIR,
    ELEMENT_TIMEOUT,
)

from src.logger import logger


# ===========================================================
# Current Date Time
# ===========================================================

def current_time():

    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# ===========================================================
# Sleep
# ===========================================================

def sleep(seconds):

    logger.info(f"Waiting {seconds} seconds...")

    time.sleep(seconds)


# ===========================================================
# Screenshot
# ===========================================================

def take_screenshot(driver, name="screenshot"):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"{name}_{timestamp}.png"

    file_path = SCREENSHOT_DIR / file_name

    driver.save_screenshot(str(file_path))

    logger.info(f"Screenshot Saved : {file_path}")

    return file_path


# ===========================================================
# Wait for Element
# ===========================================================

def wait_element(driver, by, value, timeout=ELEMENT_TIMEOUT):

    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


# ===========================================================
# Safe Click
# ===========================================================

def safe_click(driver, by, value):

    element = wait_element(driver, by, value)

    element.click()

    logger.info(f"Clicked : {value}")

    return element


# ===========================================================
# Safe Send Keys
# ===========================================================

def safe_send_keys(driver, by, value, text):

    element = wait_element(driver, by, value)

    element.clear()

    element.send_keys(text)

    logger.info(f"Text Entered : {value}")

    return element


# ===========================================================
# Create Folder
# ===========================================================

def create_folder(folder):

    Path(folder).mkdir(parents=True, exist_ok=True)

    logger.info(f"Folder Ready : {folder}")


# ===========================================================
# File Exists
# ===========================================================

def file_exists(file_path):

    return Path(file_path).exists()