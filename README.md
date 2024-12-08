# Daf Yomi AI 

This project provides a daily summary of the Daf Yomi using an external LLM API.

## Features
* Fetches the current Daf Yomi from the Hebcal API.
* Generates a concise and insightful summary using an LLM.
* Displays the summary in a user-friendly web interface using Streamlit.

## Installation
1. Clone the repository: `git clone https://github.com/moshesham/DafYomi_AI.git`
2. Create a virtual environment: `bash venv.sh`
3. Install requirements: `pip install -r requirements.txt`

## Usage
1. Make sure your LLM API is running (e.g., Ollama).
2. Run the Streamlit app: `streamlit run steamlit_app.py`
3. Click the "Let's Learn Today's Daf" button to generate and view the summary.

## Configuration
* You can customize the Streamlit UI in `steamlit_app.py`.

## Contributing
Contributions are welcome! Feel free to open issues and pull requests.

## Run it locally

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```
