import google.generativeai as genai
from google.cloud import bigquery
import pandas as pd
import os

genai.configure(api_key= os.environ.get("API_KEY"))

EMBEDDING_MODEL = "models/text-embedding-004"
GENERATIVE_MODEL = "gemini-1.5-pro"
REGION = "europe-west2"

#Following code will fetch the datatables and the schema
gcp_dataset = "thelook_ecommerce"
table_name = f"`bigquery-public-data.{gcp_dataset}.INFORMATION_SCHEMA.TABLES`"

ddl_query = f"""
SELECT table_name, ddl
FROM {table_name}
WHERE table_type = 'BASE TABLE'
ORDER BY table_name;
"""

client = bigquery.Client(project= os.environ.get("PROJECT_ID"))
ddl_query_result = client.query_and_wait(query = ddl_query)
ddl_result = dict(ddl_query_result)

#Intitating model and chat
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
chat = model.start_chat(history=[])


def get_llm_response(question:str, context_history):
    """
    This functin will take chat history and question from the user in the argument and it returns the response from the llm.
    """
    prompt = f'''You are a very helpful bot who act as an analyst to write sql query.
        User will ask database related question and you will return the query as a response using following datatables and ddl statements. Here is the schema with ddl: {ddl_result}.
        Use the chat history for a context and refer to the latest items if possible. Here is the history of the chat: {context_history}
        Answer the following question using the schema provided and if you are not clear about question, ask to provide more information. {question}
        Note: Never use Delete, Update, Drop command. Try to avoid selecting all columns by using *. Also, give meaningful name to caculated columns as much as possible. '''
    
    response = chat.send_message(prompt, stream = True)
    response_clean = "".join([item.text for item in response])
    
    return response_clean


def get_query_result(sql_query):
    """
    This function will take sql query and send it to the Data warehouse and returns the result
    """
    sql_query = sql_query.replace("```","").replace('sql',"").replace("\n"," ")
    
    query_result = client.query_and_wait(query= sql_query).to_dataframe()
     
    return  query_result