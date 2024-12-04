import requests

from config.config import *

class SeptaAPIClient:
    """
    A client to interact with SEPTA's Next to Arrive API using query parameters.
    """

    BASE_URL = "https://www3.septa.org/api/NextToArrive/index.php"

    def __init__(self):
        pass

    def get_next_arrivals(self, depart_station, arrive_station, num_results=5):
        """
        Retrieves the next arrivals from the origin station to the destination station.

        Parameters:
            origin_station (str): The name of the origin station.
            destination_station (str): The name of the destination station.
            num_results (int): The number of results to retrieve (default is 5).

        Returns:
            list: A list of dictionaries containing arrival information.

        Raises:
            requests.HTTPError: An error occurred accessing the SEPTA API.
            ValueError: If the API returns an error message.
        """
        # Prepare query parameters
        params = {
            'req1': depart_station,
            'req2': arrive_station,
            'req3': num_results
        }

        try:
            # Make the GET request to the SEPTA API
            response = requests.get(self.BASE_URL, params=params, headers={'accept': 'application/json'})
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the JSON response
            data = response.json()

            # Check if the API returned an error
            if isinstance(data, dict) and 'error' in data:
                raise ValueError(f"SEPTA API Error: {data['error']}")

            return data

        except requests.exceptions.HTTPError as http_err:
            print(f"> ERROR: HTTP error occurred: {http_err}")  # Handle HTTP errors
            raise
        except Exception as err:
            print(f"> ERROR: An error occurred: {err}")  # Handle other exceptions
            raise