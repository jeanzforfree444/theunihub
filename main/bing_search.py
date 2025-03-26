import json
import requests


def read_bing_key():
    """
    Reads the Bing API key from a file.

    Attempts to open 'search.key' first, then '../search.key' if the first attempt fails.
    Raises an IOError if neither file can be opened, or a KeyError if the key is empty.

    Returns:
        str: The Bing API key.
    """

    bing_api_key = None

    try:

        with open('search.key', 'r') as f:

            bing_api_key = f.readline().strip()

    except:

        try:

            with open('../search.key', 'r') as f:

                bing_api_key = f.readline().strip()

        except:

            raise IOError('search.key file not found')
    
    if not bing_api_key:

        raise KeyError('Bing key not found')
    
    return bing_api_key

def run_query(search_terms):
    """
    Runs a search query using Bing's Web Search API.

    Args:
        search_terms (str): The search query terms.

    Returns:
        list: A list of dictionaries, each containing 'title', 'link', and 'summary' of a search result.
    """

    bing_key = read_bing_key()

    # Define the Bing search API endpoint
    search_url = 'https://api.bing.microsoft.com/v7.0/search'

    headers = {'Ocp-Apim-Subscription-Key': bing_key}

    params = {'q': search_terms, 'textDecorations': True, 'textFormat': 'HTML'}

    # Make the GET request to the Bing API
    response = requests.get(search_url, headers=headers, params=params)

    response.raise_for_status() # Raise an error for any unsuccessful HTTP response

    # Parse the JSON response into a Python dictionary
    search_results = response.json()

    results = []

    if 'webPages' in search_results:

        # Loop through each search result provided by Bing
        for result in search_results['webPages']['value']:

            # Append a formatted dictionary of the result to the list
            results.append({
                'title': result['name'],
                'link': result['url'],
                'summary': result['snippet']
            })
    
    return results

def main():
    """
    Main function that prompts the user for search terms,
    runs the query using Bing's API, and prints the results.
    """

    search_terms = str(input("Please enter search terms: "))

    results = run_query(search_terms)

    print(json.dumps(results, indent=2))

# This condition ensures that main() is only executed when this script is run directly,
# and not when it is imported as a module in another script
if __name__ == '__main__':

    main()