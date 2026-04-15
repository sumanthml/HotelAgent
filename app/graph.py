from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.nodes import requirements_processor, hotel_searcher, hotel_reviewer

def should_continue(state: AgentState):
    """
    The Router: Decides if we need to search again or finish.
    """
    # We only stop if the reviewer has generated a final report in 'notes'
    # and the searcher has actually found hotels.
    found_hotels = len(state.get("hotels", [])) > 0
    has_final_report = bool(state.get("notes")) and "Hotel" in state.get("notes", "")
    current_loops = state.get("loop_count", 0)
    
    print(f"--- ROUTER: Hotels Found: {found_hotels} | Loops: {current_loops} ---")
    
    # If we have a report, we are done.
    if has_final_report:
        return "end"
    
    # If we found nothing and haven't hit the limit, try searching one more time
    if not found_hotels and current_loops < 2:
        print("--- ROUTER: No hotels found. Retrying search... ---")
        return "continue"
    
    # Default to ending to prevent infinite API calls
    return "end"

# Initialize the Graph
workflow = StateGraph(AgentState)

# Define the Nodes
workflow.add_node("processor", requirements_processor)
workflow.add_node("searcher", hotel_searcher)
workflow.add_node("reviewer", hotel_reviewer)

# Define the Flow
workflow.set_entry_point("processor")

# Step 1: Process the 7-point questionnaire
workflow.add_edge("processor", "searcher")

# Step 2: Search for hotels using SerpApi
workflow.add_edge("searcher", "reviewer")

# Step 3: Review the findings and decide whether to stop or retry
workflow.add_conditional_edges(
    "reviewer",
    should_continue,
    {
        "end": END,
        "continue": "searcher"
    }
)

# Compile the final app
app = workflow.compile()