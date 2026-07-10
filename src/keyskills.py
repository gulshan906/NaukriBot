"""
===========================================================
Project : NaukriBot
Module  : keyskills.py
Author  : Gulshan Singh
Version : 3.0.0
===========================================================
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config.config import PROFILE_URL, KEY_SKILL

from src.logger import logger
from src.mail import send_email
from src.utils import sleep, take_screenshot


def update_key_skills(driver):

    result = {
        "module": "Key Skills",
        "status": False,
        "message": ""
    }

    try:

        logger.info("Opening Profile Page...")

        driver.get(PROFILE_URL)

        sleep(5)

        logger.info("Searching Key Skills Edit Icon...")

        edit_icons = driver.find_elements(
            By.CSS_SELECTOR,
            "span.edit.icon"
        )

        if len(edit_icons) < 2:

            result["message"] = (
                "Key Skills Edit Icon Not Found."
            )

            failed_screenshot = take_screenshot(
                driver,
                "keyskills_failed"
            )

            send_email(
                subject="❌ Key Skills - FAILED",
                body=result["message"],
                attachment=failed_screenshot
            )

            return result

        driver.execute_script(
            "arguments[0].click();",
            edit_icons[1]
        )

        logger.info("Key Skills Popup Opened.")

        sleep(3)

        skill_box = driver.find_element(
            By.ID,
            "keySkillSugg"
        )

        skill_box.click()

        sleep(1)

        logger.info(
            f"Adding Skill : {KEY_SKILL}"
        )

        skill_box.send_keys(KEY_SKILL)

        sleep(2)

        skill_box.send_keys(
            Keys.ENTER
        )

        sleep(3)

        save_btn = driver.find_element(
            By.ID,
            "saveKeySkills"
        )

        driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

        logger.info("Save Button Clicked.")

        sleep(5)

        logger.info(
            "Key Skills Updated Successfully."
        )

        screenshot = take_screenshot(
            driver,
            "keyskills_updated"
        )

        result["status"] = True

        result["message"] = f"""
Key Skills Updated Successfully

----------------------------------------
Skill Added
----------------------------------------

{KEY_SKILL}

Status
----------------------------------------

SUCCESS
"""

        send_email(
            subject="✅ Key Skills - SUCCESS",
            body=result["message"],
            attachment=screenshot
        )

        return result

    except Exception as e:

        logger.exception(e)

        failed_screenshot = take_screenshot(
            driver,
            "keyskills_failed"
        )

        result["status"] = False

        result["message"] = str(e)

        try:

            send_email(
                subject="❌ Key Skills - FAILED",
                body=result["message"],
                attachment=failed_screenshot
            )

        except Exception:

            pass

        return result