import asyncio
from Llm.config import ApiClient
from TranscriptInsight.engagement import Engagement
from TranscriptInsight.all_participants import Participants
from TranscriptInsight.key_question import KeyQuestions
from TranscriptInsight.sentimental import SentimentAnalysis
from TranscriptInsight.summaries import Summaries
from TranscriptInsight.transcript import Transcript


async def get_transcript_insights():
    # Create a client instance
    client = ApiClient()
    
    # Create a list of tasks to run asynchronously
    tasks = [
        Engagement(client).get_engagement(),
        Participants(client).get_participants(),
        KeyQuestions(client).get_key_questions(),
        SentimentAnalysis(client).get_sentiment_analysis(),
        Summaries(client).get_summary(),
        Transcript(client).get_transcript(),
    ]
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    # Unpack and print results
    engagement, participants, key_questions, sentiment, summary, transcript = results
    print(f"Engagement: {engagement}\n")
    print(f"Participants: {participants}\n")
    print(f"Key Questions: {key_questions}\n")
    print(f"Sentiment: {sentiment}\n")
    print(f"Summary: {summary}\n")
    print(f"Transcript: {transcript}\n")

    return (engagement, participants, key_questions, sentiment, summary)

async def get_transcript_pdf():
    # TODO: Implement this function to download the transcript PDF
    pass

# async def main():
#     await get_transcript_insights()

async def run_transcript_insights():
    await get_transcript_insights()




# if __name__ == "__main__":
#     asyncio.run(main())  # Run the main async function
