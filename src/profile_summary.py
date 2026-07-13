"""
===========================================================
Project : NaukriBot
Module  : profile_summary.py
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


def update_profile_summary(driver):

    result = {
        "module": "Profile Summary",
        "status": False,
        "message": ""
    }

    try:

        logger.info("Opening Profile Page...")

        driver.get(PROFILE_URL)

        sleep(8)

        logger.info("Scrolling to Profile Summary...")

        driver.execute_script(
            """
            document.getElementById(
                'lazyProfileSummary'
            ).scrollIntoView();
            """
        )

        sleep(3)

        logger.info("Searching Profile Summary Edit Icon...")

        edit_icons = driver.find_elements(
            By.XPATH,
            "//span[contains(@class,'edit')]"
        )

        logger.info(
            f"Total Edit Icons Found : {len(edit_icons)}"
        )

        summary_icon = None

        for icon in edit_icons:

            try:

                parent = icon.find_element(
                    By.XPATH,
                    "./ancestor::div[contains(@class,'widgetHead')]"
                )

                if "Profile summary" in parent.text:

                    summary_icon = icon
                    break

            except Exception:

                pass

        if summary_icon is None:

            result["message"] = (
                "Profile Summary Edit Icon Not Found."
            )

            send_email(
                subject="❌ Profile Summary - FAILED",
                body=result["message"]
            )

            return result

        driver.execute_script(
            "arguments[0].click();",
            summary_icon
        )

        logger.info(
            "Profile Summary Popup Opened."
        )

        sleep(5)

        summary_box = driver.find_element(
            By.ID,
            "profileSummaryTxt"
        )

        current_text = summary_box.get_attribute(
            "value"
        )

        logger.info(
            "Current Profile Summary Loaded."
        )

        print("\nCurrent Summary\n")

        print(current_text)

        # ---------------------------------------
        # Existing Logic (No Change)
        # ---------------------------------------

        if current_text.strip().endswith(
            " Updated"
        ):

            new_text = current_text.replace(
                " Updated",
                ""
            )

        else:

            new_text = current_text + " Updated"

        print("\nNew Summary\n")

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
            summary_box,
            new_text
        )

        sleep(2)

        save_btn = driver.find_element(
            By.CSS_SELECTOR,
            "button.btn-dark-ot"
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
            "Profile Summary Updated Successfully."
        )

        # ==========================================
        # Refresh Profile
        # ==========================================

        driver.refresh()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "lazyProfileSummary"
                )
            )
        )

        sleep(2)

        driver.execute_script(
            """
            document.getElementById(
                'lazyProfileSummary'
            ).scrollIntoView();
            """
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
            "profile_summary_updated"
        )

        result["status"] = True

        result["message"] = f"""
Profile Summary Updated Successfully

----------------------------------------
Old Profile Summary
----------------------------------------

{current_text}

----------------------------------------
New Profile Summary
----------------------------------------

{new_text}
"""

        # ==========================================
        # Send Success Mail
        # ==========================================

        send_email(
            subject="✅ Profile Summary - SUCCESS",
            body=result["message"],
            attachment=screenshot
        )

        return result

    except Exception as e:

        logger.exception(e)

        failed_screenshot = take_screenshot(
            driver,
            "profile_summary_failed"
        )

        result["message"] = str(e)

        try:

            send_email(
                subject="❌ Profile Summary - FAILED",
                body=result["message"],
                attachment=failed_screenshot
            )

        except Exception:

            pass

        return result