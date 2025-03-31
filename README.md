# AI-Powered-Workflow-Assistant
A chat-based productivity tool built for a hackathon, leveraging IBM watsonx.ai's Granite-13B-Instruct model and Streamlit for a sleek frontend. This assistant helps users prioritize tasks, summarize meetings, and generate follow-up emails—all in a simple, interactive interface

## Features
- Task Prioritization: Input a task list with deadlines, get a prioritized order with reasoning.
- Meeting Summarization: Paste a meeting transcript, receive a concise 2-3 sentence summary.
- Follow-Up Generation: Request an email follow-up, get a professional, actionable draft.
- Document Summarization : Input a document ,get an summarized version of it.


## Tech Stack
- Backend: IBM watsonx.ai (Granite-13B-instruct-v2 model)
- Frontend: Streamlit (Python-based web app)

## Prerequisites
- Python 3.8+
- An IBM Cloud account with watsonx.ai access
- API key and Project ID from watsonx.ai (see IBM Cloud Docs)

## Setup
1. Clone the Repository:
`git clone https://github.com/JeevaKS03/Ai-Powered-Workflow-Assistant
cd ai-workflow-assistant`

2. Install Dependencies:
`pip install -r requirements.txt`

3. Configure watsonx.ai Credentials:
- Open app.py and replace the placeholders:
-- API_KEY = "your-api-key-here"
-- URL = "your-server-url"  
-- PROJECT_ID = "your-project-id-here"

4. Run the App:
`streamlit run app.py`
- Open your browser to http://localhost:8501 to use the assistant.
