import os
import re
import undetected_chromedriver as uc


def extract_meeting_code(url: str) -> str:
    try:
        match = re.search(r"meet\.google\.com/([a-z]{3}-[a-z]{4}-[a-z]{3})", url)
        if match:
            return match.group(1)
        else:
            return None
    except Exception as e:
        print(f"Error extracting meeting code: {e}")
        return None


def create_stealth_driver(meeting_code: str):
    """
    Creates a Chrome driver with stealth settings to avoid detection as a bot.
    """
    options = uc.ChromeOptions()

    # Add new experimental options for media handling
    options.add_experimental_option(
        "prefs",
        {
            # Previous options remain the same
            "profile.default_content_setting_values.media_stream_mic": 2,  # 1 = allow
            "profile.default_content_setting_values.media_stream_camera": 2,  # 2 = block
            "profile.content_settings.exceptions.media_stream_camera": {
                "*": {"setting": 2}
            },
            # Previous download settings remain the same
            "download.default_directory": os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "recordings")
            ),
            "download.prompt_for_download": False,
            # "download.directory_upgrade": True,
            # "profile.default_content_setting_values.automatic_downloads": 1,
            "profile.default_content_settings.popups": 0,
        },
    )

    options.add_argument("--auto-select-desktop-capture-source=Screen 1")
    options.add_argument("--auto-accept-this-tab-capture")

    # Add mode argument
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--window-size=1920,1080")  # Set window size to 1920x1080
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")

    driver = uc.Chrome(options=options, version_main=130)
    # driver = uc.Chrome(options=options,
    #                    version_main=129)

    return driver
