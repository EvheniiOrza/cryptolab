import requests
from requests.auth import HTTPBasicAuth

class NetworkHelper:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url
        self.auth = (username, password) if username and password else None

    def get_list(self):
        try:
            response = requests.get(f"{self.base_url}/clients", auth=self.auth)
            response.raise_for_status()

            # Check if response is JSON
            if response.headers.get("Content-Type") == "application/json":
                return response.json()
            else:
                print("Response is not JSON format:", response.text)
                return []  # Return an empty list or handle accordingly

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        return []

    def get_item_by_id(self, item_id):
        try:
            response = requests.get(f"{self.base_url}/clients/{item_id}", auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except ValueError:
            print("Response is not in JSON format:", response.text)
        return {}

    def create_item(self, data):
        try:
            response = requests.post(f"{self.base_url}/clients/add/", json=data, auth=self.auth)
            response.raise_for_status()
            return response.json() if response.content else {"status": "No Content"}
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except ValueError:
            print("Response is not in JSON format:", response.text)
        return {}

    def update_item_by_id(self, item_id, data):
        try:
            response = requests.put(f"{self.base_url}/clients/{item_id}/edit/", json=data, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except ValueError:
            print("Response is not in JSON format:", response.text)
        return {}

    def delete_item_by_id(self, item_id):
        try:
            response = requests.delete(f"{self.base_url}/clients/{item_id}/delete/", auth=self.auth)
            response.raise_for_status()
            return response.json() if response.content else {"status": "No Content"}
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except ValueError:
            print("Response is not in JSON format:", response.text)
        return {}
