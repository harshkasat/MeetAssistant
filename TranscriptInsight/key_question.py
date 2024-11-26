
KEY_QUESTIONS_PROMPT = """Your task is to:
1. Identify and list all key questions that arise from the transcript.
   - Focus on questions asked directly by participants or implied in the conversation.
   - Extract questions related to the themes, decisions, or inquiries discussed.
2. Analyze the context to propose additional key questions that should be explored based on the transcript.
   - These can be questions that delve deeper into topics, emotions, or patterns identified.

Ensure your response is:
- Comprehensive, listing all relevant questions explicitly.
- Clear and structured, categorizing direct and additional questions where possible.
- Insightful, highlighting how these questions relate to the transcript's content."""

class KeyQuestions:
    def __init__(self, client):
        self.client = client


    async def get_key_questions(self):
        try:
            print('3')
            key_question = await self.client.generate_content(questions=KEY_QUESTIONS_PROMPT)

            if key_question:
                return key_question
        except Exception as e:
            print(f"Failed to generate summary: {e}")
            return None

