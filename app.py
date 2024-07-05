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
        print(st.session_state["file_processed"])

    else:
        st.error("Please select atleast 1 file")

print(st.session_state["file_processed"])


user_query = st.text_input("Enter your message.")
submit_query = st.button("Respond")


reset = st.button("Reset current session memory")
if(reset):
    st.session_state["context"] = ""


if(submit_query):
    print(st.session_state["file_processed"])
    if(st.session_state["file_processed"] == True):
        if(user_query):
            if("context" not in st.session_state):
                st.session_state["context"] = ""
            
            context = st.session_state["context"]

            con_query = contextualize(user_query, context)
            query_response = generate_response(con_query)
            new_context = generate_context(context, con_query, query_response)

            #store new context in session
            st.session_state["context"] = new_context

            st.success(query_response)

        else:
            st.error("Please enter a query!!!")
    else:
        st.error("Please upload and process the file(s) first.")