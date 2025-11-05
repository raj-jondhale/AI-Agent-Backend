"""
External API Tools for the AI Agent
Provides integrations for Weather, Wikipedia, and News APIs
"""

import requests
import wikipediaapi
import logging
from typing import Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherTool:
    """Tool for fetching weather information from OpenWeatherMap API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city: str) -> Optional[Dict]:
        """
        Fetch current weather for a given city
        
        Args:
            city: Name of the city
            
        Returns:
            Dictionary with weather information or None if failed
        """
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"  # Use Celsius
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            
            logger.info(f"Successfully fetched weather for {city}")
            return weather_info
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing weather data: {str(e)}")
            return None


class WikipediaTool:
    """Tool for fetching information from Wikipedia"""
    
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            user_agent='AI-Agent/1.0 (Educational Project)',
            language='en'
        )
    
    def search(self, query: str) -> Optional[Dict]:
        """
        Search Wikipedia for information
        
        Args:
            query: Search query
            
        Returns:
            Dictionary with page title and summary or None if not found
        """
        try:
            page = self.wiki.page(query)
            
            if not page.exists():
                # Try alternative approach using requests
                return self._fallback_search(query)
            
            # Get first 3 sentences of the summary
            summary = page.summary.split('. ')[:3]
            summary_text = '. '.join(summary) + '.'
            
            result = {
                "title": page.title,
                "summary": summary_text,
                "url": page.fullurl
            }
            
            logger.info(f"Successfully fetched Wikipedia info for: {query}")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching Wikipedia data: {str(e)}")
            return self._fallback_search(query)
    
    def _fallback_search(self, query: str) -> Optional[Dict]:
        """Fallback method using Wikipedia API directly"""
        try:
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            result = {
                "title": data.get("title", query),
                "summary": data.get("extract", "No information found."),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
            }
            
            return result
        except Exception as e:
            logger.error(f"Fallback Wikipedia search failed: {str(e)}")
            return None


class NewsTool:
    """Tool for fetching news articles from News API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
    
    def get_news(self, topic: str, max_results: int = 3) -> Optional[Dict]:
        """
        Fetch recent news articles about a topic
        
        Args:
            topic: News topic to search for
            max_results: Maximum number of articles to return
            
        Returns:
            Dictionary with news articles or None if failed
        """
        try:
            params = {
                "q": topic,
                "apiKey": self.api_key,
                "pageSize": max_results,
                "sortBy": "publishedAt",
                "language": "en"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data["status"] != "ok" or not data.get("articles"):
                return None
            
            articles = []
            for article in data["articles"][:max_results]:
                articles.append({
                    "title": article.get("title", "No title"),
                    "description": article.get("description", "No description"),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "published_at": article.get("publishedAt", "Unknown"),
                    "url": article.get("url", "")
                })
            
            result = {
                "topic": topic,
                "total_results": data["totalResults"],
                "articles": articles
            }
            
            logger.info(f"Successfully fetched news for: {topic}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching news data: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing news data: {str(e)}")
            return None
