
SENTIMENT_ANALYSIS_PROMPT = "Perform a sentiment analysis of the transcript. \
    Identify and rate the sentiment of each sentence or phrase, noting instances with particularly high or low sentiment. \
    Additionally, provide an overall sentiment rating for the entire transcript."

class SentimentAnalysis:
    def __init__(self, client):
        self.client = client


    async def get_sentiment_analysis(self):
        try:
            sentiment = await self.client.generate_content(questions=SENTIMENT_ANALYSIS_PROMPT)

            if sentiment:
                return sentiment
        except Exception as e:
            print(f"Failed to generate summary: {e}")
            return None

