import pandas as pd
# from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# === 1. Definisi Topik Penelitian ===
topic_description = """
Ambiguity in POS Tagging for Morphologically Rich Languages.
Focus on syntactic ambiguity, morphological ambiguity, tagging errors,
and challenges in rich morphology languages (Arabic, Turkish, Finnish, etc).
"""

# Kata kunci penting
keywords = [
    "POS tagging", "part-of-speech", "part of speech", "ambiguity", "ambiguous", "morphology", 
    "morphologically rich language", "MRL", "morphological", "tagging errors", 
    "syntactic ambiguity", "morphological ambiguity", "ambiguity"
]

# === 2. Load model dan data ===
# model = SentenceTransformer("all-MiniLM-L6-v2")

# Contoh DataFrame: ID, Title, Abstract
df = pd.read_excel("forward_articles.xlsx")  # ganti dengan file Anda

# Buat kolom hasil
# df["SimilarityScore"] = 0.0
df["KeywordScore"] = 0
df["Relevant"] = ""

# === 3. Processing ===
# topic_vec = model.encode([topic_description])

for idx, row in df.iterrows():
    text = f"{row['Title']} {row['Abstract']}"
#     text_vec = model.encode([text])

#     # Similarity berbasis semantic meaning
#     similarity = cosine_similarity(topic_vec, text_vec)[0][0]
    
    # Keyword-based score
    keyword_hits = sum(text.lower().count(kw.lower()) for kw in keywords)
    
    # Tentukan relevansi berdasarkan threshold
    # is_relevant = (similarity > 0.55) and (keyword_hits >= 2)
    is_relevant = (keyword_hits >= 2)

#     # Simpan ke df
#     df.at[idx, "SimilarityScore"] = round(similarity, 3)
    df.at[idx, "KeywordScore"] = keyword_hits
    df.at[idx, "Relevant"] = "YES" if is_relevant else "NO"

# === 4. Simpan hasil ===
df.to_excel("forward_screening.xlsx", index=False)
