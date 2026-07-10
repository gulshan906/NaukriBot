"""
===========================================================
Project : NaukriBot
Module  : employment.py
Author  : Gulshan Singh
Version : 2.1.0
===========================================================
"""

from selenium.webdriver.common.by import By

from config.config import PROFILE_URL

from src.logger import logger
from src.mail import send_email
from src.utils import sleep, take_screenshot


def update_employment(driver):

    result = {
        "module": "Employment",
        "status": False,
        "message": ""
    }

    try:

        logger.info("Opening Profile Page...")

        driver.get(PROFILE_URL)

        sleep(8)

        logger.info("Scrolling to Employment Section...")

        driver.execute_script(
            """
            var el = document.getElementById(
                'lazyEmployment'
            );

            if(el){
                el.scrollIntoView(
                    {behavior:'smooth'}
                );
            }
            """
        )

        sleep(5)

        edit_icons = driver.find_elements(
            By.XPATH,
            "//span[contains(@class,'edit')]"
        )

        logger.info(
            f"Total Edit Icons Found : {len(edit_icons)}"
        )

        employment_icon = None

        for icon in edit_icons:

            try:

                icon.find_element(
                    By.XPATH,
                    "./ancestor::div[contains(@class,'emp-list')]"
                )

                employment_icon = icon

                break

            except Exception:

                pass

        if employment_icon is None:

            result["message"] = (
                "Employment Edit Icon Not Found."
            )

            send_email(
                subject="❌ Employment - FAILED",
                body=result["message"]
            )

            return result

        driver.execute_script(
            "arguments[0].click();",
            employment_icon
        )

        logger.info(
            "Employment Popup Opened."
        )

        sleep(5)

        desc_box = driver.find_element(
            By.ID,
            "jobDescription"
        )

        current_text = desc_box.get_attribute(
            "value"
        )

        logger.info(
            "Current Employment Description Loaded."
        )

        print("\nCurrent Employment Description\n")

        print(current_text)

        # ---------------------------------------
        # Existing Logic (No Change)
        # ---------------------------------------

        if current_text.strip().endswith("|"):

            new_text = current_text.rstrip("|").rstrip()

        else:

            new_text = current_text + " |"

        print("\nNew Employment Description\n")

        print(new_text)

        driver.execute_script(
            """
            arguments[0].value = arguments[1];

            arguments[0].dispatchEvent(
                new Event(
                    'input',
                    {bubbles:true}
                )
            );

            arguments[0].dispatchEvent(
                new Event(
                    'change',
                    {bubbles:true}
                )
            );
            """,
            desc_box,
            new_text
        )

        sleep(2)

        save_btn = driver.find_element(
            By.ID,
            "submitEmployment"
        )

        driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

        logger.info(
            "Save Button Clicked."
        )

        sleep(5)

        logger.info(
            "Employment Updated Successfully."
        )

        screenshot = take_screenshot(
            driver,
            "employment_updated"
        )

        result["status"] = True

        result["message"] = f"""
Employment Updated Successfully

----------------------------------------
Old Employment Description
----------------------------------------

{current_text}

----------------------------------------
New Employment Description
----------------------------------------

{new_text}
"""

        # ==========================================
        # Send Success Mail
        # ==========================================

        send_email(
            subject="✅ Employment - SUCCESS",
            body=result["message"],
            attachment=screenshot
        )

        return result

    except Exception as e:

        logger.exception(e)

        failed_screenshot = take_screenshot(
            driver,
            "employment_failed"
        )

        result["message"] = str(e)

        try:

            send_email(
                subject="❌ Employment - FAILED",
                body=result["message"],
                attachment=failed_screenshot
            )

        except Exception:

            pass

        return result