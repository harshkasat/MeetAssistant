from Automation.join_meet import MeetConfig
from Automation import create_stealth_driver, extract_meeting_code
import time
import random
import os
import threading
from MeetRecording.recording_meet import MeetRecorder
from MeetTranscript.extract_transcription import TranscriptionExtractor
from AwsService.s3_utils import upload_file_to_s3


def create_random_number():
    return random.randint(1000, 9999)


def meet_config(driver, meet_url: str = None):
    
    try:
        config_meet = MeetConfig(driver)
        random_num = create_random_number()

        driver.get(meet_url)
        print("Redirected to Google Meet", meet_url)
        time.sleep(3)
        config_meet.continue_without_mic_video()
        config_meet.type_username(random_num)
        config_meet.ask_join_meet()
        config_meet.dismiss_popup()
        config_meet.click_on_caption()
        
        return config_meet
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()  # Print the full stack trace 
    
def saving_meet_recording(video_path):
    try:
        # Verify the Recording path video file exists # 
        recording_path = 'recordings'
        if not os.path.exists(recording_path):
            os.makedirs(recording_path)

        if video_path:  # Only proceed if video_path is not None
            full_video_path = os.path.join(recording_path, video_path)
            print(f"Video path: {full_video_path}")
        
        time.sleep(2)
        # Verify the full path video file exists
        if os.path.exists(full_video_path):
            # Upload video to S3
            try:
                upload_file_to_s3(full_video_path, f"meet_{video_path}.webm") 
                print(f"Video uploaded to S3: {video_path}")
            except Exception as s3_error:
                print(f"Error uploading video to S3: {s3_error}")
        else:
            print(f"Video file does not exist: {full_video_path}")
    except Exception as record_error:
        print(f"Error during recording stop: {record_error}")
        raise # Re-raise the exception to see the full error stack


def start_stop_recording(driver, config_meet, leave_meet: bool = False ):
    try:
        recording_meet = MeetRecorder(driver=driver)
        # Start Recording
        recording_meet.start_recording()

        while not config_meet.check_num_participants():
            time.sleep(1)
        else:
            leave_meet = True

        if leave_meet:
            try:
                # Stop Recording
                video_path = recording_meet.stop_recording()
                if video_path:  # Only proceed if video_path is not None
                    saving_meet_recording(video_path)
            except Exception as record_error:
                print(f"Error during recording stop: {record_error}")
                raise # Re-raise the exception to see the full error stack
        return video_path
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()  # Print the full stack trace

def start_stop_transcription(driver, transcript_path: str = "transcript.txt"):
    try:
        transcription_extractor = TranscriptionExtractor(driver=driver, transcript_path=transcript_path)
        transcription_extractor.extract_transcription()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()  # Print the full stack trace


def google_meet(meet_url: str = None, leave_meet: bool = False):
    try:
        meeting_code = extract_meeting_code(meet_url)
        driver = create_stealth_driver(meeting_code=meeting_code)

        # Start Meet
        config_meet = meet_config(driver, meet_url)

        # Initialize transcription
        transcription_extractor = TranscriptionExtractor(driver=driver, transcript_path="transcript.txt")
        
        # Create threads for both recording and transcription
        def recording_task():
            try:
                video_path = start_stop_recording(driver=driver, leave_meet=leave_meet, config_meet=config_meet)
                setattr(threading.current_thread(), 'video_path', video_path)
            except Exception as e:
                print(f"Error in recording thread: {e}")
        
        recording_thread = threading.Thread(target=recording_task)
        transcription_thread = threading.Thread(target=transcription_extractor.extract_transcription)

        # Start threads
        print("Starting recording and transcription concurrently...")
        recording_thread.start()
        transcription_thread.start()

        # Monitor participant count
        while not config_meet.check_num_participants():
            time.sleep(1)

        # Stop threads after meeting ends
        recording_thread.join(timeout=5)
        transcription_thread.join(timeout=5)

        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if 'transcription_extractor' in locals():
            transcription_extractor.stop_transcription()
        if 'config_meet' in locals():
            config_meet.leave_meet()
        if 'driver' in locals():
            driver.quit()
