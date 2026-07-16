"""
===========================================================
Project : NaukriBot
Module  : login.py
Author  : Gulshan Singh
Version : 3.0.0
===========================================================
"""

import os
import pickle
import shutil

from pathlib import Path

from config.config import (
    COOKIE_FILE,
    NAUKRI_HOME,
    PROFILE_URL,
)

from src.logger import logger


# ===========================================================
# SAVE COOKIES (PRODUCTION)
# ===========================================================

def save_cookies(driver):
    """
    Save browser cookies safely.
    """

    try:

        cookies = driver.get_cookies()

        if not cookies:

            logger.warning(
                "No Cookies Found."
            )

            return False

        temp_file = Path(
            str(COOKIE_FILE) + ".tmp"
        )

        with open(
            temp_file,
            "wb"
        ) as file:

            pickle.dump(
                cookies,
                file,
                protocol=pickle.HIGHEST_PROTOCOL
            )

        if COOKIE_FILE.exists():

            COOKIE_FILE.unlink()

        temp_file.replace(
            COOKIE_FILE
        )

        logger.info(

            f"Cookies Saved : {len(cookies)}"

        )

        return True

    except Exception as e:

        logger.exception(e)

        return False
# ===========================================================
# DELETE COOKIE
# ===========================================================

def delete_cookie_file():

    try:

        if COOKIE_FILE.exists():

            COOKIE_FILE.unlink()

            logger.warning(

                "Corrupted Cookie Deleted."

            )

    except Exception as e:

        logger.exception(e)

# ===========================================================
# COOKIE HEALTH
# ===========================================================

def cookie_exists():

    if not COOKIE_FILE.exists():

        return False

    if os.path.getsize(COOKIE_FILE) == 0:

        logger.warning(

            "Cookie File Empty."

        )

        delete_cookie_file()

        return False

    return True
# ===========================================================
# LOAD COOKIES (PRODUCTION)
# ===========================================================

def load_cookies(driver):
    """
    Load cookies safely.
    """

    try:

        if not cookie_exists():

            logger.warning(
                "Cookie File Not Available."
            )

            return False

        driver.get(NAUKRI_HOME)

        with open(
            COOKIE_FILE,
            "rb"
        ) as file:

            try:

                cookies = pickle.load(file)

            except (
                EOFError,
                pickle.UnpicklingError
            ):

                logger.warning(
                    "Corrupted Cookie File."
                )

                delete_cookie_file()

                return False

        if not cookies:

            logger.warning(
                "Cookie List Empty."
            )

            delete_cookie_file()

            return False

        loaded = 0

        for cookie in cookies:

            try:

                driver.add_cookie(cookie)

                loaded += 1

            except Exception:

                continue

        driver.refresh()

        logger.info(
            f"Loaded {loaded} Cookies."
        )

        return loaded > 0

    except Exception as e:

        logger.exception(e)

        delete_cookie_file()

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
# ENSURE LOGIN (PRODUCTION)
# ===========================================================

def ensure_login(driver):

    logger.info(
        "Checking Login Session..."
    )

    # ----------------------------------------
    # Try Cookie Login
    # ----------------------------------------

    load_cookies(driver)

    if is_logged_in(driver):

        logger.info(
            "User Already Logged In."
        )

        save_cookies(driver)

        return True

    logger.warning(
        "Cookie Login Failed."
    )

    delete_cookie_file()

    # ----------------------------------------
    # Manual Login
    # ----------------------------------------

    driver.get(NAUKRI_HOME)

    print()

    input(
        "Login to Naukri then press ENTER..."
    )

    if not is_logged_in(driver):

        logger.error(
            "Login Failed."
        )

        return False

    save_cookies(driver)

    logger.info(
        "Login Successful."
    )

    return True

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