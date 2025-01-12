import streamlit as st
import openai
from googlesearch import search
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Ensure the API key is available
if not openai_api_key:
    st.error("API Key not found. Please set OPENAI_API_KEY in the .env file.")
else:
    openai.api_key = openai_api_key

# Function to fetch GPT-4 response
def get_openai_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            temperature=1.0,
            max_tokens=2048,
            messages=[
                {"role": "system", "content": "You are an assistant providing concise answers with links to sources."},
                {"role": "user", "content": query},
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function to fetch search results
def get_search_results(query, num_results=5):
    try:
        return [link for link in search(query, num_results=num_results)]
    except Exception as e:
        return [f"Error: {str(e)}"]

# Streamlit App UI
st.title("AI-Powered Search Engine with Sources")

# Input field for the query
user_query = st.text_input("Enter your query:")

if user_query:
    # Get the AI-generated response
    with st.spinner("Generating AI response..."):
        ai_response = get_openai_response(user_query)
    st.subheader("AI-Generated Response")
    st.write(ai_response)

    # Get related sources
    with st.spinner("Fetching sources..."):
        sources = get_search_results(user_query)
    
    st.subheader("Sources")
    for i, link in enumerate(sources, start=1):
        st.markdown(f"[Source {i}]({link})")

st.write("Powered by OpenAI GPT-4 and Google Search")
