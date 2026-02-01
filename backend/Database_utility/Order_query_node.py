from backend.Database_utility.postgres_db import PostgresDB
from backend.state.agent_state import AgentState

class OrderQueryNode:

    def __init__(self,db: PostgresDB):
        self.db = db

    def __call__(self,state:AgentState):


        result = self.db.fetch_one(
            state['sql_query'],
    
        )

        return {"db_result":result}