import streamlit as st
import openai
from googlesearch import search  # For web search results
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to fetch GPT-4 response
def get_openai_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=1.0,  # Controls randomness
            max_tokens=2048,  # Limit response length
            messages=[
                {"role": "system", "content": "You are an assistant providing concise answers with links to sources."},
                {"role": "user", "content": query},
            ]
        )
        answer = response['choices'][0]['message']['content']
        return answer
    except Exception as e:
        return f"Error fetching GPT-4 response: {str(e)}"

# Function to fetch search results
def get_search_results(query, num_results=5):
    try:
        links = [link for link in search(query, num_results=num_results)]
        return links
    except Exception as e:
        return [f"Error fetching search results: {str(e)}"]

# Streamlit App Interface
st.title("AI-Powered Search Engine with Sources")

# Input field for user query
user_query = st.text_input("Enter your query:")

if user_query:
    # Fetch GPT-4 response
    with st.spinner("Generating AI response..."):
        ai_response = get_openai_response(user_query)
    st.subheader("AI-Generated Response")
    st.write(ai_response)

    # Fetch search results
    with st.spinner("Fetching sources..."):
        sources = get_search_results(user_query)

    st.subheader("Sources")
    for i, link in enumerate(sources, 1):
        st.markdown(f"[Source {i}]({link})")

st.write("Powered by OpenAI GPT-4 and Google Search")
