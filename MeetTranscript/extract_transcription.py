from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class TranscriptionExtractor:
    def __init__(self, driver, transcript_path):
        self.driver = driver
        self.transcript_path = transcript_path
        self.is_running = False  # Add flag to control transcription
    
    def stop_transcription(self):
        """Call this method to stop the transcription"""
        print("\nStopping transcription...")
        self.is_running = False
        self.last_complete_sentence = ""
        self.start_time = None
    
    def get_timestamp(self):
        """Return both absolute and relative timestamps"""
        current_time = datetime.now()
        absolute_time = current_time.strftime("%H:%M:%S")
        
        if self.start_time is None:
            self.start_time = current_time
            
        # Calculate relative time from start
        elapsed = current_time - self.start_time
        relative_seconds = int(elapsed.total_seconds())
        relative_time = f"{relative_seconds//60:02d}:{relative_seconds%60:02d}"
        
        return absolute_time, relative_time
    
    def extract_transcription(self):
        try:
            self.is_running = True
            buffer = ""
            last_speaker = ""
            
            with open(self.transcript_path, "a", encoding="utf-8") as file:
                # Write header
                file.write("=== Transcription Start ===\n")
                file.write(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                file.write("Time  | Elapsed | Speaker | Text\n")
                file.write("-" * 70 + "\n")
                
                while self.is_running:  # Check flag in the loop
                    try:
                        # Check if we should stop
                        if not self.is_running:
                            break

                        # Find the caption container
                        caption_container = self.driver.find_element(By.XPATH, "//div[@class='nMcdL bj4p3b']")
                        
                        # Extract speaker name
                        # Wait until the speaker's name div is visible
                        WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, "//div[@class='KcIKyf jxFHg']"))
                        )
                        try:
                            speaker = caption_container.find_element(By.XPATH, "//div[@class='KcIKyf jxFHg']").text
                        except:
                            speaker = "Unknown"
                        
                        # Extract caption text
                        caption_div = caption_container.find_element(By.XPATH, ".//div[@class='bh44bd VbkSUe']")
                        current_text = " ".join([span.text for span in caption_div.find_elements(By.TAG_NAME, "span")])
                        current_text = ' '.join(current_text.split())  # Clean whitespace
                        
                        # Only process if we have new text
                        if current_text and current_text != buffer:
                            # If current text ends with punctuation
                            if current_text.strip().endswith(('.', '!', '?')):
                                # Only write if it's different from the last complete sentence
                                if current_text != self.last_complete_sentence or speaker != last_speaker:
                                    abs_time, rel_time = self.get_timestamp()
                                    formatted_line = f"{abs_time} | {rel_time} | {speaker:8} | {current_text}\n"
                                    file.write(formatted_line)
                                    file.flush()
                                    self.last_complete_sentence = current_text
                                    last_speaker = speaker
                                buffer = ""
                            else:
                                buffer = current_text
                        
                        for _ in range(5):
                            if not self.is_running:
                                break
                            time.sleep(0.1)
                            
                    except Exception as e:
                        if not self.is_running:
                            break
                        print(f"Temporary error in caption extraction: {e}")
                        time.sleep(0.5)
                        continue
                
                # Write any remaining buffer content
                if buffer and buffer != self.last_complete_sentence:
                    abs_time, rel_time = self.get_timestamp()
                    formatted_line = f"{abs_time} | {rel_time} | {last_speaker:8} | {buffer}\n"
                    file.write(formatted_line)
                    file.flush()
                
                # Write footer
                file.write("\n=== Transcription End ===\n")
                file.write(f"Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
            print("Transcription stopped successfully")
            return True
                        
        except Exception as e:
            print("Failed to start transcription:", e)
            return False
