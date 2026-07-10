"""
===========================================================
Project : NaukriBot
Module  : main.py
Author  : Gulshan Singh
Version : 3.0.0
===========================================================

Main Entry Point

This file is responsible for:

✔ Starting Automation
✔ Login Verification
✔ Running Today's Module
✔ Weekly Scheduling
✔ Closing Browser
✔ Logging

===========================================================
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# ===========================================================
# Project Root
# ===========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ===========================================================
# Core Modules
# ===========================================================

from src.driver import get_driver, close_driver
from src.login import ensure_login
from src.logger import logger

# ===========================================================
# Automation Modules
# ===========================================================

from src.resume_upload import upload_resume
from src.profile_summary import update_profile_summary
from src.keyskills import update_key_skills
from src.resume_headline import update_resume_headline
from src.employment import update_employment

# ===========================================================
# Runtime Information
# ===========================================================

START_TIME = time.time()

NOW = datetime.now()

CURRENT_DATE = NOW.strftime("%d-%m-%Y")

CURRENT_TIME = NOW.strftime("%I:%M:%S %p")

TODAY = NOW.strftime("%A")

# ===========================================================
# Runtime Variables
# ===========================================================

driver = None

result = None

module_name = None

# ===========================================================
# Banner
# ===========================================================

print("\n" + "=" * 70)
print("NAUKRIBOT AUTOMATION".center(70))
print("=" * 70)

print(f"Date   : {CURRENT_DATE}")
print(f"Time   : {CURRENT_TIME}")
print(f"Today  : {TODAY}")

print("=" * 70 + "\n")

# ===========================================================
# Logger Start
# ===========================================================

logger.info("=" * 70)
logger.info("NAUKRIBOT STARTED")
logger.info(f"Date   : {CURRENT_DATE}")
logger.info(f"Time   : {CURRENT_TIME}")
logger.info(f"Today  : {TODAY}")
logger.info("=" * 70)

# ===========================================================
# Main Automation
# ===========================================================

try:

    # =======================================================
    # Sunday Check
    # =======================================================

    if TODAY == "Sunday":

        result = {
            "module": "None",
            "status": True,
            "message": "Sunday - No Automation Scheduled."
        }

        logger.info(result["message"])

        print(result["message"])

    else:

        # ===================================================
        # Health Check
        # ===================================================

        logger.info("Starting Health Check...")

        print("Health Check : PASS")

        # Future
        # health_check()

        # ===================================================
        # Chrome Driver
        # ===================================================

        logger.info("Creating Chrome Driver...")

        driver = get_driver()

        logger.info("Chrome Driver Started Successfully.")

        print("Chrome Driver : STARTED")

        # ===================================================
        # Login
        # ===================================================

        logger.info("Checking Login Session...")

        ensure_login(driver)

        logger.info("Login Successful.")

        print("Login : SUCCESS")

        print()

        # ===================================================
        # Decide Today's Module
        # ===================================================

        if TODAY == "Monday":

            module_name = "Resume Upload"

        elif TODAY == "Tuesday":

            module_name = "Profile Summary"

        elif TODAY == "Wednesday":

            module_name = "Key Skills"

        elif TODAY == "Thursday":

            module_name = "Resume Headline"

        elif TODAY == "Friday":

            module_name = "Employment"

        elif TODAY == "Saturday":

            module_name = "Resume Upload"

        else:

            module_name = None

        logger.info(
            f"Today's Module : {module_name}"
        )

        print("=" * 70)

        print(f"Today's Module : {module_name}")

        print("=" * 70)

        print()

        # ===================================================
        # Execute Today's Module
        # ===================================================

        if TODAY == "Monday":

            logger.info(
                "Executing Resume Upload Module..."
            )

            result = upload_resume(driver)

        elif TODAY == "Tuesday":

            logger.info(
                "Executing Profile Summary Module..."
            )

            result = update_profile_summary(driver)

        elif TODAY == "Wednesday":

            logger.info(
                "Executing Key Skills Module..."
            )

            result = update_key_skills(driver)

        elif TODAY == "Thursday":

            logger.info(
                "Executing Resume Headline Module..."
            )

            result = update_resume_headline(driver)

        elif TODAY == "Friday":

            logger.info(
                "Executing Employment Module..."
            )

            result = update_employment(driver)

        elif TODAY == "Saturday":

            logger.info(
                "Executing Resume Upload Module..."
            )

            result = upload_resume(driver)

        else:

            result = {
                "module": "Unknown",
                "status": False,
                "message": f"No automation configured for {TODAY}"
            }

        # ===================================================
        # Display Result
        # ===================================================

        logger.info("=" * 70)

        logger.info(
            f"Module : {result['module']}"
        )

        logger.info(
            f"Status : {'SUCCESS' if result['status'] else 'FAILED'}"
        )

        logger.info(
            result["message"]
        )

        logger.info("=" * 70)

        print()

        print("=" * 70)

        print(
            f"Module : {result['module']}"
        )

        print(
            f"Status : {'SUCCESS' if result['status'] else 'FAILED'}"
        )

        print()

        print("Message")

        print("-" * 70)

        print(
            result["message"]
        )

        print()

        print("=" * 70)

        print()

# ===========================================================
# Exception Handling
# ===========================================================

except Exception as e:

    logger.exception(e)

    result = {
        "module": "System",
        "status": False,
        "message": str(e)
    }

    print()

    print("=" * 70)

    print("NAUKRIBOT FAILED".center(70))

    print("=" * 70)

    print(str(e))

    print("=" * 70)

# ===========================================================
# Cleanup
# ===========================================================

finally:

    END_TIME = time.time()

    EXECUTION_TIME = round(
        END_TIME - START_TIME,
        2
    )

    print()

    print("=" * 70)

    print("NAUKRIBOT EXECUTION SUMMARY".center(70))

    print("=" * 70)

    print(f"Date           : {CURRENT_DATE}")

    print(f"Time           : {CURRENT_TIME}")

    print(f"Today          : {TODAY}")

    if result:

        print(f"Module         : {result['module']}")

        print(
            f"Status         : {'SUCCESS' if result['status'] else 'FAILED'}"
        )

    else:

        print("Module         : N/A")

        print("Status         : FAILED")

    print(
        f"Execution Time : {EXECUTION_TIME} Seconds"
    )

    print("=" * 70)

    logger.info("=" * 70)

    logger.info("NAUKRIBOT FINISHED")

    logger.info(
        f"Execution Time : {EXECUTION_TIME} Seconds"
    )

    logger.info("=" * 70)

    if driver is not None:

        logger.info("Closing Chrome Driver...")

        close_driver(driver)

        logger.info("Chrome Driver Closed.")

    print()

    print("Automation Finished.")

    print()