from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def levenshtein_distance(s1, s2):
    """Calculate the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


class TranscriptionExtractor:
    def __init__(self, driver, transcript_path, similarity_threshold=0.7):
        self.driver = driver
        self.transcript_path = transcript_path
        self.is_running = False
        self.start_time = None
        self.last_complete_sentence = ""
        self.buffer = {}  # Store buffer per speaker
        self.similarity_threshold = similarity_threshold

    def calculate_similarity(self, text1, text2):
        """Calculate similarity ratio between two strings using Levenshtein distance."""
        if not text1 or not text2:
            return 0.0

        distance = levenshtein_distance(text1, text2)
        max_length = max(len(text1), len(text2))
        similarity = 1 - (distance / max_length)
        return similarity

    def is_text_significantly_different(self, text1, text2):
        """Determine if two texts are significantly different based on similarity threshold."""
        similarity = self.calculate_similarity(text1, text2)
        return similarity < self.similarity_threshold

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
        relative_time = f"{relative_seconds // 60:02d}:{relative_seconds % 60:02d}"

        return absolute_time, relative_time

    def extract_transcription(self):
        try:
            self.is_running = True
            last_speaker = None

            with open(self.transcript_path, "w", encoding="utf-8") as file:
                file.write("=== Transcription Start ===\n")
                file.write(
                    f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )
                file.write("Time  | Elapsed | Speaker | Text\n")
                file.write("-" * 70 + "\n")

                while self.is_running:
                    try:
                        caption_containers = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "div.nMcdL.bj4p3b")
                            )
                        )

                        for container in caption_containers:
                            try:
                                try:
                                    speaker = container.find_element(
                                        By.CSS_SELECTOR, "div.KcIKyf.jxFHg"
                                    ).text
                                except:
                                    speaker = "Unknown"

                                spans = container.find_elements(
                                    By.CSS_SELECTOR, "div.bh44bd.VbkSUe span"
                                )
                                current_text = " ".join(
                                    span.text for span in spans
                                ).strip()

                                if current_text:
                                    if speaker not in self.buffer:
                                        self.buffer[speaker] = ""

                                    # Check if the text is significantly different using Levenshtein distance
                                    is_different = self.is_text_significantly_different(
                                        current_text, self.buffer[speaker]
                                    )

                                    if (last_speaker and last_speaker != speaker) or (
                                        self.buffer[speaker] and is_different
                                    ):
                                        abs_time, rel_time = self.get_timestamp()
                                        formatted_line = f"{abs_time} | {rel_time} | {last_speaker:8} | {self.buffer.get(last_speaker, '')}\n"
                                        file.write(formatted_line)
                                        file.flush()

                                        self.buffer[speaker] = current_text
                                    else:
                                        # Update buffer only if new text is longer
                                        if len(current_text) > len(
                                            self.buffer[speaker]
                                        ):
                                            self.buffer[speaker] = current_text

                                    last_speaker = speaker

                            except Exception as e:
                                continue

                        time.sleep(0.2)

                    except Exception as e:
                        if not self.is_running:
                            break
                        time.sleep(0.5)
                        continue

                # Write final buffer contents
                if last_speaker and self.buffer.get(last_speaker):
                    abs_time, rel_time = self.get_timestamp()
                    formatted_line = f"{abs_time} | {rel_time} | {last_speaker:8} | {self.buffer[last_speaker]}\n"
                    file.write(formatted_line)
                    file.flush()

                # Write footer
                file.write("\n=== Transcription End ===\n")
                file.write(
                    f"Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )

            print("Transcription stopped successfully")
            return True

        except Exception as e:
            print("Failed to start transcription:", e)
            return False
