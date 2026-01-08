"""Weather information feature."""

import logging
import requests
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class WeatherService:
    """Get weather information."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize weather service.
        
        Args:
            api_key: OpenWeatherMap API key (optional, can use wttr.in without)
        """
        self.api_key = api_key
        self.use_wttr = not api_key  # Use wttr.in if no API key
        
    def get_weather(self, location: str = "auto") -> Dict[str, str]:
        """Get current weather.
        
        Args:
            location: City name or "auto" for automatic detection
            
        Returns:
            Weather information dictionary
        """
        if self.use_wttr:
            return self._get_weather_wttr(location)
        else:
            return self._get_weather_openweather(location)
    
    def _get_weather_wttr(self, location: str) -> Dict[str, str]:
        """Get weather from wttr.in (no API key needed)."""
        try:
            # Use wttr.in with format parameter
            if location == "auto":
                url = "https://wttr.in/?format=j1"
            else:
                url = f"https://wttr.in/{location}?format=j1"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return {'error': 'Failed to get weather'}
            
            data = response.json()
            current = data['current_condition'][0]
            
            return {
                'temperature': f"{current['temp_C']}°C",
                'condition': current['weatherDesc'][0]['value'],
                'feels_like': f"{current['FeelsLikeC']}°C",
                'humidity': f"{current['humidity']}%",
                'location': data['nearest_area'][0]['areaName'][0]['value']
            }
            
        except Exception as e:
            logger.error(f"Weather error: {e}")
            return {'error': str(e)}
    
    def _get_weather_openweather(self, location: str) -> Dict[str, str]:
        """Get weather from OpenWeatherMap."""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                return {'error': 'Failed to get weather'}
            
            data = response.json()
            
            return {
                'temperature': f"{data['main']['temp']}°C",
                'condition': data['weather'][0]['description'],
                'feels_like': f"{data['main']['feels_like']}°C",
                'humidity': f"{data['main']['humidity']}%",
                'location': data['name']
            }
            
        except Exception as e:
            logger.error(f"Weather error: {e}")
            return {'error': str(e)}
    
    def get_weather_summary(self, location: str = "auto") -> str:
        """Get weather as a readable summary.
        
        Args:
            location: City name or "auto"
            
        Returns:
            Weather summary text
        """
        weather = self.get_weather(location)
        
        if 'error' in weather:
            return f"I couldn't get the weather information: {weather['error']}"
        
        summary = f"The weather in {weather['location']} is {weather['condition']}. "
        summary += f"Temperature is {weather['temperature']}, feels like {weather['feels_like']}. "
        summary += f"Humidity is {weather['humidity']}."
        
        return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\nTesting weather service...")
    
    weather = WeatherService()
    
    print("\nAuto-location weather:")
    print(weather.get_weather_summary())
    
    print("\nTokyo weather:")
    print(weather.get_weather_summary("Tokyo"))
