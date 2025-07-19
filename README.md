# 📈 Crypto News Analyzer

A modern, no-hype tool to analyze cryptocurrency news using AI.  
Built with Python, Ollama, and Gradio, this app scrapes real-time crypto articles and uses an LLM to assess market 
sentiment and predict short-term trends.

---

## 🚀 Features

- 🔍 AI-driven sentiment analysis (Positive / Negative / Neutral)
- 📊 Predictive market direction (Bullish / Bearish / Neutral)
- 🎯 Confidence scoring with rationale
- 🌐 Fetches real-time crypto news using [NewsAPI.org](https://newsapi.org/)
- 🧠 Powered by [Ollama](https://ollama.com/) and LLaMA-based models
- 💻 Clean Gradio web interface for ease of use

---

## 🛠 Requirements

- Python 3.9+
- An [Ollama](https://ollama.com/) runtime installed and running
- A model pulled via Ollama (e.g., `llama3.1:8b`)
- Free API key from [NewsAPI.org](https://newsapi.org/)

---

## 📦 Installation

1. Clone the repository:

   git clone https://github.com/apliszka22/ai-crypto-news-analyzer.git
   cd crypto-news-analyzer

2. Install dependencies:

   pip install -r requirements.txt

3. Set up your .env file:

    NEWS_API_KEY=your_newsapi_key_here

4. Pull the AI model:
    
    ollama pull llama3.1:8b

Run the App
python main.py

Models are run locally using Ollama — no cloud GPU required.
The app analyzes up to 50 recent news articles for a given crypto.
If no results are returned, try a broader crypto name or verify model/API status.

✨ Credits
Built with 🧠 by Adam Pliszka 
LLMs powered by Ollama
News courtesy of NewsAPI

    
