
TRANSCRIPT_PROMPT = "Please analyze the provided transcript and reformat it to \
    display only the speaker's name and the corresponding text they spoke. The format should be as follows: \
    Speaker Name: Text spoken by the speaker \
    Ensure that the format is consistent, with each speaker's name followed by their dialogue. \
    If no speaker name is provided, label the speaker as 'Unknown'. If there are multiple speakers, \
    list them in the order they appear in the transcript."

class Transcript:
    def __init__(self, client):
        self.client = client


    async def get_transcript(self):
        try:
            print('6')
            transcript = await self.client.generate_content(questions=TRANSCRIPT_PROMPT)

            if transcript:
                return transcript
        except Exception as e:
            print(f"Failed to generate summary: {e}")
            return None

