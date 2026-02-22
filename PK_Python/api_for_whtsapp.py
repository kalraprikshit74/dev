import requests

# Define the URL of the Flask REST API
url = "https://graph.facebook.com/v16.0/{phone_number_id}/messages"


# Define the data to send in the POST request
data = {
    "num1": 4,  # Replace with the first number
    "num2": 5   # Replace with the second number
}

# Make a POST request to the API
try:
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        print(f"Multiplication Result: {result['result']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Failed to connect to the API: {e}")
