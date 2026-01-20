"""
Part 4: Robust Error Handling
=============================
Difficulty: Intermediate+

Learn:
- Try/except blocks for API requests
- Handling network errors
- Timeout handling
- Response validation
"""

import time
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from requests.exceptions import (
    ConnectionError,
    Timeout,
    HTTPError,
    RequestException
)
def safe_api_request(url, timeout=5, retries=3):
    """Make an API request with retry logic and logging."""

    logging.info(f"Request started: {url}")

    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Attempt {attempt} for {url}")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            logging.info(
                f"Request successful ({response.status_code}) for {url}"
            )
            return {"success": True, "data": response.json()}

        except (ConnectionError, Timeout) as e:
            logging.warning(
                f"Attempt {attempt} failed due to network issue: {e}"
            )
            if attempt == retries:
                logging.error(
                    f"Request failed after {retries} attempts: {url}"
                )
                return {
                    "success": False,
                    "error": f"Failed after {retries} attempts"
                }
            time.sleep(2)

        except HTTPError as e:
            status = e.response.status_code
            logging.error(f"HTTP error {status} for {url}")
            return {
                "success": False,
                "error": f"HTTP Error: {status}"
            }

        except RequestException as e:
            logging.error(f"Request exception for {url}: {e}")
            return {
                "success": False,
                "error": f"Request failed: {e}"
            }


def demo_error_handling():
    print("=== Error Handling Demo ===\n")

    tests = [
        ("Valid URL", "https://jsonplaceholder.typicode.com/posts/1"),
        ("Non-existent Resource (404)", "https://jsonplaceholder.typicode.com/posts/99999"),
        ("Invalid Domain", "https://this-domain-does-not-exist-12345.com/api"),
        ("Timeout Simulation", "https://httpstat.us/200?sleep=5000")
    ]

    for desc, url in tests:
        print(f"\n--- Test: {desc} ---")
        timeout = 1 if "Timeout" in desc else 5
        result = safe_api_request(url, timeout=timeout)
        if result["success"]:
            print(f"Success! Data preview: {str(result['data'])[:60]}...")
        else:
            print(f"Failed: {result['error']}")

def validate_crypto_response(data):
    """Check if crypto response contains required fields."""
    try:
        if "quotes" not in data or "USD" not in data["quotes"]:
            return False, "Missing quotes/USD data"
        usd = data["quotes"]["USD"]
        for field in ["price", "percent_change_24h"]:
            if field not in usd:
                return False, f"Missing field '{field}' in USD data"
        return True, None
    except TypeError:
        return False, "Invalid response format"


def fetch_crypto_safely():
    """Fetch crypto data with full error handling."""
    print("\n=== Safe Crypto Price Checker ===\n")

    coin = input("Enter coin (btc-bitcoin, eth-ethereum): ").strip().lower()

    if not coin:
        print("Error: Please enter a coin name.")
        return

    url = f"https://api.coinpaprika.com/v1/tickers/{coin}"
    result = safe_api_request(url)

    if not result["success"]:
        print(f"\nError: {result['error']}")
        print("Tip: Try 'btc-bitcoin' or 'eth-ethereum'")
        return

    data = result["data"]

    # ✅ VALIDATION STEP
    is_valid, error = validate_crypto_response(data)
    if not is_valid:
        print(f"\nInvalid crypto data: {error}")
        return

    # ✅ SAFE ACCESS
    usd = data["quotes"]["USD"]

    print(f"\n{data['name']} ({data['symbol']})")
    print(f"Price: ${usd['price']:,.2f}")
    print(f"24h Change: {usd['percent_change_24h']:+.2f}%")


def validate_json_response():
    """Demonstrate JSON validation."""
    print("\n=== JSON Validation Demo ===\n")

    url = "https://jsonplaceholder.typicode.com/users/1"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        required_fields = ["name", "email", "phone"]
        missing = [f for f in required_fields if f not in data]

        if missing:
            print(f"Warning: Missing fields: {missing}")
        else:
            print("All required fields present!")
            print(f"Name: {data['name']}")
            print(f"Email: {data['email']}")
            print(f"Phone: {data['phone']}")

    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not valid JSON")

    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all demos."""
    demo_error_handling()
    print("\n" + "=" * 40 + "\n")
    validate_json_response()
    print("\n" + "=" * 40 + "\n")
    fetch_crypto_safely()


if __name__ == "__main__":
    main()



# --- EXERCISES ---
#
# Exercise 1: Add retry logic - if request fails, try again up to 3 times
#             Hint: Use a for loop and time.sleep() between retries
#
# Exercise 2: Create a function that validates crypto response
#             Check that 'quotes' and 'USD' keys exist before accessing
#
# Exercise 3: Add logging to track all API requests
#             import logging
#             logging.basicConfig(level=logging.INFO)
