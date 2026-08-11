from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

    current_text = ""
    new_text = ""
    saved_text = ""

    try:

        # ==================================================
        # OPEN PROFILE PAGE
        # ==================================================

        logger.info("Opening Profile Page...")

        driver.get(PROFILE_URL)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.ID, "lazyProfileSummary")
            )
        )

        sleep(3)

        # ==================================================
        # SCROLL TO PROFILE SUMMARY
        # ==================================================

        logger.info("Scrolling to Profile Summary...")

        driver.execute_script(
            """
            const element = document.getElementById(
                'lazyProfileSummary'
            );

            if (element) {
                element.scrollIntoView({
                    block: 'center',
                    behavior: 'instant'
                });
            }
            """
        )

        sleep(1)

        # ==================================================
        # FIND PROFILE SUMMARY EDIT ICON
        # ==================================================

        logger.info(
            "Searching Profile Summary Edit Icon..."
        )

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

                parent_text = (
                    parent.text or ""
                ).strip()

                if "Profile summary" in parent_text:

                    summary_icon = icon

                    logger.info(
                        "Profile Summary Edit Icon Found."
                    )

                    break

            except Exception:

                continue

        if summary_icon is None:

            result["message"] = (
                "Profile Summary Edit Icon Not Found."
            )

            send_email(
                subject="❌ Profile Summary - FAILED",
                body=result["message"]
            )

            return result

        # ==================================================
        # CLICK EDIT ICON
        # ==================================================

        driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center'
            });

            arguments[0].click();
            """,
            summary_icon
        )

        logger.info(
            "Profile Summary Popup Opened."
        )

        sleep(1)

        # ==================================================
        # FIND SUMMARY TEXT BOX
        # ==================================================

        summary_box = WebDriverWait(
            driver,
            20
        ).until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "profileSummaryTxt"
                )
            )
        )

        sleep(2)

        # ==================================================
        # READ CURRENT SUMMARY
        # ==================================================

        current_text = (
            summary_box.get_attribute("value")
            or ""
        )

        logger.info(
            f"Current Profile Summary: {current_text}"
        )

        print("\n================================")
        print("CURRENT PROFILE SUMMARY")
        print("================================\n")

        print(current_text)

        # ==================================================
        # CREATE NEW SUMMARY
        # ==================================================

        if current_text.strip().endswith(
            " Updated"
        ):

            new_text = current_text[
                :-len(" Updated")
            ]

        else:

            new_text = (
                current_text.rstrip()
                + " Updated"
            )

        logger.info(
            f"New Profile Summary: {new_text}"
        )

        print("\n================================")
        print("NEW PROFILE SUMMARY")
        print("================================\n")

        print(new_text)

        # ==================================================
        # SCROLL TEXT BOX
        # ==================================================

        driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center'
            });
            """,
            summary_box
        )

        sleep(1)

        # ==================================================
        # CLICK TEXT BOX
        # ==================================================

        summary_box.click()

        sleep(1)

        # ==================================================
        # CLEAR EXISTING TEXT
        # ==================================================

        logger.info(
            "Clearing Existing Profile Summary..."
        )

        summary_box.send_keys(
            Keys.CONTROL,
            "a"
        )

        sleep(0.5)

        summary_box.send_keys(
            Keys.BACKSPACE
        )

        sleep(1)

        # ==================================================
        # TYPE NEW TEXT
        # ==================================================

        logger.info(
            "Typing New Profile Summary..."
        )

        summary_box.send_keys(
            new_text
        )

        sleep(2)

        # ==================================================
        # VERIFY TEXTBOX VALUE
        # ==================================================

        typed_text = (
            summary_box.get_attribute("value")
            or ""
        )

        logger.info(
            f"Text After Typing: {typed_text}"
        )

        if typed_text.strip() != new_text.strip():

            raise Exception(
                "Profile Summary text was not entered correctly.\n\n"
                f"Expected:\n{new_text}\n\n"
                f"Actual:\n{typed_text}"
            )

        logger.info(
            "Profile Summary Text Entered Successfully."
        )

        # ==================================================
        # FIND SAVE BUTTON
        # ==================================================

        logger.info(
            "Searching Profile Summary Save Button..."
        )

        save_btn = None

        # ------------------------------------------
        # METHOD 1
        # Exact visible Save text
        # ------------------------------------------

        save_xpaths = [

            "//button[normalize-space()='Save']",

            "//button[contains(normalize-space(.), 'Save')]",

            "//input[@type='button' and "
            "contains(translate(@value,'SAVE','save'),'save')]",

            "//input[@type='submit' and "
            "contains(translate(@value,'SAVE','save'),'save')]",

            "//button[contains(@class,'btn-dark-ot')]",

            "//button[contains(@class,'btn-dark') and "
            "contains(normalize-space(.),'Save')]",

            "//button[contains(@class,'save')]",

            "//button[contains(@aria-label,'Save')]",

            "//button[contains(@title,'Save')]"
        ]

        for xpath in save_xpaths:

            try:

                buttons = driver.find_elements(
                    By.XPATH,
                    xpath
                )

                for button in buttons:

                    try:

                        if (
                            button.is_displayed()
                            and button.is_enabled()
                        ):

                            save_btn = button

                            logger.info(
                                f"Save Button Found Using: {xpath}"
                            )

                            break

                    except Exception:

                        continue

                if save_btn is not None:
                    break

            except Exception:

                continue

        # ==================================================
        # SAVE BUTTON NOT FOUND
        # ==================================================

        if save_btn is None:

            # Log visible buttons for debugging
            try:

                visible_buttons = driver.find_elements(
                    By.XPATH,
                    "//button"
                )

                logger.error(
                    "Could not find Save button."
                )

                logger.error(
                    f"Total buttons on page: "
                    f"{len(visible_buttons)}"
                )

                for index, button in enumerate(
                    visible_buttons
                ):

                    try:

                        if button.is_displayed():

                            logger.error(
                                f"BUTTON {index}: "
                                f"text={button.text!r}, "
                                f"class={button.get_attribute('class')!r}, "
                                f"id={button.get_attribute('id')!r}"
                            )

                    except Exception:

                        continue

            except Exception:

                pass

            raise Exception(
                "Profile Summary Save Button Not Found."
            )

        # ==================================================
        # SCROLL SAVE BUTTON
        # ==================================================

        driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center'
            });
            """,
            save_btn
        )

        sleep(1)

        # ==================================================
        # CLICK SAVE
        # ==================================================

        logger.info(
            "Clicking Profile Summary Save Button..."
        )

        try:

            save_btn.click()

            logger.info(
                "Save Button Clicked Normally."
            )

        except Exception as click_error:

            logger.warning(
                f"Normal Save click failed: "
                f"{click_error}"
            )

            logger.info(
                "Trying JavaScript Save Button Click..."
            )

            driver.execute_script(
                """
                arguments[0].click();
                """,
                save_btn
            )

            logger.info(
                "Save Button Clicked Using JavaScript."
            )

        # ==================================================
        # WAIT AFTER SAVE
        # ==================================================

        sleep(3)

        # ==================================================
        # REFRESH PROFILE
        # ==================================================

        logger.info(
            "Refreshing Profile For Verification..."
        )

        driver.refresh()

        WebDriverWait(
            driver,
            30
        ).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "lazyProfileSummary"
                )
            )
        )

        sleep(4)

        logger.info(
            "Profile Refreshed Successfully."
        )

        # ==================================================
        # SCROLL PROFILE SUMMARY AGAIN
        # ==================================================

        driver.execute_script(
            """
            const element = document.getElementById(
                'lazyProfileSummary'
            );

            if (element) {
                element.scrollIntoView({
                    block: 'center',
                    behavior: 'instant'
                });
            }
            """
        )

        sleep(1)

        # ==================================================
        # FIND EDIT ICON AGAIN
        # ==================================================

        logger.info(
            "Opening Profile Summary For Verification..."
        )

        edit_icons = driver.find_elements(
            By.XPATH,
            "//span[contains(@class,'edit')]"
        )

        summary_icon = None

        for icon in edit_icons:

            try:

                parent = icon.find_element(
                    By.XPATH,
                    "./ancestor::div[contains(@class,'widgetHead')]"
                )

                if "Profile summary" in (
                    parent.text or ""
                ):

                    summary_icon = icon
                    break

            except Exception:

                continue

        if summary_icon is None:

            raise Exception(
                "Profile Summary Edit Icon Not Found "
                "After Refresh."
            )

        # ==================================================
        # OPEN SUMMARY AGAIN
        # ==================================================

        driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center'
            });

            arguments[0].click();
            """,
            summary_icon
        )

        sleep(1)

        # ==================================================
        # READ SAVED SUMMARY
        # ==================================================

        verification_box = WebDriverWait(
            driver,
            20
        ).until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "profileSummaryTxt"
                )
            )
        )

        saved_text = (
            verification_box.get_attribute("value")
            or ""
        )

        logger.info(
            f"Actual Saved Profile Summary: {saved_text}"
        )

        print("\n================================")
        print("ACTUAL SAVED PROFILE SUMMARY")
        print("================================\n")

        print(saved_text)

        # ==================================================
        # FINAL SERVER SAVE VERIFICATION
        # ==================================================

        if saved_text.strip() != new_text.strip():

            raise Exception(
                "Profile Summary was NOT saved successfully.\n\n"
                "EXPECTED:\n"
                f"{new_text}\n\n"
                "ACTUAL SAVED VALUE:\n"
                f"{saved_text}"
            )

        logger.info(
            "Profile Summary Save Verified Successfully."
        )

        # ==================================================
        # OPEN NAUKRI HOME PAGE
        # ==================================================

        driver.get(
            "https://www.naukri.com/mnjuser/homepage"
        )

        sleep(1)

        logger.info(
            "Naukri Home Page Opened Successfully."
        )

        # ==================================================
        # FINAL SCREENSHOT
        # ==================================================

        screenshot = take_screenshot(
            driver,
            "naukri_homepage"
        )

        # ==================================================
        # SUCCESS RESULT
        # ==================================================

        result["status"] = True

        result["message"] = f"""
Profile Summary Updated Successfully

---

## Old Profile Summary

{current_text}

---

## New Profile Summary

{new_text}

---

## Verified Saved Summary

{saved_text}
"""

        # ==================================================
        # SUCCESS EMAIL
        # ==================================================

        send_email(
            subject="✅ Profile Summary - SUCCESS",
            body=result["message"],
            attachment=screenshot
        )

        logger.info(
            "Profile Summary Update Completed Successfully."
        )

        return result

    # ======================================================
    # ERROR HANDLING
    # ======================================================

    except Exception as e:

        logger.exception(
            "Profile Summary Update Failed."
        )

        result["status"] = False

        result["message"] = str(e)

        # ==================================================
        # FAILURE SCREENSHOT
        # ==================================================

        try:

            failed_screenshot = take_screenshot(
                driver,
                "profile_summary_failed"
            )

        except Exception:

            failed_screenshot = None

        # ==================================================
        # FAILURE EMAIL
        # ==================================================

        try:

            send_email(
                subject="❌ Profile Summary - FAILED",
                body=(
                    "Profile Summary Update Failed.\n\n"
                    f"Error:\n{str(e)}"
                ),
                attachment=failed_screenshot
            )

        except Exception:

            logger.exception(
                "Failed to send failure email."
            )

        return result