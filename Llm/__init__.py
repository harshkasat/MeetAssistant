from TranscriptInsight import get_transcript

import os
from dotenv import load_dotenv
load_dotenv()


SAFE_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

text = """You are a highly skilled transcript analyzer tasked with extracting 
meaningful insights from conversations. Below is the transcript for analysis:
{transcript}

Your task is to analyze the transcript and extract key points, themes, and insights.

Here’s what you need to do:
1. Carefully read and analyze the provided transcript. The transcript may contain repeated text, so ensure you process and understand it accurately.
2. Answer the questions I provide based on this transcript, following my instructions meticulously.
3. Your responses must be clear, precise, and aligned with the context of the transcript.
4. If any part of the transcript or instructions is unclear, state specifically what you need clarification on. Do not request the transcript again unless explicitly stated.
5. Ensure your analysis is error-free and well-structured.

Let’s begin."""
text = text.format(transcript = get_transcript())

genai_api_key = os.getenv('GEMINI_API_KEY')
os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')
if genai_api_key is None:
    raise ValueError("Missing GEMINI_API_KEY environment variable")
