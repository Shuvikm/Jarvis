"""Web search functionality for J.A.R.V.I.S."""

import logging
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WebSearch:
    """Web search capability."""
    
    def __init__(self):
        """Initialize web search."""
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Search the web for a query.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results
        """
        try:
            # Use DuckDuckGo HTML (no API key needed)
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Search failed: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.find_all('div', class_='result')[:num_results]:
                try:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem:
                        results.append({
                            'title': title_elem.get_text(strip=True),
                            'url': title_elem.get('href', ''),
                            'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                        })
                except:
                    continue
            
            logger.info(f"Found {len(results)} results for: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def get_summary(self, query: str) -> str:
        """Get a summary of search results.
        
        Args:
            query: Search query
            
        Returns:
            Summary text
        """
        results = self.search(query, num_results=3)
        
        if not results:
            return f"I couldn't find any results for '{query}'."
        
        summary = f"I found {len(results)} results for '{query}':\n\n"
        
        for i, result in enumerate(results, 1):
            summary += f"{i}. {result['title']}\n"
            if result['snippet']:
                summary += f"   {result['snippet'][:100]}...\n"
        
        return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\nTesting web search...")
    
    search = WebSearch()
    results = search.search("Bleach anime Aizen")
    
    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   {result['url']}")
        if result['snippet']:
            print(f"   {result['snippet'][:100]}...")
