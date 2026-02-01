from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class AppState:

    def __init__(self,model:dict):
        
        self.model = ChatGroq(**model)