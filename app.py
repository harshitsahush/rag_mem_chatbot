import streamlit as st
from utils import *


#initialised to know if a file has been uploaded and processed
#remember that the WHOLE script reruns at any action on frontend
if("file_processed" not in st.session_state):
    st.session_state["file_processed"] = False


st.title("RAG Chatbot(with memory)")
st.header("Let's chat!")


pdfs = st.file_uploader("Upload relevant files.", accept_multiple_files = True)
submit_file = st.button("Submit and process files")
if(submit_file):
    if(pdfs):
        st.session_state["file_processed"] = True
        process_files(pdfs)

    else:
        st.error("Please select atleast 1 file")


user_query = st.text_input("Enter your message.")
submit_query = st.button("Respond")


reset = st.button("Reset current session memory")
if(reset):
    st.session_state["chat_history"] = ""


if(submit_query):
    if(st.session_state["file_processed"] == True):
        if(user_query):
            if("chat_history" not in st.session_state):
                st.session_state["chat_history"] = ""
            chat_history = st.session_state["chat_history"]

            #if chat history is empty, no need to contextualize
            if chat_history != "":
                con_query = contextualize(user_query, chat_history)
            else:
                con_query = user_query
                
            sim_docs = sim_search(con_query)
            query_response = generate_response(con_query, sim_docs)
            new_chat_history = generate_chat_history(chat_history, con_query, query_response)

            #store new chat_history in session
            st.session_state["chat_history"] = new_chat_history

            st.success(query_response)

        else:
            st.error("Please enter a query!!!")
    else:
        st.error("Please upload and process the file(s) first.")