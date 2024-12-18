import asyncio
from Llm.config import ApiClient
from TranscriptInsight.engagement import Engagement
from TranscriptInsight.all_participants import Participants
from TranscriptInsight.key_question import KeyQuestions
from TranscriptInsight.sentimental import SentimentAnalysis
from TranscriptInsight.summaries import Summaries
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


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


async def generate_pdf(engagement, participants, key_questions, sentiment, summary):
    # Create a PDF document
    pdf_file = "transcript_insights.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=20,
    )
    section_title_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=colors.darkblue,
        spaceAfter=10,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=12,
        leading=16,
        spaceAfter=10,
    )

    # PDF content
    content = []

    # Add title
    content.append(Paragraph("Transcript Insights Report", title_style))
    content.append(Spacer(1, 12))

    # Add summary
    content.append(Paragraph("Quick Summaries", section_title_style))
    content.append(Paragraph(summary, body_style))
    content.append(Spacer(1, 12))

    # Add participants
    content.append(Paragraph("Participants", section_title_style))
    participant_list = "<br />".join([f"• {participant}" for participant in participants])
    content.append(Paragraph(participant_list, body_style))
    content.append(Spacer(1, 12))

    # Add engagement
    content.append(Paragraph("Engagement", section_title_style))
    content.append(Paragraph(engagement, body_style))
    content.append(Spacer(1, 12))

    # Add sentiment analysis
    content.append(Paragraph("Sentimental Analysis", section_title_style))
    sentiment_table_data = [["Aspect", "Analysis"]]
    for aspect, analysis in sentiment.items():
        sentiment_table_data.append([aspect, analysis])

    table = Table(sentiment_table_data, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    content.append(table)
    content.append(Spacer(1, 12))

    # Add key questions
    content.append(Paragraph("Key Questions", section_title_style))
    question_list = "<br />".join([f"• {question}" for question in key_questions])
    content.append(Paragraph(question_list, body_style))
    content.append(Spacer(1, 12))

    # Build PDF
    doc.build(content)
    print(f"PDF generated: {pdf_file}")

async def async_transcript_insights():
    engagement, participants, key_questions, sentiment, summary = await get_transcript_insights()
    await generate_pdf(engagement, participants, key_questions, sentiment, summary)
