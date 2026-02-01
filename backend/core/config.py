from dotenv import load_dotenv
import os

load_dotenv()


PINE_CONE_API = os.getenv("PINECONE_API_KEY")
PINE_CONE_INDEX = os.getenv("PINECONE_INDEX")
