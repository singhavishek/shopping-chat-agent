import streamlit as st
from src.chatbot import ShoppingAgent
import time

st.set_page_config(page_title="Mobile Shopping Assistant", page_icon="📱", layout="wide")

st.title("📱 Mobile Shopping Assistant")
st.markdown("Ask me about mobile phones! I can help you find, compare, and choose the best phone for you.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize agent
if "agent" not in st.session_state:
    try:
        st.session_state.agent = ShoppingAgent()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.info("Please add your GROQ_API_KEY to the .env file.")
        st.stop()
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        st.stop()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What are you looking for?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.send_message(prompt)
                
                # Simulate typing effect
                for chunk in response.split(" "):
                    full_response += chunk + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(response)
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                message_placeholder.markdown(error_msg)
                response = error_msg
                
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This agent uses **Google Gemini** to help you shop for mobile phones.
    
    **Features:**
    - Search by price, brand, specs
    - Compare models
    - Get detailed specs
    
    **Example Queries:**
    - "Best camera phone under 30k"
    - "Compare Pixel 8a and OnePlus 12R"
    - "Show me Samsung phones"
    """)
    
    if st.button("Reset Chat"):
        st.session_state.messages = []
        # Re-initialize agent to clear its internal history if needed
        # st.session_state.agent = ShoppingAgent() 
        st.rerun()
