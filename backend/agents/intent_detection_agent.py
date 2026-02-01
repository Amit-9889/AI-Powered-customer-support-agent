from dotenv import load_dotenv
from langchain_core.messages import SystemMessage,HumanMessage
from backend.state.agent_state import AgentState
import json
load_dotenv()

class Intent:

    def __init__(self,model):
        self.model = model


    def intent_agent(self,state:AgentState):

        messages = [SystemMessage(
            content="""
        You are a strict Intent classification engine.
        
        Critical Rule:
        
        -Only classify as ORDER if the user message clearly refers to a specific, user-owned order or payment.
        -If a message implies an order-related issue (e.g delivery delay) but does not include an order ID, you may still classify it as ORDER, but confidence should be below 0.85 
        -If there is any doubt , choose HUMAN

        Intent definitions:
            - ORDER: Mentions a specific order, transaction, payment, shipment, or personal ownership (e.g., "my order", order ID, tracking, payment made).
            - POLICY: Asks about rules, terms, eligibility, or general policies without referring to a specific order.
            - HUMAN: General questions, hypothetical cases, or unclear intent.
                       
        Output format (JSON Only):
        {
        "intent":ORDER | POLICY | HUMAN,
        "confidence": number between 0.0 and 1.0
        }

        Confidence guidelines:
        - 0.9–1.0: Explicit ownership or order ID
        - 0.7–0.85: Clear ownership but no ID
        - <0.6: Ambiguous or hypothetical

        Do not answer the user.
        Do not explain reasoning.
        """),
       
       HumanMessage(content=state['question'])
        ]

        ## Invoking model with above question

        model_output = self.model.invoke(messages).content

        # print("User Question:" , state['question'])

        #print("Intent detected: ",model_output)

        #state["intent"] = model_output["intent"]

        ## converting output json-string into Pure json
        
        try:
            result = json.loads(model_output)

        except json.JSONDecodeError:
            result = {"intent":"HUMAN","confidence":0.0}

        intent = result.get("intent","HUMAN")
        
        #state["intent"] = intent
        return {
            "intent":intent
        }




# ## Calling method for testing

# intent_obj = Intent()

# ## Ask query

# query = {"My order #458921 hasn’t been delivered yet. Can you check the status":{"intent": "ORDER_QUERY","confidence": "≥ 0.9"},
#          "What is your return and refund policy for electronic items?":{"intent": "POLICY_QUERY","confidence": "≥ 0.9"},"How long does delivery usually take?":{"intent": "POLICY_QUERY",
# "confidence": "~0.7 ", "intent": "AMBIGUOUS acceptable"},"I paid yesterday but my order is still showing processing.":{"intent": "ORDER_QUERY",
# "confidence": "≥ 0.85"},"If I cancel my order now, will I get a full refund?":{"intent": "ORDER_QUERY", "confidence": "~0.7–0.8"},
# "Hi, I placed an order last Friday (#782341). I got the confirmation email, but since then there’s been no update at all. Can you tell me where it is":{"intent":"order_status"},
# "I paid using UPI yesterday and the amount was deducted, but my order is still marked as processing. Is something wrong?":{"intent":"order_payment"},"Implicit delivery delay":{"intent":"order"},
# "I placed two orders on Monday, canceled one on Tuesday, but today I got a shipment message. Which order is this for?":{"intent":"ORDER_TRACKING ORDER_CANCELLATION_VERIFICATION"},
# "Your policy says refunds take 5–7 days, but my last refund took 12. My current order is canceled—should I expect the same delay?":{"intent":"REFUND_STATUS POLICY_EXCEPTIONORDER_CANCELLATION_CONFIRMED"}}
                                                                                                                              

# i = 0
# for key,val in query.items():
#     print(f"Agent answer of question {i} -----\n",intent_obj.intent_agent({"question":key}))
    

#     print(f"Actual answer of {i} question\n",val)

#     i+=1
          


