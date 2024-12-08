import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# API keys for the new services
NEWS_API_KEY = "d78f0a5978844825bbe9414dcf9234d9"
ALPHA_VANTAGE_API_KEY = "8USSUHG9CIPYSADT"

# Function to fetch articles using News API
def fetch_articles_news_api(topic, days):
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': topic,
        'from': from_date,
        'sortBy': 'publishedAt',
        'apiKey': NEWS_API_KEY,
        'language': 'en',
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = []
        for article in data.get('articles', []):
            # Fetch full text using the link
            full_text = fetch_article_text(article['url'])
            articles.append({
                'date': article['publishedAt'],
                'link': article['url'],
                'text': full_text or (article['title'] + " " + (article['description'] or ""))  # Fallback to title + description
            })
        return articles
    else:
        print(f"Failed to fetch data from News API: {response.status_code}")
        return []

# Function to fetch articles using Alpha Vantage
# Function to fetch articles using Alpha Vantage
ALPHA_VANTAGE_API_KEY = "8USSUHG9CIPYSADT"  # Replace with your Alpha Vantage API key

ALPHA_VANTAGE_API_KEY = "8USSUHG9CIPYSADT"  # Replace with your Alpha Vantage API key

# Function to fetch articles from Alpha Vantage
def fetch_articles_alpha_vantage(topic, days):
    """
    Fetch articles using Alpha Vantage API, filter by date, and fetch full text for each article.
    
    :param topic: The keyword or topic to search for (e.g., "Bitcoin", "Tesla").
    :param days: Number of previous days to filter the news.
    :return: A list of articles with metadata and full text.
    """
    # Define the API endpoint and parameters
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "keywords": topic,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "feed" in data:
            # Convert the response to a pandas DataFrame
            news_df = pd.DataFrame(data["feed"])
            news_df = news_df.rename(columns={"time_published": "date", "url": "link", "title": "text"})
            news_df = news_df[["date", "link", "text"]]
            news_df["date"] = pd.to_datetime(news_df["date"], format="%Y%m%dT%H%M%S")
            
            # Filter rows by the specified number of previous days
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_df = news_df[news_df["date"] >= cutoff_date]
            
            # Fetch full text for each article
            articles = []
            for _, row in filtered_df.iterrows():
                full_text = fetch_article_text(row['link'])
                articles.append({
                    'date': row['date'].isoformat(),
                    'link': row['link'],
                    'text': full_text or row['text'],  # Fallback to the title if full text isn't available
                    'source': 'Alpha Vantage'
                })
            return articles
        else:
            print("No news data found for this topic.")
            return []
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

# Function to fetch the full text of an article from its URL
def fetch_article_text(url):
    """
    Fetch the full text of an article from its URL.
    
    :param url: The URL of the article.
    :return: The full text of the article or None if not accessible.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            full_text = ' '.join([para.get_text() for para in paragraphs if para.get_text()])
            return full_text.strip()
        else:
            print(f"Failed to fetch article content from {url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching article content from {url}: {e}")
        return None


# Function to fetch the full text of an article from its URL


# Unified function to fetch articles from multiple sources
def scrape_articles(topic, days):
    """
    Fetch articles from multiple sources, including News API and Alpha Vantage.
    
    :param topic: The keyword or topic to search for.
    :param days: Number of previous days to filter.
    :return: A combined list of articles from all sources.
    """
    news_api_articles = fetch_articles_news_api(topic, days)
    alpha_vantage_articles = fetch_articles_alpha_vantage(topic, days)

    # Add source name to each article
    for article in news_api_articles:
        article['source'] = 'News API'

    for article in alpha_vantage_articles:
        article['source'] = 'Alpha Vantage'

    return news_api_articles + alpha_vantage_articles
    