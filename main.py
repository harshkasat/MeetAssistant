from Automation.join_meet import MeetConfig
from Automation import create_stealth_driver, extract_meeting_code
import time
import random
import os
import threading
from queue import Queue
from MeetRecording.recording_meet import MeetRecorder
from MeetTranscript.extract_transcription import TranscriptionExtractor
from AwsService.s3_utils import upload_file_to_s3
from transcript_insight import async_transcript_insights


class MeetSession:
    def __init__(self, meet_url):
        self.meet_url = meet_url
        self.driver = None
        self.config_meet = None
        self.start_event = threading.Event()
        self.stop_event = threading.Event()
        self.recording_finished = threading.Event()
        self.transcription_finished = threading.Event()
        self.error_queue = Queue()
        self.video_path = None

    def setup_meet(self):
        try:
            meeting_code = extract_meeting_code(self.meet_url)
            self.driver = create_stealth_driver(meeting_code=meeting_code)
            self.config_meet = MeetConfig(self.driver)
            
            self.driver.get(self.meet_url)
            print("Redirected to Google Meet", self.meet_url)
            time.sleep(3)
            
            self.config_meet.continue_without_mic_video()
            self.config_meet.type_username(random.randint(1000, 9999))
            self.config_meet.ask_join_meet()
            self.config_meet.dismiss_popup()
            self.config_meet.click_on_caption()
            
            return True
        except Exception as e:
            self.error_queue.put(f"Setup error: {str(e)}")
            return False

    def recording_worker(self):
        try:
            recorder = MeetRecorder(driver=self.driver)
            
            # Wait for start signal
            self.start_event.wait()
            
            # Start recording
            recorder.start_recording()
            print("Recording started")
            
            # Wait for stop signal
            self.stop_event.wait()
            
            # Stop recording
            self.video_path = recorder.stop_recording()
            print("Recording stopped")
            
            if self.video_path:
                self.save_recording()
            
            self.recording_finished.set()
        except Exception as e:
            self.error_queue.put(f"Recording error: {str(e)}")

    def transcription_worker(self):
        try:
            transcriber = TranscriptionExtractor(driver=self.driver, transcript_path="transcript.txt")
            
            # Wait for start signal
            self.start_event.wait()
            
            # Start transcription
            transcriber.extract_transcription()
            print("Transcription started")
            
            # Wait for stop signal
            self.stop_event.wait()
            
            # Stop transcription
            transcriber.stop_transcription()
            print("Transcription stopped")
            
            self.transcription_finished.set()
        except Exception as e:
            self.error_queue.put(f"Transcription error: {str(e)}")

    def save_recording(self):
        try:
            recording_path = 'recordings'
            if not os.path.exists(recording_path):
                os.makedirs(recording_path)

            full_video_path = os.path.join(recording_path, self.video_path)
            
            if os.path.exists(full_video_path):
                upload_file_to_s3(full_video_path, f"meet_{self.video_path}.webm")
                print(f"Video uploaded to S3: {self.video_path}")
            else:
                print(f"Video file not found: {full_video_path}")
        except Exception as e:
            self.error_queue.put(f"Save recording error: {str(e)}")

    def run(self):
        try:
            if not self.setup_meet():
                return False

            # Create worker threads
            recording_thread = threading.Thread(target=self.recording_worker)
            transcription_thread = threading.Thread(target=self.transcription_worker)

            # Start threads (they will wait for the start event)
            recording_thread.start()
            transcription_thread.start()

            # Signal both threads to start simultaneously
            self.start_event.set()
            print("Recording and transcription started simultaneously")

            # Monitor participant count
            while not self.config_meet.check_num_participants():
                if not self.error_queue.empty():
                    raise Exception(self.error_queue.get())
                time.sleep(1)

            # Signal both threads to stop simultaneously
            self.stop_event.set()
            print("Signaling recording and transcription to stop")

            # Wait for both processes to finish
            recording_thread.join(timeout=10)
            transcription_thread.join(timeout=10)

            # Check for any errors
            if not self.error_queue.empty():
                raise Exception(self.error_queue.get())

            return True

        except Exception as e:
            print(f"Session error: {str(e)}")
            return False
        finally:
            if self.config_meet:
                self.config_meet.leave_meet()
            if self.driver:
                self.driver.quit()
            if os.path.exists('transcript.txt'):
                async_transcript_insights()

def google_meet(meet_url: str):
    session = MeetSession(meet_url)
    return session.run()