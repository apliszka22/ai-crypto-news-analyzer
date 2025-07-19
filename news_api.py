# news_api.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY") # Free API key available @ https://newsapi.org/


class News:
    def __init__(self, crypto_topic):
        self.crypto_topic = crypto_topic

    def get_news(self):
        """Fetch news articles about the crypto topic"""
        try:
            url = (f"https://newsapi.org/v2/everything?q={self.crypto_topic}&"
                   f"sortBy=publishedAt&apiKey={API_KEY}&language=en")

            print(f"Fetching news for: {self.crypto_topic}")

            response = requests.get(url)
            response.raise_for_status()

            content = response.json()

            if content.get('status') == 'ok' and content.get('articles'):
                # Extract descriptions, filter out None values
                articles = []
                for article in content['articles']:
                    description = article.get('description')
                    if description and description.strip():
                        articles.append(description)

                print(f"Successfully fetched {len(articles)} articles")
                return articles
            else:
                print(f"No articles found for {self.crypto_topic}")
                return []

        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def get_full_articles(self):
        """Get full article data (title, description, url, etc.) for future use"""
        try:
            url = (f"https://newsapi.org/v2/everything?q={self.crypto_topic}&"
                   f"sortBy=publishedAt&apiKey={API_KEY}&language=en")

            response = requests.get(url)
            response.raise_for_status()

            content = response.json()

            if content.get('status') == 'ok':
                return content.get('articles', [])
            else:
                return []

        except Exception as e:
            print(f"Error fetching full articles: {e}")
            return []


# Test the news API independently
if __name__ == '__main__':


    # Test with different crypto topics
    for crypto in ['bitcoin', 'binance', 'cardano']:
        print(f"\n--- Testing {crypto.upper()} news ---")
        news = News(crypto)
        articles = news.get_news()
        if articles:
            print(f"Found {len(articles)} articles")
            print(f"Sample: {articles[0][:100]}...")
        else:
            print("No articles found")