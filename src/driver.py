"""
===========================================================
Project : NaukriBot
Module  : driver.py
Author  : Gulshan Singh
Version : 3.0.0
===========================================================
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.config import (
    PROFILE_DIR,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PAGE_LOAD_TIMEOUT,
    HEADLESS,
    CHROME_OPTIONS,
)

from src.logger import logger


def get_driver():
    """
    Create and return configured Chrome WebDriver.
    """

    logger.info("Creating Chrome Driver...")

    options = webdriver.ChromeOptions()

    # ===========================================================
    # Chrome Profile
    # ===========================================================

    options.add_argument(
        f"--user-data-dir={PROFILE_DIR}"
    )

    # ===========================================================
    # Window Size
    # ===========================================================

    options.add_argument(
        f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}"
    )

    # ===========================================================
    # Chrome Options (from config.py)
    # ===========================================================

    for option in CHROME_OPTIONS:

        options.add_argument(option)

    # ===========================================================
    # EC2 / Docker Compatibility
    # ===========================================================

    options.add_argument("--no-sandbox")

    options.add_argument("--disable-dev-shm-usage")

    # ===========================================================
    # Headless Mode
    # ===========================================================

    if HEADLESS:

        options.add_argument("--headless=new")

    # ===========================================================
    # Create Driver
    # ===========================================================

    driver = webdriver.Chrome(

        service=Service(

            ChromeDriverManager().install()

        ),

        options=options,

    )

    driver.set_page_load_timeout(
        PAGE_LOAD_TIMEOUT
    )

    logger.info(
        "Chrome Driver Started Successfully."
    )

    return driver


def close_driver(driver):
    """
    Safely Close Chrome Driver.
    """

    if driver is None:

        return

    try:

        logger.info("Closing Chrome Driver...")

        driver.quit()

        logger.info("Chrome Closed.")

    except Exception as e:

        logger.exception(e)