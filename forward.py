from paperfetcher import snowballsearch
from scholar import metadata
import pandas as pd

# Path to the Excel file (adjust according to your filename)
file_path = "data/articles.xlsx"

# Read data from the "Primary" sheet
df = pd.read_excel(file_path, sheet_name="Primary")

# Ensure that the required columns "ID" and "DOI" exist in the DataFrame
required_columns = ["ID", "DOI"]
if all(col in df.columns for col in required_columns):
    # Select only the ID and DOI columns, and drop rows with missing DOI values
    df_subset = df[["ID", "DOI"]].dropna(subset=["DOI"])
else:
    # Raise an error if any required columns are missing
    missing = [col for col in required_columns if col not in df.columns]
    raise ValueError(f"The following columns are missing from the sheet: {missing}")

# Initialize a list to store extracted article metadata
articles = []

# Iterate through each row containing paper ID and DOI
for index, row in df_subset.iterrows():
    paper_id = row["ID"]
    doi = row["DOI"]

    # Initialize COCI Forward Citation Search to retrieve all papers citing the current DOI
    forward = snowballsearch.COCIForwardCitationSearch([doi])
    
    # Execute the forward snowballing search
    forward()
    
    # Get number of forward citations
    forward_count = len(forward)
    
    # Extract DOIs of the citing papers
    forward_doi = list(forward.result_dois)
    
    # Display current ID and the list of citing DOIs (for tracking progress)
    print(paper_id, forward_doi)

    # Fetch metadata for all forward DOIs, linking them to the original paper ID
    forward_meta = metadata(forward_doi, paper_id)
    
    # Add the metadata results to the articles list
    articles.extend(forward_meta)

# Convert the collected metadata into a DataFrame
df = pd.DataFrame(articles)

# Save results to an Excel file
df.to_excel("data/forward_articles.xlsx", index=False)
