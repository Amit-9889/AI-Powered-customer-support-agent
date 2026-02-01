from langgraph.graph import StateGraph,START,END
from backend.agents.intent_detection_agent import Intent
from backend.Nodes.Validator import intent_validator
from backend.agents.SQL_query_agent import Sql_agent
from backend.Database_utility.Order_query_node import OrderQueryNode
from backend.Database_utility.postgres_db import PostgresDB
from backend.state.LLM_app_state import AppState
from backend.agents.answer_agent import AnswerAgent
from backend.state.agent_state import AgentState
from langchain_groq import ChatGroq

class AgentGraph:

    def __init__(self):
        pass
    ### DB Utility 
    def final_workflow(self):
        
        graph = StateGraph(AgentState)

        db = PostgresDB({
        "host": "localhost",
        "user": "genai_user",
        "password": "genai_pass",
        "database": "genai_db",
        "port": 5432,
        })

        ## LLM utility


        llm =  ChatGroq(model_name="llama-3.3-70b-versatile",temperature=0.3)
        ## Intent detection node
        intent = Intent(llm).intent_agent

        ## User Query validation
        validator = intent_validator().validate_order

        ## SQL Query generator
        sql_generator = Sql_agent(llm).create_sql_query

        ## Database connection and query executor
        sql_executor = OrderQueryNode(db)

        ## Answer node using llm to restructure answer and show to user
        answer = AnswerAgent(llm).answer


        ## Writing conditional method


        def route_after_validator(state:AgentState):

            if not state.get('user_id') or not state.get('order_id'):
                return 'need_info'

            return 'ready'

        ## Now connecting Nodes to graph

        graph.add_node("intent",intent)
        graph.add_node("validator",validator)
        graph.add_node("sql_generator",sql_generator)
        graph.add_node("sql_executor",sql_executor)
        graph.add_node("answer",answer)

        ## Now Connecting Nodes with edges


        graph.add_edge(START,"intent")
        graph.add_edge("intent","validator")
        graph.add_conditional_edges("validator",
                                route_after_validator,{
                                    'need_info':END,
                                    'ready':"sql_generator"
                                }
                                )


        graph.add_edge("sql_generator","sql_executor")
        graph.add_edge("sql_executor","answer")
        graph.add_edge("answer",END)


        workflow = graph.compile()

        return workflow
    #### 
