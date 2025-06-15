__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from guide_creator_flow.main import BuildingAssistantFlow, BuildingAssistantState

st.title("Building Management Assistant")

# Initialize the conversation state in Streamlit's session state
if "assistant_state" not in st.session_state:
    st.session_state.assistant_state = BuildingAssistantState()

# Display chat messages from history
for message in st.session_state.assistant_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the inputs for the flow
    inputs = {
        "user_query": prompt,
        "chat_history": st.session_state.assistant_state.chat_history
    }

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            flow = BuildingAssistantFlow()
            final_state = flow.kickoff(inputs=inputs)
            
            # Update the session state with the new state from the flow
            st.session_state.assistant_state = final_state

            # Display the latest assistant response
            response = final_state.chat_history[-1]['content']
            st.markdown(response) 