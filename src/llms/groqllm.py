from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv


class GroqLLM:
    def __init__(self):
        load_dotenv()
    
    def get_llm(self):
        try:
            os.environ["GROQ_API_KEY"] = self.groq_api_key = os.getenv("GROQ_API_KEY")
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=self.groq_api_key)
            return llm
        except Exception as e:
            print(f"Error: {e}")
            return None
        