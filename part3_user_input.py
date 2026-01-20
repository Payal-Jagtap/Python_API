"""
Part 3: Dynamic Queries with User Input
=======================================
Difficulty: Intermediate

Learn:
- Using input() to make dynamic API requests
- Building URLs with f-strings
- Query parameters in URLs
"""

import requests


def get_user_info():
    """Fetch user info based on user input."""
    print("=== User Information Lookup ===\n")

    #user_id = input("Enter user ID (1-10): ")
    user_id = input("Enter user ID (1-10): ")

    if not user_id.isdigit() or not (1<=int(user_id)<=10):
        print("User ID must be a number!")
        return


    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"\n--- User #{user_id} Info ---")
        print(f"Name: {data['name']}")
        print(f"Email: {data['email']}")
        print(f"Phone: {data['phone']}")
        print(f"Website: {data['website']}")
    except requests.RequestException:
        print(f"\nUser with ID {user_id} not found!")

def search_posts():
    """Search posts by user ID."""
    print("\n=== Post Search ===\n")

    #user_id = input("Enter user ID to see their posts (1-10): ")
    user_id = input("Enter user ID to see their posts (1-10): ").strip()

    if not user_id.isdigit() or not (1<=int(user_id) <=10):
        print("User ID must be numeric!")
        return

    # Using query parameters
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": user_id}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        posts = response.json()
        if posts:
            print(f"\n--- Posts by User #{user_id} ---")
            for i, post in enumerate(posts, 1):
                print(f"{i}. {post['title']}")
        else:
            print("No posts found for this user.")
    except requests.RequestException:
        print("Error fetching posts.")


def get_crypto_price():
    """Fetch cryptocurrency price based on user input."""
    print("\n=== Cryptocurrency Price Checker ===\n")

    print("Available coins: btc-bitcoin, eth-ethereum, doge-dogecoin")
    coin_id = input("Enter coin ID (e.g., btc-bitcoin): ").lower().strip()

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price_usd = data['quotes']['USD']['price']
        change_24h = data['quotes']['USD']['percent_change_24h']

        print(f"\n--- {data['name']} ({data['symbol']}) ---")
        print(f"Price: ${price_usd:,.2f}")
        print(f"24h Change: {change_24h:+.2f}%")
    except requests.RequestException:
        print(f"\nCoin '{coin_id}' not found! Try: btc-bitcoin, eth-ethereum, doge-dogecoin")

def get_weather():
    """Fetch current weather for a city."""
    print("\n=== Weather Checker ===\n")

    city_coords = {
        "delhi": (28.61, 77.23),
        "mumbai": (19.07, 72.87),
        "london": (51.50, -0.12),
        "new york": (40.71, -74.00)
    }

    city = input("Enter city name: ").lower().strip()

    if city not in city_coords:
        print("City not available!")
        return

    lat, lon = city_coords[city]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        weather = data["current_weather"]
        print(f"\nCity: {city.title()}")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Wind Speed: {weather['windspeed']} km/h")
    except requests.RequestException:
        print("Could not fetch weather data.")

def search_todos():
    """Search todos by completion status."""
    print("\n=== Todo Search ===\n")

    status = input("Enter status (true/false): ").lower().strip()

    if status not in ["true", "false"]:
        print("Invalid status!")
        return

    url = "https://jsonplaceholder.typicode.com/todos"
    params = {"completed": status}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        todos = response.json()
        print(f"\nTotal todos found: {len(todos)}")
        for todo in todos[:5]:
            print("-", todo["title"])
    except requests.RequestException:
        print("Could not fetch todos.")

def main():
    """Main menu for the program."""
    print("=" * 40)
    print("  Dynamic API Query Demo")
    print("=" * 40)

    while True:
        print("\nChoose an option:")
        print("1. Look up user info")
        print("2. Search posts by user")
        print("3. Check crypto price")
        print("4. Search todos")
        print("5. Check weather")
        print("6. Exit")


        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            get_user_info()
        elif choice == "2":
            search_posts()
        elif choice == "3":
            get_crypto_price()
        elif choice == "4":
            search_todos()
        elif choice == "5":
            get_weather()
        elif choice =="6":
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


# --- EXERCISES ---
#
# Exercise 1: Add a function to fetch weather for a city
#             Use Open-Meteo API (no key required):
#             https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.23&current_weather=true
#             Challenge: Let user input city name (you'll need to find lat/long)
#
# Exercise 2: Add a function to search todos by completion status
#             URL: https://jsonplaceholder.typicode.com/todos
#             Params: completed=true or completed=false
#
# Exercise 3: Add input validation (check if user_id is a number)
