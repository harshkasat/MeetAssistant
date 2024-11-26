
PARTICIPANTS_PROMPT = "Identify all participants involved in the conversation from the transcript,\
    listing their names if provided; if a name is not available, label the participant as Unknown, \
    and present the results as a bullet-point list."

class Participants:
    def __init__(self, client):
        self.client = client


    async def get_participants(self):
        try:
            participants = await self.client.generate_content(questions=PARTICIPANTS_PROMPT)

            if participants:
                return participants
        except Exception as e:
            print(f"Failed to generate summary: {e}")
            return None

