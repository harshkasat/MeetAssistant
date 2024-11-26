from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class TranscriptionExtractor:
    def __init__(self, driver, transcript_path):
        self.driver = driver
        self.transcript_path = transcript_path
        self.is_running = False
        self.start_time = None
        self.last_complete_sentence = ""
        self.buffer = {}  # Store buffer per speaker
        
    def stop_transcription(self):
        print("\nStopping transcription...")
        self.is_running = False
    
    def get_timestamp(self):
        current_time = datetime.now()
        absolute_time = current_time.strftime("%H:%M:%S")
        
        if self.start_time is None:
            self.start_time = current_time
            
        elapsed = current_time - self.start_time
        relative_seconds = int(elapsed.total_seconds())
        relative_time = f"{relative_seconds//60:02d}:{relative_seconds%60:02d}"
        
        return absolute_time, relative_time
    
    def extract_transcription(self):
        try:
            self.is_running = True
            last_speaker = None
            
            with open(self.transcript_path, "w", encoding="utf-8") as file:
                file.write("=== Transcription Start ===\n")
                file.write(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                file.write("Time  | Elapsed | Speaker | Text\n")
                file.write("-" * 70 + "\n")
                
                while self.is_running:
                    try:
                        # Find all caption containers (handles multiple speakers)
                        caption_containers = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.nMcdL.bj4p3b"))
                        )
                        
                        for container in caption_containers:
                            try:
                                # Extract speaker name with better error handling
                                try:
                                    speaker = container.find_element(By.CSS_SELECTOR, "div.KcIKyf.jxFHg").text
                                except:
                                    speaker = "Unknown"
                                
                                # Extract caption text using CSS selector
                                spans = container.find_elements(By.CSS_SELECTOR, "div.bh44bd.VbkSUe span")
                                current_text = " ".join(span.text for span in spans).strip()
                                
                                # Only process if text is not empty
                                if current_text:
                                    # Initialize buffer for new speakers
                                    if speaker not in self.buffer:
                                        self.buffer[speaker] = ""
                                    
                                    # If speaker changes or text is significantly different
                                    if (last_speaker and last_speaker != speaker) or \
                                    (self.buffer[speaker] and 
                                        len(current_text) > len(self.buffer[speaker]) and 
                                        current_text not in self.buffer[speaker]):
                                        
                                        # Write previous speaker's text
                                        abs_time, rel_time = self.get_timestamp()
                                        formatted_line = f"{abs_time} | {rel_time} | {last_speaker:8} | {self.buffer.get(last_speaker, '')}\n"
                                        file.write(formatted_line)
                                        file.flush()
                                        
                                        # Reset buffer for the new speaker
                                        self.buffer[speaker] = current_text
                                    else:
                                        # Store the most meaningful text
                                        if len(current_text) > len(self.buffer[speaker]):
                                            self.buffer[speaker] = current_text
                                    
                                    # Update last speaker
                                    last_speaker = speaker
                            
                            except Exception as e:
                                continue  # Skip problematic containers
                        
                        time.sleep(0.2)  # Reduced polling interval
                            
                    except Exception as e:
                        if not self.is_running:
                            break
                        time.sleep(0.5)
                        continue
                
                # Improved handling of speaker change
                if (last_speaker and last_speaker != speaker) or \
                (self.buffer.get(speaker) and 
                    len(current_text) > len(self.buffer[speaker]) and 
                    current_text != self.buffer[speaker]):
                    # Write the previous speaker's text
                    abs_time, rel_time = self.get_timestamp()
                    formatted_line = f"{abs_time} | {rel_time} | {last_speaker:8} | {self.buffer.get(last_speaker, '')}\n"
                    file.write(formatted_line)
                    file.flush()

                    # Reset buffer for new speaker
                    self.buffer[speaker] = current_text

                
                # Write footer
                file.write("\n=== Transcription End ===\n")
                file.write(f"Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
            print("Transcription stopped successfully")
            return True
                        
        except Exception as e:
            print("Failed to start transcription:", e)
            return False
