import random
import psutil

import undetected_chromedriver as uc


def create_stealth_driver():
    """
    Creates a Chrome driver with stealth settings to avoid detection as a bot.
    """
    options = uc.ChromeOptions()
    
    # Add stealth settings
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument('--disable-blink-features=AutomationControlled')

    # Mimic regular browser behavior
    # options.add_argument('--disable-infobars')
    options.add_argument("start-maximized")
    # options.add_argument('--disable-extensions')

    # Add random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    ]

    random_user_agent = random.choice(user_agents)
    print(f"Using random user agent: {random_user_agent}")
    options.add_argument(f'user-agent={random_user_agent}')

    # Enable headless mode if needed
    # options.add_argument("--headless")

    # Create driver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = uc.Chrome(options=options) 

    return driver

def terminate_ffmpeg_processes():
    # Loop through all the running processes
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            # Check if the process is FFmpeg
            if 'ffmpeg' in proc.info['name']:
                print(f"Terminating FFmpeg process with PID {proc.info['pid']}")
                proc.terminate()  # Terminate the process
                proc.wait()       # Wait for the process to terminate
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process has already terminated or we do not have permission
            pass