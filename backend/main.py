from backend.graph.app import AgentGraph
from backend.state.agent_state import AgentState


def state_respons(state:AgentState):

    for key,value in state.items():
        print(f"{key}--: {value}")
    

if __name__ == "__main__":

    workflow = AgentGraph().final_workflow()

    output = workflow.invoke({'question':"Status of order with orderid PC12345","user_id":"3"})

    # print(output)

    state_respons(output)
    
    