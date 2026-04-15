import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from serpapi import GoogleSearch
from app.state import AgentState

# Load environment variables
load_dotenv()

# Using Gemini 1.5 Flash for high-speed agentic processing
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def requirements_processor(state: AgentState):
    print("\n--- NODE: REFINING TRAVELER PROFILE ---")
    
    # Updated prompt to handle the complex 7-point input from main.py
    prompt = f"""
    Analyze this synthesized traveler profile: "{state['user_requirements']}"
    
    Extract and refine:
    1. LOCATION: A specific, searchable path (e.g., 'Poonamallee, Chennai, Tamil Nadu').
    2. BUDGET_USD: The total budget number only.
    3. SEARCH_QUERY: A specialized string for Google Hotels (e.g., 'luxury hotels in Chennai with wifi and pool').
    
    Format EXACTLY as:
    LOCATION: [Value]
    BUDGET_USD: [Value]
    QUERY: [Value]
    """
    
    response = llm.invoke(prompt)
    content = response.content.strip()

    loc_match = re.search(r"LOCATION:\s*(.*)", content, re.IGNORECASE)
    price_match = re.search(r"BUDGET_USD:\s*(\d+)", content, re.IGNORECASE)
    query_match = re.search(r"QUERY:\s*(.*)", content, re.IGNORECASE)

    refined_location = loc_match.group(1).strip() if loc_match else state['user_requirements']
    budget_usd = int(price_match.group(1)) if price_match else 200
    search_query = query_match.group(1).strip() if query_match else f"hotels in {refined_location}"

    print(f"--- DEBUG: Search Query optimized to: '{search_query}' ---")

    return {
        "location": refined_location, 
        "max_budget": budget_usd,
        "hotels": [], 
        "notes": search_query, # Temporarily passing query through notes to searcher
        "loop_count": 0
    }

def hotel_searcher(state: AgentState):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return {"hotels": [], "notes": "CRITICAL ERROR: SERPAPI_KEY MISSING"}

    # Dynamic Dates for the search
    check_in = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    check_out = (datetime.now() + timedelta(days=9)).strftime('%Y-%m-%d')

    print(f"--- NODE: EXECUTING LIVE SEARCH FOR {state['location']} ---")
    
    # We use the specialized query generated in the previous node
    params = {
        "engine": "google_hotels",
        "q": state.get("notes", f"hotels in {state['location']}"),
        "check_in_date": check_in,
        "check_out_date": check_out,
        "api_key": api_key,
        "currency": "USD", # Using USD for standardized filtering
        "gl": "us",
        "hl": "en"
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            print(f"--- SERPAPI ERROR: {results['error']} ---")
            return {"hotels": []}

        # Grabbing all valid properties
        hotels = results.get("properties", []) or results.get("other_hotels", [])
        print(f"--- DEBUG: Live Data Secured. Found {len(hotels)} properties. ---")

    except Exception as e:
        print(f"--- CONNECTION ERROR: {e} ---")
        hotels = []

    return {
        "hotels": hotels[:10], 
        "loop_count": state.get("loop_count", 0) + 1,
        "notes": "" # Clear the query for the reviewer
    }

def hotel_reviewer(state: AgentState):
    print("--- NODE: GENERATING TOP 5 RECOMMENDATIONS ---")
    
    hotels = state.get('hotels', [])
    budget = state.get('max_budget', 500)
    
    if not hotels:
        return {"notes": f"❌ No hotels found matching your specific criteria in {state['location']}."}
    
    # Filter by price before passing to AI
    valid_hotels = []
    for h in hotels:
        rate = h.get("rate_per_night", {}).get("lowest", "")
        if rate:
            price_val = int("".join(filter(str.isdigit, rate)))
            if price_val <= budget:
                valid_hotels.append(h)

    # If no hotels in budget, use the top 3 regardless to show user options
    source_list = valid_hotels[:5] if valid_hotels else hotels[:5]
    
    prompt = f"""
    User Requirements: {state['user_requirements']}
    
    Top Hotels Found:
    {source_list}
    
    TASK: Provide a detailed breakdown of the TOP 5 HOTELS.
    For each hotel, include:
    1. Full Name
    2. Exact Price per night
    3. Rating and Review count
    4. Key Amenities (WiFi, Pool, etc.)
    5. A 1-sentence 'Pro-Tip' why this is a good choice.
    
    Format the response clearly with bold headings and bullet points.
    """
    
    response = llm.invoke(prompt)
    return {"notes": response.content.strip()}