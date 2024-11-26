
ENGAGEMENT_PROMPT = "Analyze the transcript and identify engagement levels, \
    focusing on moments of active participation, interaction, or collaboration among participants."


class Engagement:
    def __init__(self, client):
        self.client = client

    async def get_engagement(self):
        try:
            print('1')
            engagements = await self.client.generate_content(questions=ENGAGEMENT_PROMPT)

            if engagements:
                return engagements
        except Exception as e:
            print(f"Failed to generate summary: {e}")
            return None

