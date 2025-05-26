SUMMARY_PROMPT = "Summarize the key points discussed in the transcript"


class Summaries:
    def __init__(self, client):
        self.client = client

    async def get_summary(self):
        try:
            summary = await self.client.generate_content(questions=SUMMARY_PROMPT)

            if summary:
                return summary
        except Exception as e:
            print(f"Failed to generate summary: {e}")
            return None
