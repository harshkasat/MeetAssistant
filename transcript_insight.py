import asyncio
from Llm.config import ApiClient
from TranscriptInsight.engagement import Engagement
from TranscriptInsight.all_participants import Participants
from TranscriptInsight.key_question import KeyQuestions
from TranscriptInsight.sentimental import SentimentAnalysis
from TranscriptInsight.summaries import Summaries
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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
    ]
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    # Unpack and print results
    engagement, participants, key_questions, sentiment, summary = results

    return (engagement, participants, key_questions, sentiment, summary)

async def get_transcript_pdf(engagement, participants, key_questions, sentiment, summary):    
    # Create a PDF file
    pdf_file = "transcript_insights.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Define starting position
    y_position = height - 50
    line_height = 20  # Space between lines

    # Function to add a section to the PDF
    def add_section(title, content):
        nonlocal y_position
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, y_position, title)
        y_position -= line_height
        c.setFont("Helvetica", 12)
        for line in content.splitlines():
            if y_position < 50:  # Check if we need to create a new page
                c.showPage()
                c.setFont("Helvetica-Bold", 16)
                y_position = height - 50  # Reset position for new page
            c.drawString(100, y_position, line)
            y_position -= line_height

    # Add sections to the PDF
    add_section("Quick Summaries", summary)
    add_section("Participants", str(participants))
    add_section("Engagement", str(engagement))
    add_section("Sentimental Analysis", str(sentiment))
    add_section("Key Questions", str(key_questions))

    # Save the PDF
    c.save()
    print(f"PDF generated: {pdf_file}")



async def async_transcript_insights():
    engagement, participants, key_questions, sentiment, summary = await get_transcript_insights()
    await get_transcript_pdf(engagement, participants, key_questions, sentiment, summary)
