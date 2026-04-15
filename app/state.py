from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    # The raw synthesized string from the 7-point questionnaire
    user_requirements: str
    
    # The AI-refined specific location (e.g., 'Poonamallee, Chennai')
    location: str
    
    # The integer budget extracted for filtering
    max_budget: int
    
    # Annotated with operator.add so that if the searcher runs twice, 
    # it keeps all results in one big list for the reviewer.
    hotels: Annotated[List[dict], operator.add]
    
    # Used for the AI's final formatted report (Top 3 Hotels)
    notes: str
    
    # Internal system logs for debugging
    logs: str
    
    # Tracks search attempts to prevent hitting SerpApi limits
    loop_count: int