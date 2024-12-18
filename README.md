# MeetAssistant: Automated Google Meet Transcription and Recording

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/harshkasat/MeetAssistant/actions/workflows/main.yml/badge.svg)](https://github.com/harshkasat/MeetAssistant/actions)


## 1. Project Title and Short Description

MeetAssistant is a Python-based automation tool that joins Google Meet meetings, records the session, transcribes the audio, and generates insightful reports based on the transcription.  It leverages Selenium for browser automation, and integrates with AWS S3 for storing recordings and potentially other services for transcription analysis (LLM integration suggested but not fully implemented in provided code).


## 2. Project Overview

MeetAssistant automates the process of attending, recording, and transcribing Google Meet sessions. This eliminates the manual effort involved in these tasks, providing a streamlined workflow for users who frequently participate in online meetings.  The tool's key differentiator is its ability to generate insightful reports analyzing meeting engagement, participant activity, key questions asked, sentiment analysis, and summaries. This feature is partially implemented, relying on an external API (LLM) for deeper analysis.


## 3. Table of Contents

* [Project Title and Short Description](#project-title-and-short-description)
* [Project Overview](#project-overview)
* [Table of Contents](#table-of-contents)
* [Prerequisites](#prerequisites)
* [Installation Guide](#installation-guide)
* [Configuration](#configuration)
* [Usage Examples](#usage-examples)
* [Project Architecture](#project-architecture)
* [API Reference](#api-reference)
* [Contributing Guidelines](#contributing-guidelines)
* [Testing](#testing)
* [Deployment](#deployment)
* [License](#license)


## 4. Prerequisites

* **Python 3.7+:** The project is built using Python.
* **Dependencies:**  The `requirements.txt` file lists all necessary Python packages.  Install them using `pip install -r requirements.txt`.
* **ChromeDriver:** Selenium requires a compatible ChromeDriver. Download the appropriate version for your Chrome browser.  The project uses `undetected-chromedriver` to help evade detection.
* **AWS Credentials (Optional):**  For S3 integration, configure AWS access keys.
* **LLM API Key (Optional):**  The transcription insight generation relies on an LLM API (not specified in the provided code) and requires an API key.


## 5. Installation Guide

1. **Clone the repository:** `git clone https://github.com/harshkasat/MeetAssistant.git`
2. **Navigate to the directory:** `cd MeetAssistant`
3. **Install dependencies:** `pip install -r requirements.txt`
4. **Download ChromeDriver:** Download the appropriate version from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) and place it in your system's PATH or specify the path in the code.
5. **Configure AWS (Optional):** Set up AWS credentials using environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION).


## 6. Configuration

The primary configuration is done through environment variables (if using AWS) and potentially through an external configuration file (not explicitly defined in the code).  The Google Meet URL is passed as an argument to the `google_meet` function.

## 7. Usage Examples

The core functionality is accessed through the `extension_api.py` which exposes a FastAPI endpoint.  The  `google_meet` function in `main.py` handles the meeting joining, recording, and transcription.

**Example (using the FastAPI endpoint):**

Send a POST request to `/new-meeting` with the Google Meet URL in the `meetUrl` field:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"meetUrl": "https://meet.google.com/abc-defg-hij"}' http://localhost:8000/new-meeting
```

**Example (from `main.py` -  not intended for direct use):**

```python
from main import google_meet

google_meet("https://meet.google.com/abc-defg-hij") #Starts the process
```


The `google_meet` function uses threading to run recording and transcription concurrently. The `start_stop_recording` function in `main.py` handles recording using `MeetRecorder`, and `start_stop_transcription` handles transcription using `TranscriptionExtractor`.  These functions interact with the Selenium driver to control the browser.  Error handling is present but could be improved.



## 8. Project Architecture

The project is structured into several modules:

* **Automation:** Contains functions for joining and interacting with Google Meet.
* **AwsService:** Handles interaction with AWS S3 for storing recordings.
* **Llm:** (Partially implemented) Intended for interaction with an LLM API for advanced transcript analysis.
* **MeetRecording:**  Handles the recording of the meeting.
* **MeetTranscript:** Handles transcription extraction.
* **TranscriptInsight:** (Partially implemented)  Processes the transcription to generate insights (engagement, participants, key questions, sentiment, summaries).  Uses `reportlab` to generate a PDF report.
* **extension_api:**  Provides a FastAPI web server for external interaction.


## 9. API Reference

The project exposes a REST API via FastAPI:

* **Endpoint:** `/new-meeting`
* **Method:** `POST`
* **Request Body:**  `{"meetUrl": "https://meet.google.com/your-meeting-code"}`
* **Response:**  A JSON object indicating success or failure.


## 10.  Contributing Guidelines

Contributions are welcome!  Please open issues for bug reports and feature requests.  Follow standard GitHub pull request procedures.  A code of conduct and detailed contribution guidelines are not explicitly defined in the provided files.


## 11. Testing

Testing is not explicitly implemented in the provided code.


## 12. Deployment

The project can be deployed using uvicorn (for the FastAPI server) and Docker (suggested by the presence of `run_docker.sh` and `stop_docker.sh`).  Deployment instructions are not detailed.


## 13. Security

Security considerations are not explicitly addressed in the provided documentation.  Use of `undetected-chromedriver` suggests an attempt to evade detection, but further security measures are needed.


## 14. License

The project is licensed under the MIT License.  (See LICENSE file).


## 15. Acknowledgments

No explicit acknowledgments are provided in the code.


## 16. Contact and Support

No explicit contact information is provided.


This README provides a comprehensive overview based on the provided code and files.  Many sections require further development and detail within the project itself.
