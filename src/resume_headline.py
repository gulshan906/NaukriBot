"""
===========================================================
Project : NaukriBot
Module  : resume_headline.py
Author  : Gulshan Singh
Version : 2.2.0
===========================================================
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import PROFILE_URL

from src.logger import logger
from src.mail import send_email
from src.utils import sleep, take_screenshot


def update_resume_headline(driver):

    result = {
        "module": "Resume Headline",
        "status": False,
        "message": ""
    }

    try:

        logger.info("Opening Profile Page...")

        driver.get(PROFILE_URL)

        sleep(5)

        logger.info("Opening Resume Headline Popup...")

        driver.find_element(
            By.CSS_SELECTOR,
            "span.edit.icon"
        ).click()

        sleep(3)

        headline_box = driver.find_element(
            By.ID,
            "resumeHeadlineTxt"
        )

        current_text = headline_box.get_attribute(
            "value"
        )

        logger.info(
            f"Current Headline : {current_text}"
        )

        print("\nCurrent Headline\n")

        print(current_text)

        headline_box.click()

        sleep(1)

        # -----------------------------------------
        # Existing Logic (No Change)
        # -----------------------------------------

        headline_box.send_keys(" ")

        headline_box.send_keys("|")

        sleep(2)

        updated_text = headline_box.get_attribute(
            "value"
        )

        logger.info(
            f"Updated Headline : {updated_text}"
        )

        logger.info(
            "Headline Modified"
        )

        # -----------------------------------------
        # Submit Form
        # -----------------------------------------

        driver.execute_script(
            """
            document.forms['resumeHeadlineForm'].submit();
            """
        )

        sleep(5)

        logger.info(
            "Resume Headline Updated Successfully."
        )

        # ==========================================
        # Refresh Profile
        # ==========================================

        driver.refresh()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "span.edit.icon"
                )
            )
        )

        sleep(2)

        logger.info(
            "Profile Refreshed Successfully."
        )

        # ==========================================
        # Final Screenshot
        # ==========================================

        screenshot = take_screenshot(
            driver,
            "resume_headline_updated"
        )

        result["status"] = True

        result["message"] = f"""
Resume Headline Updated Successfully

----------------------------------------
Old Headline
----------------------------------------

{current_text}

----------------------------------------
New Headline
----------------------------------------

{updated_text}
"""

        # ==========================================
        # Send Success Mail
        # ==========================================

        send_email(
            subject="✅ Resume Headline - SUCCESS",
            body=result["message"],
            attachment=screenshot
        )

        return result

    except Exception as e:

        logger.exception(e)

        failed_screenshot = take_screenshot(
            driver,
            "resume_headline_failed"
        )

        result["message"] = str(e)

        # ==========================================
        # Send Failed Mail
        # ==========================================

        try:

            send_email(
                subject="❌ Resume Headline - FAILED",
                body=result["message"],
                attachment=failed_screenshot
            )

        except Exception:

            pass

        return result