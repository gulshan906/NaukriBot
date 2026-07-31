"""
===========================================================
Project : NaukriBot
Module  : resume_headline.py
Author  : Gulshan Singh
Version : 2.2.1
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

        sleep(2)

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
        # Click Save Button
        # -----------------------------------------

        logger.info("Clicking Save Button...")

        save_btn = driver.find_element(
            By.XPATH,
            "//button[@type='submit' and normalize-space()='Save']"
        )

        driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

        sleep(2)

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
        # Open Naukri Home Page
        # ==========================================
        driver.get("https://www.naukri.com/mnjuser/homepage")
        sleep(2)
        logger.info("Naukri Home Page Opened Successfully.")

        # ==========================================
        # Final Screenshot
        # ==========================================

        screenshot = take_screenshot(
            driver,
            "naukri_homepage"
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