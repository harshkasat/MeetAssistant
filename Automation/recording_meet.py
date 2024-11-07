import os
import psutil
import random
import subprocess
import threading

class RecordMeet:
    def __init__(self, window_title: str = None, audio_device: str = "Microphone (Realtek(R) Audio)", output_dir: str = "recordings"):
        self.window_title = window_title
        self.random_num = random.randint(1000, 9999)
        self.output_dir = output_dir
        self.video_file_name = f"{self.output_dir}/{window_title}_{self.random_num}.mp4"
        self.audio_device = audio_device
        self.ffmpeg_command = self._build_ffmpeg_command()
        self.process = None
        self.recording_thread = None

    def _build_ffmpeg_command(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        return [
            "ffmpeg",
            "-y",
            "-f", "dshow",
            "-i", f"audio={self.audio_device}",
            "-f", "gdigrab",
            "-framerate", "60",
            "-video_size", "1920x1020",  # Set the screen capture resolution to 1920x1020
            "-i", "desktop",
            "-acodec", "aac",
            "-strict", "experimental",
            "-ac", "1",
            "-b:a", "64k",
            "-vcodec", "libx264",
            "-b:v", "300k",
            "-r", "30",
            "-g", "30",
            self.video_file_name
        ]

    def start_recording(self):
        print("Starting screen recording with audio...")
        self.recording_thread = threading.Thread(target=self._run_ffmpeg)
        self.recording_thread.start()

    def _run_ffmpeg(self):
        try:
            self.process = subprocess.Popen(self.ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print("Screen recording with audio started.")
            ps_process = psutil.Process(self.process.pid)
            # self.process.wait()  # Wait for the FFmpeg process to complete
        except subprocess.CalledProcessError as e:
            print(f"Error starting recording: {e}")

    def stop_recording(self):
        if self.process and self.process.poll() is None:
            print("Stopping recording...")
            self.process.stdin.write(b'q')  # Simulate user pressing q key for gracefully closing FFmpeg.
            self.process.communicate()
            self.process.wait()
            # self.process.wait()
            print("Screen recording with audio stopped.")
        else:
            print("FFmpeg process is not running.")

# if __name__ == '__main__':
#     recording_meet = RecordMeet(window_title="MyMeeting")
#     recording_meet.start_recording()
#     time.sleep(15)
#     recording_meet.stop_recording()
