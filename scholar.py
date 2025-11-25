import requests
import pandas as pd
import time
from tqdm import tqdm

# ====== OPSIONAL: Masukkan API KEY jika ada ======
API_KEY = "Kad2qRSoqh7Z8qbrGe4GV4bTUy7V9Bs85mjdYHmJ"  # kosongkan jika tidak ingin pakai API key

# ====== Daftar DOI ======
dois = [
    "10.1145/3366423.3380283",
    "10.18653/v1/P19-1015",
    "10.1109/5.771073"
]

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/"
FIELDS = "title,authors,abstract,year,referenceCount,citationCount,venue,fieldsOfStudy,url"



# ====== Headers: otomatis pakai API key jika diisi ======
headers = {"x-api-key": API_KEY} if API_KEY else {}

# Fungsi aman untuk join list (menghindari error jika bukan iterable)
def safe_join(value):
    if isinstance(value, list):
        # Jika list of dict (contoh authors), ambil "name"
        if all(isinstance(v, dict) and "name" in v for v in value):
            return ", ".join(v["name"] for v in value)
        return ", ".join(str(v) for v in value)
    return ""  # jika None atau bukan list, kembalikan string kosong

def metadata(dois, id):
    results = []
    for doi in tqdm(dois, desc="Fetching metadata"):
        paper_id = f"DOI:{doi}"
        url = f"{BASE_URL}{paper_id}?fields={FIELDS}"
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            # Penanganan error umum
            if response.status_code == 404:
                print(f"⚠️ DOI tidak ditemukan: {doi}")
                results.append({"DOI": doi, "Title": "Not Found"})
                continue
            elif response.status_code == 429:
                print("⏳ Rate limit exceeded. Tunggu 5 detik...")
                time.sleep(5)
                continue
            elif response.status_code != 200:
                print(f"⚠️ Error {response.status_code} untuk DOI {doi}")
                results.append({"DOI": doi, "Title": "Error"})
                continue

            # Ambil authors (nama saja, atau tambah affiliation jika tersedia)
            authors = safe_join(data.get("authors", []))

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
                "source paper ID": id,
                "URL": data.get("url", "")
            })
            time.sleep(2)  # untuk menghindari blok rate limit

        except Exception as e:
            print(f"❌ Error pada DOI {doi}: {e}")
            time.sleep(2)  # untuk menghindari blok rate limit
    return results