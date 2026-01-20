"""
Part 1: Basic GET Request
=========================
Difficulty: Beginner

Learn: How to make a simple GET request and view the response.

We'll use JSONPlaceholder - a free fake API for testing.
"""

import requests


# ---------------------------------------------------
# Exercise 1: Fetch post number 5
# ---------------------------------------------------
print("Exercise 1: Fetch Post Number 5\n")

url_post_5 = "https://jsonplaceholder.typicode.com/posts/5"
response = requests.get(url_post_5)

print(f"URL: {url_post_5}")
print(f"Status Code: {response.status_code}")
print("Response:")
print(response.json())
print("\n" + "-" * 50 + "\n")


# ---------------------------------------------------
# Exercise 2: Fetch list of all users
# ---------------------------------------------------
print("Exercise 2: Fetch All Users\n")

url_users = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url_users)

print(f"URL: {url_users}")
print(f"Status Code: {response.status_code}")
print("Response:")
print(response.json())
print(f"\nTotal Users: {len(response.json())}")
print("\n" + "-" * 50 + "\n")


# ---------------------------------------------------
# Exercise 3: Fetch a post that does NOT exist
# ---------------------------------------------------
print("Exercise 3: Fetch Non-Existent Post (ID 999)\n")

url_invalid = "https://jsonplaceholder.typicode.com/posts/999"
response = requests.get(url_invalid)

print(f"URL: {url_invalid}")
print(f"Status Code: {response.status_code}")
print("Response:")
print(response.json())

if response.status_code == 404:
    print("\nPost not found (404 Error)")
# --- EXERCISES ---
# Try these on your own:
#
# Exercise 1: Change the URL to fetch post number 5
#             Hint: Change /posts/1 to /posts/5
#
# Exercise 2: Fetch a list of all users
#             URL: https://jsonplaceholder.typicode.com/users
#
# Exercise 3: What happens if you fetch a post that doesn't exist?
#             Try: https://jsonplaceholder.typicode.com/posts/999
