import requests
import pandas as pd
import time
from tqdm import tqdm

# ===== Optional: Insert your API key if available (recommended for higher rate limits) =====
API_KEY = "Kad2qRSoqh7Z8qbrGe4GV4bTUy7V9Bs85mjdYHmJ"  # leave empty ("") if not using API key

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/"
# Fields to be retrieved from Semantic Scholar API
FIELDS = "title,authors,abstract,year,referenceCount,citationCount,venue,fieldsOfStudy,url"

# ===== Headers: automatically include API key if provided =====
headers = {"x-api-key": API_KEY} if API_KEY else {}


def safe_join(value):
    """
    Safely join list elements into a comma-separated string.
    - If the list contains dictionaries with 'name' keys (e.g., authors), extract the names.
    - If the list contains normal elements, convert them to string and join.
    - If input is None or not a list, return an empty string to avoid errors.
    """
    if isinstance(value, list):
        # Handle list of dictionaries such as authors
        if all(isinstance(v, dict) and "name" in v for v in value):
            return ", ".join(v["name"] for v in value)
        return ", ".join(str(v) for v in value)
    return ""  # Return empty string for unsupported types


def metadata(dois, id):
    """
    Fetch article metadata from Semantic Scholar using a list of DOIs.
    
    Parameters:
    - dois: list of DOIs to be queried
    - id: ID of the source paper (used for traceability in snowballing)
    
    Returns:
    - List of dictionaries containing metadata for each DOI
    """
    results = []
    
    # Iterate through each DOI with progress bar
    for doi in tqdm(dois, desc="Fetching metadata"):
        paper_id = f"DOI:{doi}"
        url = f"{BASE_URL}{paper_id}?fields={FIELDS}"
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            # Handle common HTTP response status codes
            if response.status_code == 404:
                print(f"⚠️ DOI not found: {doi}")
                results.append({"DOI": doi, "Title": "Not Found"})
                continue
            elif response.status_code == 429:
                print("⏳ Rate limit exceeded. Waiting for 5 seconds...")
                time.sleep(5)
                continue
            elif response.status_code != 200:
                print(f"⚠️ Error {response.status_code} for DOI {doi}")
                results.append({"DOI": doi, "Title": "Error"})
                continue

            # Extract author names using safe_join()
            authors = safe_join(data.get("authors", []))

            # Append metadata to results list
            results.append({
                "DOI": doi,
                "Title": data.get("title", ""),
                "Authors": authors,
                "Year": data.get("year", ""),
                "Venue": data.get("venue", ""),
                "Abstract": data.get("abstract", ""),
                "Citation Count": data.get("citationCount", ""),
                "Reference Count": data.get("referenceCount", ""),
                "Fields of Study": safe_join(data.get("fieldsOfStudy", [])),
                "source paper ID": id,   # Trace source paper for snowball mapping
                "URL": data.get("url", "")
            })

            # Sleep to avoid hitting rate limits
            time.sleep(2)

        except Exception as e:
            # Handle unexpected exceptions (e.g., connection failure)
            print(f"❌ Error while processing DOI {doi}: {e}")
            time.sleep(2)  # Short delay before continuing
    
    return results
