from groq import Groq

def contextualize(query, context):
    #contextualizes the query wrt to context and returns it
    client = Groq(api_key = "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")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role" : "system",
                "content" : """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question  which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is. Return just the reformulated question, without any notes."""
            },

            {
                "role" : "user",
                "content" : "Chat history is : " + context + "\n\n" + "Latest user question is : " + query
            }
        ],
        model="llama3-70b-8192"
    )

    return chat_completion.choices[0].message.content

def generate_response(con_query):
    #calls groq and creates a response
    client = Groq(api_key = "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")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role" : "system",
                "content" : """You are a very helpful assistant. Given a standalone question, generate the appropriate answer of the question """
            },

            {
                "role" : "user",
                "content" : con_query
            }
        ],
        model="llama3-70b-8192"
    )

    return chat_completion.choices[0].message.content

def generate_context(old_context, query, response):
    #creates new context by sending old_context, query, response to groq_api
    client = Groq(api_key = "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")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role" : "system",
                "content" : """Given a chat history and the latest user question which might reference context in the chat history and the appropriate answer, formulate a new updated standalone chat history which has all the data of the older chat history, the user question and the answer."""
            },

            {
                "role" : "user",
                "content" : "Old chat history : " + old_context + "\n\n User question :" + query + "\n\n Answer :" + response
            }
        ],
        model="llama3-70b-8192"
    )

    return chat_completion.choices[0].message.content