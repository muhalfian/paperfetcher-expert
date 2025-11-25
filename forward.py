from paperfetcher import snowballsearch
from scholar import metadata
import pandas as pd

# Path file Excel (ubah sesuai nama file Anda)
file_path = "articles.xlsx"

# Membaca sheet "Primary"
df = pd.read_excel(file_path, sheet_name="Primary")

# Pastikan kolom DOI dan ID ada
required_columns = ["ID", "DOI"]
if all(col in df.columns for col in required_columns):
    df_subset = df[["ID", "DOI"]].dropna(subset=["DOI"])  # buang baris yang DOI-nya kosong
else:
    missing = [col for col in required_columns if col not in df.columns]
    raise ValueError(f"Kolom berikut tidak ditemukan di sheet: {missing}")

# Contoh looping
articles = []
for index, row in df_subset.iterrows():
    paper_id = row["ID"]
    doi = row["DOI"]

    forward = snowballsearch.COCIForwardCitationSearch([row["DOI"]])
    forward()
    forward_count = len(forward)
    forward_doi = list(forward.result_dois)
    print(row["ID"], forward_doi)

    forward_meta = metadata(forward_doi, paper_id)
    articles.extend(forward_meta)

df = pd.DataFrame(articles)
df.to_excel("forward_articles.xlsx")