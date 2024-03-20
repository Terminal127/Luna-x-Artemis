import json
import pprint

from googleapiclient.discovery import build


def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    developer_key = ""

    # Get user input for the search query
    search_query = input("Enter your search query: ")

    service = build("customsearch", "v1", developerKey=developer_key)

    try:
        # Execute the custom search API request with user input
        res = (
            service.cse()
            .list(
                q=search_query,
                cx="017576662512468239146:omuauf_lfve",
            )
            .execute()
        )

        # Save the response to a text file
        filename = f"{search_query}_search_response.txt"
        with open(filename, "w") as file:
            # Beautify the JSON response
            json.dump(res, file, indent=2)

        print(f"Response saved to {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
