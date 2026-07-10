"""
===========================================================
Project : NaukriBot
Module  : resume_upload.py
Author  : Gulshan Singh
Version : 2.1.0
===========================================================
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import PROFILE_URL, RESUME_FILE

from src.logger import logger
from src.mail import send_email
from src.utils import take_screenshot


def upload_resume(driver):

    result = {
        "module": "Resume Upload",
        "status": False,
        "message": ""
    }

    try:

        if RESUME_FILE is None:
            raise FileNotFoundError(
                "Resume file not found in Resume folder."
            )

        logger.info("Opening Profile Page...")

        driver.get(PROFILE_URL)

        upload_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.ID, "attachCV")
            )
        )

        logger.info(
            f"Uploading Resume : {RESUME_FILE.name}"
        )

        upload_box.send_keys(
            str(RESUME_FILE)
        )

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'Resume') or contains(text(),'Uploaded')]"
                )
            )
        )

        logger.info(
            "Resume Uploaded Successfully."
        )

        screenshot = take_screenshot(
            driver,
            "resume_uploaded"
        )

        result["status"] = True

        result["message"] = f"""
Resume Uploaded Successfully

----------------------------------------
Resume File
----------------------------------------

{RESUME_FILE.name}
"""

        # ==========================================
        # Send Success Mail
        # ==========================================

        send_email(
            subject="✅ Resume Upload - SUCCESS",
            body=result["message"],
            attachment=screenshot
        )

        return result

    except Exception as e:

        logger.exception(e)

        failed_screenshot = take_screenshot(
            driver,
            "resume_upload_failed"
        )

        result["message"] = str(e)

        # ==========================================
        # Send Failure Mail
        # ==========================================

        try:

            send_email(
                subject="❌ Resume Upload - FAILED",
                body=result["message"],
                attachment=failed_screenshot
            )

        except Exception:

            pass

        return result