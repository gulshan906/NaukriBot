"""
===========================================================
Project : NaukriBot
Module  : login.py
Author  : Gulshan Singh
Version : 3.0.0
===========================================================
"""

import pickle

from config.config import (
    COOKIE_FILE,
    NAUKRI_HOME,
    PROFILE_URL,
)

from src.logger import logger


# ===========================================================
# Save Cookies
# ===========================================================

def save_cookies(driver):
    """
    Save browser cookies.
    """

    try:

        with open(COOKIE_FILE, "wb") as file:

            pickle.dump(
                driver.get_cookies(),
                file
            )

        logger.info("Cookies Saved Successfully.")

        return True

    except Exception as e:

        logger.exception(e)

        return False


# ===========================================================
# Load Cookies
# ===========================================================

def load_cookies(driver):
    """
    Load cookies if available.
    """

    try:

        if not COOKIE_FILE.exists():

            logger.warning(
                "Cookie File Not Found."
            )

            return False

        driver.get(NAUKRI_HOME)

        with open(COOKIE_FILE, "rb") as file:

            cookies = pickle.load(file)

        for cookie in cookies:

            try:

                driver.add_cookie(cookie)

            except Exception:

                continue

        driver.refresh()

        logger.info(
            "Cookies Loaded Successfully."
        )

        return True

    except Exception as e:

        logger.exception(e)

        return False


# ===========================================================
# Check Login
# ===========================================================

def is_logged_in(driver):
    """
    Check whether user is logged in.
    """

    try:

        driver.get(PROFILE_URL)

        return "profile" in driver.current_url.lower()

    except Exception as e:

        logger.exception(e)

        return False


# ===========================================================
# Open Profile
# ===========================================================

def open_profile(driver):
    """
    Open Profile Page.
    """

    driver.get(PROFILE_URL)

    logger.info(
        "Profile Page Opened."
    )


# ===========================================================
# Ensure Login
# ===========================================================

def ensure_login(driver):
    """
    Ensure valid login session.
    """

    logger.info(
        "Checking Login Session..."
    )

    load_cookies(driver)

    if is_logged_in(driver):

        logger.info(
            "User Already Logged In."
        )

        if not COOKIE_FILE.exists():

            save_cookies(driver)

        return True

    logger.warning(
        "Login Required."
    )

    print()

    input(
        "Login to Naukri and press ENTER..."
    )

    save_cookies(driver)

    if is_logged_in(driver):

        logger.info(
            "Login Successful."
        )

        return True

    logger.error(
        "Login Failed."
    )

    return False