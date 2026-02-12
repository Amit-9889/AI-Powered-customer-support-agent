from pinecone import Pinecone,ServerlessSpec
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from typing import List
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from dotenv import load_dotenv
from core.config import PINE_CONE_API,PINE_CONE_INDEX


load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

class vector_db:

    def __init__(self):

        self.pc = Pinecone(api_key=PINE_CONE_API)
        if not self.pc.has_index(PINE_CONE_INDEX):
            self.pc.create_index(
                name = PINE_CONE_INDEX,
                dimension=384,
                metric="cosine",
                spec = ServerlessSpec(cloud="aws",region="us-east-1"),
            )

        self.index = self.pc.Index(PINE_CONE_INDEX)

        self.vector_store = PineconeVectorStore(index=self.index , embedding=embeddings)
        
        
    def ingest(self,document:List[Document]):

        self.uuids = [str(uuid4()) for _ in range(len(document))]
        
        self.vector_store.add_documents(documents=document)

        print("Data inserted into vector store successfully!!!")

    def query(self):

        return self.vector_store



    

        

        

        




        


