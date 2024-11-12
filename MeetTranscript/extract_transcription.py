from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TranscriptionExtractor:
    def __init__(self, driver, transcript_path):
        self.driver = driver
        self.transcript_path = transcript_path
        self.is_running = False  # Add flag to control transcription
    
    def stop_transcription(self):
        """Call this method to stop the transcription"""
        print("\nStopping transcription...")
        self.is_running = False
    
    def extract_transcription(self):
        try:
            self.is_running = True
            
            with open("captions.txt", "a", encoding="utf-8") as file:
                previous_text = ""
                
                while self.is_running:  # Check flag in the loop
                    try:
                        # Check if we should stop
                        if not self.is_running:
                            break

                        caption_div = self.driver.find_element(By.XPATH, "//div[@class='nMcdL bj4p3b']//div[@class='bh44bd VbkSUe']")
                        current_text = " ".join([span.text for span in caption_div.find_elements(By.TAG_NAME, "span")])
                        
                        if current_text != previous_text and current_text.strip():
                            file.write(current_text + "\n")
                            file.flush()
                            previous_text = current_text
                        
                        # Shorter sleep time to be more responsive to stop signal
                        for _ in range(10):  # 1 second broken into 10 parts
                            if not self.is_running:
                                break
                            time.sleep(0.1)
                            
                    except Exception as e:
                        if not self.is_running:
                            break
                        print(f"Temporary error in caption extraction: {e}")
                        time.sleep(1)
                        continue
                
            print("Transcription stopped successfully")
            return True
                        
        except Exception as e:
            print("Failed to start transcription:", e)
            return False
