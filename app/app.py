import streamlit as st
import backend

logo_url = "media/Dax_11zon.png"
#st.sidebar.image(logo_url)


st.title("Data Analytics :blue[X] AI")
st.subheader("Your personal data analyst powered by AI :sunglasses:")

# setting up side bar
with st.sidebar:

    st.image(logo_url)
    st.divider()

    st.subheader("Wanna talk to your AI analyst!")
    st.subheader("Follow the steps to get started :rocket:")

    st.divider()

    llm = st.selectbox("Step 1: Select LLM model:",
            ("Gemini", "GPT 4"))
    
    
    llm_api_key =  st.text_input(
        f"Step 2: Enter {llm} API Key:", 
        key = "API_key",
        type="password"
    )
    
    "Don't have key? No worries! Go to following link and create one."
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[Get Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)"

    dataset = st.selectbox("Step 3: Select a dataset!",
                           ("Ecommerce dataset",  "Energy dataset"))

    st.divider()

    st.subheader("You're all set!! Ask a question. :point_right:")

# Set api key


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input(f'''Looking for insight about {dataset}?'''):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Sending request to llm API
    llm_response = backend.get_llm_response(question= prompt, context_history= st.session_state.messages)

    #Sending query to DWH for result
    try:
        dwh_reponse = backend.get_query_result(sql_query= llm_response)
    except:
        dwh_reponse = "Sorry, I can't get the data. Need more information. Please try again!"
     
    # response = f"AI: {llm_response}"
    # catch errors from bigquery 
    response = llm_response
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
        if isinstance(dwh_reponse,str):
            st.markdown(dwh_reponse) 
        else:
            st.dataframe(dwh_reponse)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})