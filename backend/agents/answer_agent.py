from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from backend.state.agent_state import AgentState
from dotenv import load_dotenv

load_dotenv()

class AnswerAgent:

    def __init__(self,model):
        self.model = model


    def answer(self,state:AgentState):

        prompt = PromptTemplate(template="""You are an great explainer,
                                 you have to analyse the given question:{question} , and database result {db_result}the corresponding to that.
                                and generate clear,meaningful,concrete summary.""",
                                input_variables=['question','db_result'])
        
        final_prompt = prompt.format(**{'question':state['question'],'db_result':state['db_result']})

        answer = self.model.invoke(final_prompt).content

        
        return {"answer":answer}
