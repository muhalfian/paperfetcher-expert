from paperfetcher import snowballsearch
from scholar import metadata
import pandas as pd

# Define the path to the Excel file (modify according to your file location or name)
file_path = "data/articles.xlsx"

# Read the "Primary" sheet from the Excel file
df = pd.read_excel(file_path, sheet_name="Primary")

# Ensure the sheet contains the required columns: "ID" and "DOI"
required_columns = ["ID", "DOI"]
if all(col in df.columns for col in required_columns):
    # Select only the columns needed and remove rows with missing DOI values
    df_subset = df[["ID", "DOI"]].dropna(subset=["DOI"])
else:
    # Raise an error if any required column is missing
    missing = [col for col in required_columns if col not in df.columns]
    raise ValueError(f"The following columns are missing from the sheet: {missing}")

# Initialize a list to collect metadata for all articles found
articles = []

# Loop through each row containing paper ID and DOI
for index, row in df_subset.iterrows():
    paper_id = row["ID"]     # Unique identifier from the Excel file
    doi = row["DOI"]         # DOI of the primary article

    # Perform backward snowballing using COCI API to get references cited by the article
    backward = snowballsearch.COCIBackwardReferenceSearch([doi])
    backward()  # Execute the search
    
    # Get the number of backward references and extract the list of DOIs
    backward_count = len(backward)
    backward_doi = list(backward.result_dois)

    # Display the article ID and retrieved referenced DOIs (for tracking/logging)
    print(paper_id, backward_doi)
    
    # Fetch metadata for the backward references using the paper ID as parent
    forward_meta = metadata(backward_doi, paper_id)

    # Add the retrieved metadata to the final articles list
    articles.extend(forward_meta)

# Convert collected article metadata into a DataFrame
df = pd.DataFrame(articles)

# Export the DataFrame to an Excel file
df.to_excel("data/backward_articles.xlsx", index=False)
