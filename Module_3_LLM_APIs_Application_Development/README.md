# Module 3: LLM APIs & Application Development

> **Codomax Gen AI Internship — Day 11 to Day 15**  
> Priority: High

---

## 📌 Overview

This module dives deep into **LLM API integration** using Python. You will learn how to authenticate with LLM providers, manage multi-turn conversations, handle errors robustly, optimize token usage and cost, and finally build a **full-featured AI Chat Application** with a polished web UI.

---

## 🎯 Learning Objectives

| Topic | Description |
|-------|-------------|
| LLM Authentication | API keys, environment variables, `.env` files |
| Python LLM Client | Wrapping Gemini / OpenAI APIs in reusable classes |
| Chat History | Managing system, user, and assistant message roles |
| Conversation Context | Maintaining multi-turn context across requests |
| Model Parameters | Temperature, max_tokens, top_p, frequency_penalty |
| Token Usage | Counting tokens and estimating API costs |
| Structured Responses | Forcing JSON output and parsing structured data |
| Error Handling | Retry logic, rate limit handling, graceful degradation |
| Cost Management | Per-request token tracking and budget warnings |
| AI Chat Application | End-to-end web UI with history and custom instructions |

---

## 📁 Repository Structure

```
Module_3_LLM_APIs_Application_Development/
│
├── README.md                          ← This file
├── requirements.txt                   ← Python dependencies
├── .env.example                       ← Environment variable template
│
├── notebooks/
│   └── Module3_LLM_APIs.ipynb         ← Main Colab notebook (full walkthrough)
│
├── src/
│   ├── llm_client.py                  ← Core LLM API wrapper (Gemini + OpenAI)
│   ├── chat_history.py                ← Conversation history manager
│   ├── structured_responses.py        ← JSON / structured output helpers
│   └── cost_tracker.py               ← Token usage & cost estimation
│
└── app/
    ├── index.html                     ← AI Chat web application UI
    ├── style.css                      ← Dark-mode glassmorphism styles
    └── app.js                         ← Chat logic, API calls, history management
```

---

## 🚀 Getting Started

### Option 1: Google Colab (Recommended)

1. Open the notebook: [Module3_LLM_APIs.ipynb](./notebooks/Module3_LLM_APIs.ipynb)
2. Click `File → Open in Colab`
3. Add your API key as a Colab Secret named `GEMINI_API_KEY`
4. Run all cells from top to bottom

### Option 2: Local Setup

```bash
# 1. Clone and navigate
cd Module_3_LLM_APIs_Application_Development

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env and add your API key

# 4. Run the notebook
jupyter notebook notebooks/Module3_LLM_APIs.ipynb

# 5. Open the web app
# Simply open app/index.html in your browser
```

---

## 🌐 AI Chat Application Features

The web app (`app/`) provides:

- 💬 **Multi-turn chat** with full conversation history
- 🧠 **Custom system instructions** to set AI persona
- 📊 **Token usage tracker** displayed in real time
- 🌙 **Dark-mode glassmorphism UI** — premium look & feel
- ⚙️ **Model parameter controls** — temperature slider
- 🔄 **Clear history** button to reset conversation
- ⚠️ **Error handling** with user-friendly messages
- 📋 **Copy response** button for quick access

---

## 📦 Submission Deliverables

- [x] GitHub Repository Link
- [x] Live Website Link
- [ ] LinkedIn Post Link

---

## 🛠️ Tools & Technologies

- **Google Gemini API** (`google-generativeai`)
- **OpenAI API** (`openai`) — optional
- **Python 3.10+**
- **Google Colab / Jupyter Notebooks**
- **HTML5 + CSS3 + Vanilla JavaScript** (web app)
- **python-dotenv** (environment management)

---

## 📚 Key Concepts Covered

### 1. API Authentication
```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```

### 2. Message Roles
```python
history = [
    {"role": "user",      "parts": ["Hello, who are you?"]},
    {"role": "model",     "parts": ["I am Gemini, an AI assistant."]},
]
```

### 3. Structured JSON Response
```python
response = model.generate_content(
    "Return a JSON object with name, age, and skills fields."
)
```

### 4. Token Usage Tracking
```python
usage = response.usage_metadata
print(f"Prompt tokens: {usage.prompt_token_count}")
print(f"Output tokens: {usage.candidates_token_count}")
```

---

## 👤 Author

**Codomax Gen AI Internship — Module 3**  
Completed: October 2026
