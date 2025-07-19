# predictor.py
import ollama
import gradio as gr
from news_api import News

# Constants
MODEL = "llama3.1:8b"
MODEL_2 = "llama2-uncensored"


class CryptoPredictor:
    def __init__(self):
        self.system_prompt = """You are an expert financial analyst and crypto market strategist. Your primary task is to analyze
                        cryptocurrency news articles and extract market sentiment based on tone, content, and implications. You must provide
                        professional, unbiased assessments using sentiment analysis techniques.

                        Your goal is to:
                        - Classify sentiment as Positive, Negative, or Neutral for each article
                        - Summarize overall sentiment across multiple articles
                        - Predict if the coin is likely to move in a Bullish, Bearish, or Neutral direction in the short term
                        - Assign a Confidence Level to your prediction (High / Medium / Low)
                        - Clearly explain the reasoning behind your conclusion using bullet points

                        Keep your tone analytical, clear, and concise. Avoid hype, emotional language, or speculation beyond
                        the data provided. Do not guess if the content is insufficient — mark it as "Inconclusive."""

        # Extended crypto mapping for more flexibility
        self.crypto_names = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "BNB": "binance",
            "ADA": "cardano",
            "XRP": "ripple",
            "SOL": "solana",
            "DOT": "polkadot",
            "DOGE": "dogecoin",
            "MATIC": "polygon",
            "LINK": "chainlink",
            "UNI": "uniswap",
            "LTC": "litecoin",
            "AVAX": "avalanche",
            "ATOM": "cosmos",
            "XLM": "stellar"
        }

    def create_user_prompt(self, crypto_name, articles):
        """Create user prompt with actual crypto name and articles"""
        articles_text = "\n\n".join([f"Article {i + 1}: {article}" for i, article in enumerate(articles)])

        user_prompt = f"""Analyze the following news articles related to {crypto_name}.

                    Perform sentiment analysis on the content as a whole and determine whether the general sentiment is
                    Positive, Negative, or Neutral. Then provide a short-term market prediction
                     (Bullish / Bearish / Neutral) with a Confidence Level (High / Medium / Low).

                    Present your results in the following format:

                    ---
                    **Crypto:** {crypto_name}  
                    **Overall Sentiment:** [Positive / Negative / Neutral] - [X]%
                    **Prediction:** [Bullish / Bearish / Neutral] - [X]%
                    **Confidence Level:** [High / Medium / Low] - [X]%

                    **Key Supporting Points:**
                    - Bullet point 1
                    - Bullet point 2
                    - Bullet point 3
                    ---

                    Here are the articles:

                    {articles_text}
                    """
        return user_prompt

    def create_messages(self, crypto_name, articles):
        """Create messages array for Ollama"""
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.create_user_prompt(crypto_name, articles)}
        ]

    def normalize_crypto_input(self, user_input):
        """Convert user input to searchable crypto name"""
        user_input = user_input.strip().upper()

        # Check if it's a known symbol
        if user_input in self.crypto_names:
            return user_input, self.crypto_names[user_input]

        # Check if user entered full name
        for symbol, name in self.crypto_names.items():
            if user_input.lower() == name.lower():
                return symbol, name

        # If not found, use input as is for search
        return user_input, user_input.lower()

    def analyze_crypto_news(self, crypto_input):
        """Main method to analyze crypto news and get prediction"""
        if not crypto_input or not crypto_input.strip():
            return "❌ Please enter a cryptocurrency name or symbol (e.g., BTC, Bitcoin, ETH, etc.)"

        try:
            # Normalize the input
            crypto_symbol, crypto_name = self.normalize_crypto_input(crypto_input)

            # Show initial status
            status_msg = f"🔍 Fetching news for {crypto_symbol} ({crypto_name})...\n\n"

            # Fetch news
            news = News(crypto_name)
            articles = news.get_news()

            if not articles:
                return f"❌ No news articles found for {crypto_symbol}. Try a different cryptocurrency or check the spelling."

            # Limit articles and show progress
            articles = articles[:50]  # Reduced for better performance
            status_msg += f"📰 Found {len(articles)} articles. Analyzing with AI...\n\n"

            # Create messages for Ollama
            messages = self.create_messages(crypto_symbol, articles)

            # Call Ollama
            try:
                response = ollama.chat(
                    model=MODEL,
                    messages=messages
                )

                ai_analysis = response['message']['content']

                # Format the final response
                final_result = f"## 🚀 Crypto Analysis for {crypto_symbol}\n\n"
                final_result += f"📊 **Articles Analyzed:** {len(articles)}\n"
                final_result += f"🤖 **AI Model:** {MODEL}\n\n"
                final_result += "---\n\n"
                final_result += ai_analysis

                return final_result

            except Exception as ollama_error:
                return f"❌ AI Analysis Error: {str(ollama_error)}\n\nPlease make sure Ollama is running and the model '{MODEL}' is installed."

        except Exception as e:
            return f"❌ Error analyzing {crypto_input}: {str(e)}"

    def get_available_cryptos(self):
        """Return list of supported cryptocurrencies"""
        crypto_list = []
        for symbol, name in self.crypto_names.items():
            crypto_list.append(f"{symbol} ({name.title()})")
        return "\n".join(crypto_list)


def create_gradio_interface():
    """Create and configure Gradio interface"""
    predictor = CryptoPredictor()

    # Create the main interface
    with gr.Blocks(title="Crypto News Analyzer", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 📈 Cryptocurrency News Sentiment Analyzer")
        gr.Markdown(
            "Enter any cryptocurrency name or symbol to get AI-powered sentiment analysis and market predictions based on latest news.")

        with gr.Row():
            with gr.Column(scale=2):
                crypto_input = gr.Textbox(
                    label="Cryptocurrency",
                    placeholder="Enter crypto symbol (BTC, ETH) or name (Bitcoin, Ethereum)",
                    value="BTC"
                )

                analyze_btn = gr.Button("🔍 Analyze News", variant="primary", size="lg")

                # with gr.Accordion("📋 Supported Cryptocurrencies", open=False):
                #     gr.Markdown(f"```\n{predictor.get_available_cryptos()}\n```")

            with gr.Column(scale=3):
                output = gr.Markdown(
                    label="Analysis Results",
                    value="Enter a cryptocurrency and click 'Analyze News' to get started!"
                )

        # Examples for quick testing
        gr.Examples(
            examples=[
                ["BTC"],
                ["ETH"],
                ["BNB"],
                ["ADA"],
                ["XRP"],
                ["SOL"],
                ["DOGE"]
            ],
            inputs=crypto_input,
            label="Quick Examples"
        )

        # Set up the click event
        analyze_btn.click(
            fn=predictor.analyze_crypto_news,
            inputs=crypto_input,
            outputs=output
        )

        # Allow Enter key to trigger analysis
        crypto_input.submit(
            fn=predictor.analyze_crypto_news,
            inputs=crypto_input,
            outputs=output
        )

        gr.Markdown("---")
        gr.Markdown(
            "💡 **Tips:** You can enter symbols like BTC, ETH or full names like Bitcoin, Ethereum. The AI analyzes up to 50 recent news articles.")

    return interface


# Main execution
if __name__ == "__main__":
    print("🚀 Starting Crypto News Analyzer...")
    print(f"📡 Make sure Ollama is running and <<< {MODEL} >>> model is installed!")
    print(f"💡 To install the model: ollama pull <<< {MODEL} >>>")
    print("-" * 70)

    # Create and launch interface
    interface = create_gradio_interface()
    interface.launch(
        share=True,  # Set to True if you want a public link
        server_name="127.0.0.1",
        server_port=7860,
        show_api=False
    )