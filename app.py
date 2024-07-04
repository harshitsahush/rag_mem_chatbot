import streamlit as st
from utils import *

st.title("Chatbot(with memory)")
st.header("Let's chat!")

user_query = st.text_input("Enter your message.")
submit = st.button("Respond")

reset = st.button("Reset current session")
if(reset):
    st.session_state["context"] = ""

if(submit):
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