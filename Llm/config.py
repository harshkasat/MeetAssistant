import asyncio
import google.generativeai as genai
from Llm import genai_api_key, text


# Initialize the API client
class ApiClient():
            
    async def configure_llm(self):
        try:
            genai.configure(api_key=genai_api_key)
            llm = genai.GenerativeModel('models/gemini-1.5-flash',
                        system_instruction=text)            

            if llm is None:
                raise ValueError("LLM component is None")
            return llm
        except Exception as e:
            print(f"Failed to configure LLM: {e}")
            return None

    async def generate_content(self, questions:str) -> str:
        try:
            llm = await self.configure_llm()
            response = await llm.generate_content_async(questions)
            if response is None:
                raise ValueError("Response is None")
            return response.text
        except Exception as e:
            print(f"Failed to generate content: {e}")
            return None