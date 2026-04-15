import streamlit as st
from app.graph import app
import uuid

# 1. Page Configuration
st.set_page_config(page_title="HotelAgent AI", page_icon="🏨", layout="wide")

# 2. Sidebar - Control Center
with st.sidebar:
    st.title("⚙️ Agent Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info("Agent: Gemini 2.5 Flash + SerpApi\n\nStatus: Online")

st.title("🏨 AI Travel Assistant")
st.caption("Precision hotel discovery powered by Multi-Agent Orchestration")

# 3. Initialize Session State (Using the clean setdefault pattern)
st.session_state.setdefault("messages", [])

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The Chat Loop
if prompt := st.chat_input("Ex: Find a hotel in Tirupati for $100 with WiFi"):
    
    # Store and display user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Processing
    with st.chat_message("assistant"):
        # st.status provides the 'Chain of Thought' visibility
        with st.status("🚀 Agent starting...", expanded=True) as status:
            
            # Initial state for LangGraph
            initial_state = {
                "user_requirements": prompt,
                "hotels": [],
                "location": "",
                "max_budget": 0,
                "notes": "",
                "loop_count": 0
            }
            
            try:
                # Running the graph
                st.write("🔍 Refining requirements...")
                # Note: stream=True can be used here for even more detail
                final_state = app.invoke(initial_state)
                
                if final_state.get("hotels"):
                    st.write(f"✅ Found {len(final_state['hotels'])} hotels in {final_state['location']}")
                
                status.update(label="Search Complete!", state="complete", expanded=False)
                
                # Extract the final AI response
                response = final_state.get("notes", "⚠️ I processed the request but couldn't generate a report.")
                
            except Exception as e:
                status.update(label="Error occurred", state="error")
                response = f"❌ **System Error:** {str(e)}"
        
        # Display and Save the Final Response
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})