from http.client import responses

import requests
import json
import re
import time

def replace_placeholders(data, env):
    """
    Replaces placeholders in the data with values from the environment.

    :param data: The JSON data (dict) containing placeholders.
    :param env: A dictionary of environment variables.
    :return: The JSON data with placeholders replaced.
    """
    # Convert to string for replacement
    data_str = json.dumps(data)

    # Replace placeholders with environment variables
    for key, value in env.items():
        placeholder = f"{{{{{key}}}}}"  # e.g., "{{host}}"
        data_str = data_str.replace(placeholder, value)

    # Convert back to dict
    return json.loads(data_str)

def call_api(json_file=None):
    try:
        # Read JSON payload from file if provided
        payload = None
        if json_file:
            with open(json_file, 'r') as file:
                payload = json.load(file)
        print(payload)
        env = payload.get("environment", {})

        responses = []
        # Parse the list of API requests
        requests_list = payload.get("requests", [])
        for request in requests_list:
            request = replace_placeholders(request, env)
            url = request.get("url")
            method = request.get("method", "GET").upper()
            body = request.get("body", {})
            headers = request.get("headers", {})
            # Perform the API call
            print(f"Calling {method} {url} with body: {body}")
            start_time = time.time()
            if method == "POST":
                response = requests.post(url, json=body, headers=headers)
            elif method == "GET":
                response = requests.get(url, params=body,headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, params=body,headers=headers)
            elif method == "PUT":
                response = requests.put(url, params=body,headers=headers)
            elif method == "PATCH":
                response = requests.patch(url, params=body,headers=headers)
            else:
                response = {"error": f"Unsupported HTTP method: {method}"}
            end_time = time.time()
            time_taken = end_time - start_time
            print( f"time_taken {time_taken:.2f} seconds")
            if isinstance(response, dict):  # Handle unsupported method
                responses.append(response)
            else:
                try:
                    responses.append({"response": response.text})
                except json.JSONDecodeError:
                    responses.append({"error": "Failed to parse response", "status_code": response.status_code})

    except Exception as e:
        return {"error": str(e)}

    return responses

# Example Usage
if __name__ == "__main__":
    try:
        response = call_api(json_file="input.json")
        print("API Response:")
        print(json.dumps(response, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")
