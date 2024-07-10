import streamlit as st


logo_url = "media/Dax_11zon.png"
st.sidebar.image(logo_url)

st.title("Data Analytics :blue[X] AI")
st.subheader("Your personal data analyst powerd by AI :sunglasses:")

# setting up side bar
with st.sidebar:

    llm = st.radio("Select LLM model:",
             options=["Gemini", "GPT 4"])
    
    
    llm_api_key =  st.text_input(
        f"{llm} API Key:", 
        key = "API_key",
        type="password"
    )
    
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})