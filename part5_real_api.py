"""
Part 5: Real-World APIs - Weather & Crypto Dashboard
====================================================
Difficulty: Advanced

Learn:
- Working with multiple real APIs
- Data formatting and presentation
- Building a simple CLI dashboard
- Using environment variables for API keys (optional)
"""
import json
import requests
from datetime import datetime

import os

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    print("Warning: OPENWEATHER_API_KEY not set! OpenWeatherMap requests may fail.")

# City coordinates (latitude, longitude)
CITIES = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "sydney": (-33.8688, 151.2093),
    "paris": (48.8566, 2.3522),
    "berlin": (52.5200, 13.4050),
    "dubai": (25.276987, 55.296249),
    "singapore": (1.3521, 103.8198),
    "toronto": (43.6532, -79.3832),
    "san francisco": (37.7749, -122.4194),
    "moscow": (55.7558, 37.6173),
    "beijing": (39.9042, 116.4074),
    "rio de janeiro": (-22.9068, -43.1729),
    "cape town": (-33.9249, 18.4241),
}

# Popular cryptocurrencies
CRYPTO_IDS = {
    "bitcoin": "btc-bitcoin",
    "ethereum": "eth-ethereum",
    "dogecoin": "doge-dogecoin",
    "cardano": "ada-cardano",
    "solana": "sol-solana",
    "ripple": "xrp-xrp",
}


def get_weather(city_name):
    """
    Fetch weather data using Open-Meteo API (FREE, no API key needed).
    """
    city_lower = city_name.lower().strip()

    if city_lower not in CITIES:
        print(f"\nCity '{city_name}' not found.")
        print(f"Available cities: {', '.join(CITIES.keys())}")
        return None

    lat, lon = CITIES[city_lower]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,relative_humidity_2m",
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None
def save_to_json(data, filename="results.json"):
    """
    Save any Python dictionary or list to a JSON file.
    
    data: dict or list
    filename: str, output file name
    """
    if not data:
        print("No data to save.")
        return

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nData successfully saved to '{filename}'")
    except Exception as e:
        print(f"Failed to save data: {e}")

def get_openweather(city_name):
    """
    Fetch weather data from OpenWeatherMap using API key.
    """
    city = city_name.strip()
    if not OPENWEATHER_API_KEY:
        print("No API key provided. Set OPENWEATHER_API_KEY environment variable.")
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Celsius
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching OpenWeatherMap data: {e}")
        return None
def display_weather(city_name):
    """Display formatted weather information."""
    data = get_weather(city_name)

    if not data:
        return

    current = data["current_weather"]

    print(f"\n{'=' * 40}")
    print(f"  Weather in {city_name.title()}")
    print(f"{'=' * 40}")
    print(f"  Temperature: {current['temperature']}°C")
    print(f"  Wind Speed: {current['windspeed']} km/h")
    print(f"  Wind Direction: {current['winddirection']}°")

    # Weather condition codes
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        95: "Thunderstorm",
    }

    code = current.get("weathercode", 0)
    condition = weather_codes.get(code, "Unknown")
    print(f"  Condition: {condition}")
    print(f"{'=' * 40}")

def display_openweather(city_name):
    """Display OpenWeatherMap weather information."""
    data = get_openweather(city_name)
    if not data:
        return

    main = data.get("main", {})
    wind = data.get("wind", {})
    weather_list = data.get("weather", [])
    condition = weather_list[0]["description"] if weather_list else "Unknown"

    print(f"\n{'='*40}")
    print(f"  OpenWeatherMap Weather in {city_name.title()}")
    print(f"{'='*40}")
    print(f"  Temperature: {main.get('temp', 'N/A')}°C")
    print(f"  Humidity: {main.get('humidity', 'N/A')}%")
    print(f"  Wind Speed: {wind.get('speed', 'N/A')} m/s")
    print(f"  Condition: {condition.title()}")
    print(f"{'='*40}")

def get_crypto_price(coin_name):
    """
    Fetch crypto data using CoinPaprika API (FREE, no API key needed).
    """
    coin_lower = coin_name.lower().strip()

    # Map common name to API ID
    coin_id = CRYPTO_IDS.get(coin_lower, coin_lower)

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching crypto data: {e}")
        return None
def compare_cryptos(coin_list):
    """
    Compare multiple cryptocurrencies and display their prices and 24h changes.
    
    coin_list: list of coin names or symbols (e.g., ['bitcoin', 'ethereum'])
    """
    print(f"\n{'='*55}")
    print("   Crypto Price Comparison")
    print(f"{'='*55}")
    print(f"{'Coin':<15}{'Price USD':>15}{'24h Change':>15}")
    print(f"{'-'*55}")

    for coin in coin_list:
        data = get_crypto_price(coin)  # reuse your existing function
        if data is None:
            print(f"{coin:<15}{'N/A':>15}{'N/A':>15}")
            continue

        try:
            usd = data["quotes"]["USD"]
            price = usd["price"]
            change_24h = usd["percent_change_24h"]
            print(f"{data['symbol']:<15}${price:>14,.2f}{change_24h:>14.2f}%")
        except KeyError:
            print(f"{coin:<15}{'Error':>15}{'Error':>15}")

    print(f"{'='*55}")


def display_crypto(coin_name):
    """Display formatted crypto information."""
    data = get_crypto_price(coin_name)

    if not data:
        print(f"\nCoin '{coin_name}' not found.")
        print(f"Available: {', '.join(CRYPTO_IDS.keys())}")
        return

    usd = data["quotes"]["USD"]

    print(f"\n{'=' * 40}")
    print(f"  {data['name']} ({data['symbol']})")
    print(f"{'=' * 40}")
    print(f"  Price: ${usd['price']:,.2f}")
    print(f"  Market Cap: ${usd['market_cap']:,.0f}")
    print(f"  24h Volume: ${usd['volume_24h']:,.0f}")
    print(f"  ")
    print(f"  1h Change:  {usd['percent_change_1h']:+.2f}%")
    print(f"  24h Change: {usd['percent_change_24h']:+.2f}%")
    print(f"  7d Change:  {usd['percent_change_7d']:+.2f}%")
    print(f"{'=' * 40}")


def get_top_cryptos(limit=5):
    """Fetch top cryptocurrencies by market cap."""
    url = "https://api.coinpaprika.com/v1/tickers"
    params = {"limit": limit}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def create_post():
    """
    Create a new post using JSONPlaceholder POST endpoint.
    """
    global last_post_data 
    print("\n=== Create a New Post ===")
    title = input("Enter post title: ").strip()
    body = input("Enter post body: ").strip()

    if not title or not body:
        print("Title and body cannot be empty.")
        return

    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {"title": title, "body": body}

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()
        last_post_data = data
        print("\nPost successfully created!")
        print(f"Post ID: {data.get('id')}")
        print(f"Title: {data.get('title')}")
        print(f"Body: {data.get('body')}")
    except requests.RequestException as e:
        print(f"Failed to create post: {e}")

def display_top_cryptos():
    """Display top 5 cryptocurrencies."""
    data = get_top_cryptos(5)

    if not data:
        return

    print(f"\n{'=' * 55}")
    print(f"  Top 5 Cryptocurrencies by Market Cap")
    print(f"{'=' * 55}")
    print(f"  {'Rank':<6}{'Name':<15}{'Price':<15}{'24h Change'}")
    print(f"  {'-' * 50}")

    for coin in data:
        usd = coin["quotes"]["USD"]
        change = usd["percent_change_24h"]
        change_str = f"{change:+.2f}%"

        print(f"  {coin['rank']:<6}{coin['name']:<15}${usd['price']:>12,.2f}  {change_str}")

    print(f"{'=' * 55}")


def dashboard():
    """Interactive dashboard combining weather and crypto."""
    print("\n" + "=" * 50)
    print("   Real-World API Dashboard")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("  1. Check Weather")
        print("  2. Check Crypto Price")
        print("  3. View Top 5 Cryptos")
        print("  4. Quick Dashboard (Delhi + Bitcoin)")
        print("  5. Compare Multiple Cryptos")
        print("  6. Create a New Post")
        print("  7. Save Results to JSON")
        print("  8. OpenWeatherMap Weather")
        print("  9. Exit")

        choice = input("\nSelect (1-9): ").strip()

        if choice == "1":
            print(f"\nAvailable: {', '.join(CITIES.keys())}")
            city = input("Enter city name: ")
            display_weather(city)

        elif choice == "2":
            print(f"\nAvailable: {', '.join(CRYPTO_IDS.keys())}")
            coin = input("Enter crypto name: ")
            display_crypto(coin)

        elif choice == "3":
            display_top_cryptos()

        elif choice == "4":
            display_weather("delhi")
            display_crypto("bitcoin")

        elif choice == "5":
            print(f"\nAvailable cryptos: {', '.join(CRYPTO_IDS.keys())}")
            coins_input = input("Enter coin names separated by commas: ")
            coins = [c.strip() for c in coins_input.split(",") if c.strip()]
            if coins:
                compare_cryptos(coins)
            else:
                print("No valid coins entered.")
        elif choice == "6":
            create_post()
        elif choice == "7":
            print("\nOptions to save data:")
            print("1. Crypto Data")
            print("2. Weather Data")
            print("3. Last POST Response")

            sub_choice = input("Select (1-3): ").strip()

            if sub_choice == "1":
                coin = input("Enter crypto name to save: ").strip()
                data = get_crypto_price(coin)
                save_to_json(data, f"{coin}_data.json")

            elif sub_choice == "2":
                city = input("Enter city name to save: ").strip()
                data = get_weather(city)
                save_to_json(data, f"{city}_weather.json")

            elif sub_choice == "3":
                # Make sure you store the last POST response in a variable
                if 'last_post_data' in globals():
                    save_to_json(last_post_data, "last_post.json")
                else:
                    print("No POST data available to save.")
            else:
                print("Invalid choice.")
        elif choice == "8":
            city = input("Enter city name: ").strip()
            display_openweather(city)
        elif choice == "9":
            print("\nGoodbye! Happy coding!")
            break
        

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    dashboard()


# --- CHALLENGE EXERCISES ---
#
# Exercise 1: Add more cities to the CITIES dictionary
#             Find coordinates at: https://www.latlong.net/
#
# Exercise 2: Create a function that compares prices of multiple cryptos
#             Display them in a formatted table
#
# Exercise 3: Add POST request example
#             Use: https://jsonplaceholder.typicode.com/posts
#             Send: requests.post(url, json={"title": "My Post", "body": "Content"})
#
# Exercise 4: Save results to a JSON file
#             import json
#             with open("results.json", "w") as f:
#                 json.dump(data, f, indent=2)
#
# Exercise 5: Add API key support for OpenWeatherMap
#             Sign up at: https://openweathermap.org/api
#             Use environment variables:
#             import os
#             api_key = os.environ.get("OPENWEATHER_API_KEY")
