from backend.state.agent_state import AgentState
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class Sql_agent:

    def __init__(self,model):
        self.model = model

    def create_sql_query(self,state:AgentState):

        ### Checking 
        
        prompt_template = PromptTemplate(

        input_variables=["question", "user_id", "order_id","intent"],
        template="""
        You are a SQL query generator for a production backend system.

        CRITICAL SECURITY RULES (must never be violated):
        - Generate ONLY a single READ-ONLY SELECT statement.
        - NEVER generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, MERGE, COMMIT, or ROLLBACK.
        - NEVER modify or manipulate database data.
        - NEVER generate SQL without BOTH `order_id` and `user_id`.
        - ALWAYS enforce ownership by filtering on BOTH `order_id` AND `user_id`.
        - NEVER use SELECT *.
        - NEVER access any table other than `users` and `orders`.
        - NEVER infer or guess missing values.
        - The original user query is for CONTEXT.
        - Check if 'intent' is "ORDER" only then generate SQL query.
        - Return 'order_id' in every select sql query

        Database schema:

        users(
        user_id BIGINT PRIMARY KEY,
        name VARCHAR,
        email VARCHAR,
        )

        orders(
        id BIGINT PRIMARY KEY,
        user_id BIGINT,
        status VARCHAR,
        order_date TIMESTAMP,
        order_id VARCHAR
        )

        intent:
        "{intent}"

        User query (for reference that what user wants):
        "{question}"

        Resolved Inputs (authoritative — must be used as-is):
        - user_id: {user_id}
        - order_id: {order_id}

        Task:
        Generate a safe, read-only SQL query to fetch order details.

        Output requirements:
        - Output VALID SQL only.
        - No explanations.
        - No comments.
        - No formatting text.
        """
        )

        final_prompt = prompt_template.format(

            question = state['question'],
            user_id = state['user_id'],
            order_id = state['order_id'],
            intent = state['intent'],
            
        )

        output = self.model.invoke(final_prompt).content

        return {'sql_query':output}
        



