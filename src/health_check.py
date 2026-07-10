"""
===========================================================
Project : NaukriBot
Module  : health_check.py
Author  : Gulshan Singh
Version : 3.0.0
===========================================================
"""

import socket

from config.config import (
    RESUME_FILE,
    PROFILE_DIR,
    COOKIE_FILE,
    GMAIL_USER,
    GMAIL_APP_PASSWORD,
    RECIPIENT_EMAIL,
)

from src.driver import get_driver, close_driver
from src.logger import logger


# ===========================================================
# Display Check Result
# ===========================================================

def check(title, status):

    icon = "PASS" if status else "FAIL"

    print(f"{title:<20} {icon}")

    return status


# ===========================================================
# Internet Check
# ===========================================================

def internet_check():

    try:

        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=5
        )

        logger.info("Internet Check : PASS")

        return True

    except Exception:

        logger.error("Internet Check : FAILED")

        return False


# ===========================================================
# Health Check
# ===========================================================

def health_check():

    logger.info("=" * 60)
    logger.info("Starting Health Check")
    logger.info("=" * 60)

    print("\n" + "=" * 60)
    print("          NAUKRIBOT HEALTH CHECK")
    print("=" * 60)

    results = []

    # -------------------------------------------------------
    # Resume
    # -------------------------------------------------------

    resume_ok = (
        RESUME_FILE is not None
        and RESUME_FILE.exists()
    )

    results.append(
        check("Resume", resume_ok)
    )

    # -------------------------------------------------------
    # Chrome Profile
    # -------------------------------------------------------

    results.append(
        check(
            "Chrome Profile",
            PROFILE_DIR.exists()
        )
    )

    # -------------------------------------------------------
    # Cookies
    # -------------------------------------------------------

    results.append(
        check(
            "Cookies",
            COOKIE_FILE.exists()
        )
    )

    # -------------------------------------------------------
    # Gmail
    # -------------------------------------------------------

    results.append(
        check(
            "Gmail User",
            bool(GMAIL_USER)
        )
    )

    results.append(
        check(
            "App Password",
            bool(GMAIL_APP_PASSWORD)
        )
    )

    results.append(
        check(
            "Recipient",
            bool(RECIPIENT_EMAIL)
        )
    )

    # -------------------------------------------------------
    # Internet
    # -------------------------------------------------------

    results.append(
        check(
            "Internet",
            internet_check()
        )
    )

    # -------------------------------------------------------
    # Chrome Driver
    # -------------------------------------------------------

    driver = None

    try:

        driver = get_driver()

        results.append(
            check(
                "Chrome Driver",
                True
            )
        )

    except Exception as e:

        logger.exception(e)

        results.append(
            check(
                "Chrome Driver",
                False
            )
        )

    finally:

        if driver is not None:

            close_driver(driver)

    # -------------------------------------------------------
    # Final Result
    # -------------------------------------------------------

    print("=" * 60)

    if all(results):

        print("SYSTEM STATUS : READY")

        logger.info("Health Check : PASSED")

        print("=" * 60)
        print()

        return True

    else:

        print("SYSTEM STATUS : FAILED")

        logger.error("Health Check : FAILED")

        print("=" * 60)
        print()

        return False


# ===========================================================
# Entry Point
# ===========================================================

if __name__ == "__main__":

    health_check()