from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def create_stealth_driver():
    options = webdriver.ChromeOptions()
    
    # Add stealth settings
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Mimic regular browser behavior
    options.add_argument('--disable-infobars')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })
    
    # Add random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    # Create driver with stealth settings
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Execute CDP commands to prevent detection
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })
    
    return driver


def type_username(driver, random_num: int = 0):
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys(f"Guest_{random_num}")
    time.sleep(2)

def ask_join_meet(driver):
    try:
        driver.find_element(By.XPATH, "//button[span[contains(text(), 'Ask to join')]]").click()
        # time.sleep(2)
        try:
            while True:
                pass  # Infinite loop to keep the browser running
        except KeyboardInterrupt:
            # This allows you to exit the loop and close the browser with Ctrl+C
            print("Closing browser...")
            driver.quit()
    except Exception as e:
        print("Failed to click on the 'Ask to join' button:", e)


def create_random_number():
    return random.randint(1000, 9999)

def google_meet(meet_url: str = None):
    driver = create_stealth_driver()
    driver.get(meet_url)
    time.sleep(3)
    random_num = create_random_number()
    type_username(driver, random_num)
    ask_join_meet(driver)
    # driver.quit()

if __name__ == '__main__':
    google_meet()