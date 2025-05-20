import requests

def get_weather(city):
    API_KEY = "5a1fab4a27d3c6d0397383f4c875a34a"  # Replace with your OpenWeatherMap API key
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"].capitalize()
        }
        
        return weather_info
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    city = input("Enter city name: ")
    weather = get_weather(city)
    if "error" in weather:
        print("Error fetching weather:", weather["error"])
    else:
        print(f"Weather in {weather['city']}: {weather['temperature']}°C, {weather['condition']}, Humidity: {weather['humidity']}%")
