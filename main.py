from Automation.join_meet import JoinMeet
from Automation import create_stealth_driver
import time
import random
import os
from Automation.recording_meet import RecordMeet

from AwsService.s3_utils import upload_file_to_s3


def create_random_number():
    return random.randint(1000, 9999)


def stop_recording(recorder):
    recorder = RecordMeet
    recorder.stop_screen_recording(recording_process=recorder)

def google_meet(meet_url: str = None, leave_meet: bool = False):
    try:
        driver = create_stealth_driver()
        join_meet = JoinMeet(driver)
        random_num = create_random_number()
            
        driver.get(meet_url)
        print("Redriected to Google Meet", meet_url)
        time.sleep(3)
        join_meet.continue_without_mic_video()
        join_meet.type_username(random_num)
        join_meet.ask_join_meet()
        window_title = driver.title
        print("Window title:", window_title)
        # Start recording
        recording_meet = RecordMeet(window_title=window_title)
        recording_meet.start_recording()  
        time.sleep(15)
        
        if leave_meet:
            # Stop recording
            recording_meet.stop_recording()
            video_path = recording_meet.video_file_name  # Get the path to the recorded video
            time.sleep(1)
            
            # Upload file to S3 if it exists
            if os.path.exists(video_path):
                # upload_file_to_s3(video_path, s3_key=f"recordings/{random_num}.mp4")
                print("Recording uploaded to S3")
            else:
                print("No recording data found")
                
            print("Recording stopped")
            join_meet.leave_meet()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == '__main__':
    google_meet(meet_url="https://meet.google.com/qdm-hrsb-haw", leave_meet=True)