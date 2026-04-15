from app.graph import app
import sys

def get_travel_details():
    """
    Acts as the 'Receptionist' to gather all necessary data 
    before the AI agents start working.
    """
    print("\n--- 📝 TRAVELER QUESTIONNAIRE ---")
    print("Please provide the following details for a precise search:\n")
    
    details = {}
    details['location'] = input("📍 1. Where exactly do you want to stay? (City/Neighborhood): ")
    details['dates'] = input("📅 2. When are you planning to go? (Check-in to Check-out dates): ")
    details['days'] = input("⏳ 3. For how many days is your stay?: ")
    details['budget'] = input("💰 4. What is your total budget in USD? (e.g., 300): ")
    details['guests'] = input("👥 5. How many guests (Adults/Children)?: ")
    details['amenities'] = input("✨ 6. Any must-haves? (WiFi, Pool, AC, Breakfast, etc.): ")
    details['extra'] = input("📝 7. Any other specific requests? (Near beach, quiet area, etc.): ")
    
    # Synthesize everything into one powerful master requirement string
    master_query = (
        f"Location: {details['location']}, Dates: {details['dates']}, Duration: {details['days']} days, "
        f"Budget: ${details['budget']}, Guests: {details['guests']}, "
        f"Requirements: {details['amenities']}, Extra Notes: {details['extra']}"
    )
    return master_query

def run_hotel_agent(synthesized_query: str):
    print(f"\n🚀 Agent is now analyzing your full profile...")
    
    inputs = {
        "user_requirements": synthesized_query,
        "hotels": [],      
        "notes": "",       
        "location": "",    
        "max_budget": 0,   
        "loop_count": 0    
    }
    
    config = {"recursion_limit": 20}
    
    try:
        # The graph now receives a perfect, detailed prompt
        final_state = app.invoke(inputs, config=config)
        
        print("\n" + "="*60)
        print("🏨 YOUR PERSONALIZED TOP RECOMMENDATION:")
        print(final_state.get("notes", "Sorry, I couldn't find a suitable hotel with these criteria."))
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ An error occurred during search: {e}")

if __name__ == "__main__":
    print("--- 🏨 WELCOME TO YOUR PREMIUM AI TRAVEL ASSISTANT ---")
    print("I will ask a few questions to ensure I find exactly what you need.")
    
    while True:
        menu = input("\nReady to start a new search? (yes/exit): ").lower()
        
        if menu in ['exit', 'quit', 'no']:
            print("Safe travels! Goodbye. 👋")
            break
        
        if menu == 'yes':
            # Step 1: Human-to-Human Interview
            synthesized_query = get_travel_details()
            
            # Step 2: Agent-to-API Search
            run_hotel_agent(synthesized_query)
        else:
            print("Please type 'yes' to start or 'exit' to leave.")