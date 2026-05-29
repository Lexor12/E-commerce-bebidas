import os
from groq import Groq
from app.domain.ports.faq_port import FAQPort
from typing import Optional
from dotenv import load_dotenv
from app.domain.prompts.prompt import SYSTEM_PROMPT

load_dotenv()

class GroqRepository(FAQPort):
    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        
    def get_answer(self, question: str) -> Optional[str]:
        try:
            response=self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except:
            return None;