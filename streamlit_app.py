# from app import get_current_daf_name,
import streamlit as st

import requests
import json
from datetime import datetime
from ollama import chat
from ollama import ChatResponse
import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate




CACHE_DIR = "cache"  # Directory to store cached responses

def get_cached_response(daf_name):
    """Retrieves a cached response from a JSON file."""
    cache_file = os.path.join(CACHE_DIR, f"{daf_name}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return None

def cache_response(daf_name, response):
    """Saves the API response to a JSON file."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    cache_file = os.path.join(CACHE_DIR, f"{daf_name}.json")
    with open(cache_file, "w") as f:
        json.dump(response, f)


def generate_prom(Tractate_daf="Baba Batra 166"):
    prompt = f""" **I am studying Talmud Tractate and Daf : {Tractate_daf}.**

**Please provide a comprehensive summary of this Daf, focusing on:**

1. **Background Context:** 
    * Briefly summarize the key discussions and conclusions from the preceding Daf or pages that directly lead into the current Daf's analysis. This should establish the necessary context for understanding the current page's arguments.
2. **Topics and Subtopics:**
    * Clearly outline the main topics and subtopics discussed on the Daf.
    * Use a hierarchical structure (e.g., bullet points, numbered lists) to organize the information logically.
3. **Argument Analysis:**
    * For each topic/subtopic, concisely explain the different opinions presented, the supporting arguments, and any resolutions or conclusions reached.
    * Highlight any key disagreements between different Rabbis or schools of thought.
4. **Key Concepts and Terms:**
    * Identify and define any important concepts, terms, or principles introduced or discussed on the Daf.

**My goal is to use this summary to quickly grasp the core arguments and flow of the Daf, enabling efficient analysis and deeper understanding.**

**Optional additions:**

* **Connections:** If relevant, mention any connections to other areas of Talmud or Jewish law.
* **Modern Applications:** Briefly discuss any potential modern-day applications or relevance of the discussed topics.
"""

    return prompt


def get_current_daf_name():
    # Base URL for Hebcal API
    API_URL = "https://www.hebcal.com/hebcal"

    # Get today's date in ISO format
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        # Send request to the API
        response = requests.get(
            API_URL,
            params={
                "cfg": "json",
                "v": "1",
                "F": "on",
                "start": today,
                "end": today,
            }
        )
        response.raise_for_status()

        # Parse the response

        data = response.json()
        items = data.get("items", [])
        daf_yomi_info = next((item for item in items if item.get("category") == "dafyomi"), None)

        if daf_yomi_info:
            title = daf_yomi_info["title"]
            return title
        else:
            return "Daf Yomi information not found for today."
    except requests.exceptions.RequestException as e:
        return f"Error fetching Daf Yomi: {e}"

# def get_current_daf_name():
#     today = datetime.now().date()
#     days_since_start = (today - DAF_YOMI_START.date()).days
#     current_daf_number = days_since_start % TOTAL_DAFIM
#
#     for tractate, pages in TRACTATES:
#         if current_daf_number < pages:
#             print(tractate,current_daf_number + 2)
#             return tractate, current_daf_number + 2
#         current_daf_number -= pages


def fetch_daf_content():
    daf_name = get_current_daf_name()

    # Check for cached response
    cached_response = get_cached_response(daf_name)
    if cached_response:
        print(f"Using cached response for {daf_name}")
        return cached_response

    prompt = generate_prom(get_current_daf_name())
    print(prompt)

    llm = ChatOllama(
        model="llama3.2",
        temperature=0,
    )
    messages = [
        HumanMessage(
            content=prompt
        )
    ]
    llm.invoke(messages)


    response: ChatResponse = chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    print(response['message']['content'])

    # response = requests.post("http://localhost:11434/api/generate", json=data, stream=False)
    # json_data = json.loads(response.text)
    daf_content = response['message']['content']

    # Cache the response for future use
    cache_response(daf_name, daf_content)

    return daf_content







# Set page config
st.set_page_config(
    page_title="Welcome To your Llama powere Daily Daf",
    page_icon=":book:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        font-family: sans-serif;
        background-color: #ffffff;
        color: #2c3e50;
    }
    .title {
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .caption {
        font-size: 1.2em;
        color: #7f8c8d;
        margin-bottom: 1.5em;
    }
    .stChatContainer {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and caption
st.markdown('<div class="title">Daily Daf</div>', unsafe_allow_html=True)
st.markdown('<div class="caption">Dive into the sea of Talmudic wisdom.</div>', unsafe_allow_html=True)


# "Let's Learn Today's Daf" button
# Streamlit App
st.title("Daf Yomi AI")

# Daf Yomi Summary
if st.button("Let's Learn Today's Daf"):
    with st.spinner('Generating summary...'):

        daf_name = get_current_daf_name()
        st.subheader(f"Today's Daf: {daf_name}")

        # Include email in the request data
        request_data = {'daf_name': daf_name}

        content = fetch_daf_content() # Pass request_data
        if content:
            st.write(content)
