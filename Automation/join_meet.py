from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MeetConfig:
    def __init__(self, driver):
        """
        Initializes a new instance of the JoinMeet class.

        Args:
            driver: The Selenium WebDriver instance to interact with the browser.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
    
    def continue_without_mic_video(self):
        """
        Clicks on the "Continue without microphone and camera" button.

        This is a part of the process of joining a Google Meet meeting.
        It is used to skip the microphone and camera permission prompts.
        """
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Continue without microphone and camera']]")))
            button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Continue without microphone and camera']]")
            button.click()
            time.sleep(2)
        except Exception as e:
            print("Failed to click on the 'Continue without microphone and camera' button:", e)
        
    def type_username(self, random_num: int = 0) -> None:
        """
        Enters a guest username in the Google Meet dialog.

        Args:
            random_num: An optional random number to append to the guest username.
        """
        try:
            print('Creating Guest user:', random_num)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
            self.driver.find_element(By.XPATH, "//input[@type='text']").send_keys(f"Guest_{random_num}")
            time.sleep(2)
        except Exception as e:
            print("Failed to type username:", e)


    def ask_join_meet(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Ask to join')]]")))
            button = self.driver.find_element(By.XPATH, "//button[span[contains(text(), 'Ask to join')]]")
            button.click()
            time.sleep(2)
        except Exception as e:
            print("Failed to click on the 'Ask to join' button:", e)
    
    def leave_meet(self):
        """
        Leaves the Google Meet call by clicking on the "Leave call" button.

        This method is used to leave the Google Meet call after the recording has finished.
        """
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Leave call']")))
            leave_call_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Leave call']")
            leave_call_button.click()
            time.sleep(2)
        except Exception as e:
            print("Failed to click on the 'Leave call' button:", e)
    
    def dismiss_popup(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Got it']]")))
            button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Got it']]")
            button.click()
            time.sleep(2)
        except Exception as e:
            print("Failed to click on the 'Got it' button:", e)
    
    def click_on_caption(self):
        try:
            # Locate button using aria-label attribute
            button = self.driver.find_element(By.XPATH, "//button[@aria-label='Turn on captions']")
            button.click()
            time.sleep(2)
        except Exception as e:
            print("Failed to click on the 'Turn on captions' button:", e)
