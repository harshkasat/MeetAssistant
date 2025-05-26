from MeetRecording import init_script, recording_script, stop_script
import time


class MeetRecorder:
    def __init__(self, driver):
        self.driver = driver

        self.timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.video_file_name = f"meet_recording_{self.timestamp}.webm"

    def start_recording(self):
        self.driver.execute_script(init_script)

        print("Starting recording...")
        try:
            # Execute the initialization first
            self.driver.execute_script(init_script)
            # Then execute the recording script
            result = self.driver.execute_script(recording_script, self.video_file_name)
            if not result:
                raise Exception("Failed to start recording")
        except Exception as e:
            print(f"Recording error: {str(e)}")
            raise Exception("Failed to start recording")

    def stop_recording(self):
        print("Stopping recording...")
        try:
            self.driver.execute_script(stop_script)
            return self.video_file_name

        except Exception as e:
            print(f"Error stopping recording: {str(e)}")
