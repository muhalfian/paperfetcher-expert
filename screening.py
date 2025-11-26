import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# === 1. Definisi Topik Penelitian ===
topic_description = """
Ambiguity in POS (part-of-speech) Tagging for Morphologically Rich Languages.
Focus on syntactic ambiguity, morphological ambiguity, tagging errors,
and challenges in rich morphology languages.
"""

input = "backward_articles.xlsx"
output = "backward_screening.xlsx"

# Kata kunci penting
keyword_1 = ["POS tagging", "part-of-speech", "parts-of-speech", "part of speech"]

keyword_2 = ["ambiguity", "ambiguous", "tagging errors", "syntactic ambiguity", "morphological ambiguity"]

keyword_3 = ["morphology", "morphologically rich language", "MRL", "morphological"]

# === 2. Load model dan data ===
model = SentenceTransformer("all-MiniLM-L6-v2")

# Contoh DataFrame: ID, Title, Abstract
df = pd.read_excel(input)  # ganti dengan file Anda

# Buat kolom hasil
df["SimilarityScore"] = 0.0
# df["KeywordScore"] = 0
# df["Relevant"] = ""

# === 3. Processing ===
topic_vec = model.encode([topic_description])

for idx, row in df.iterrows():
    text = f"{row['Title']} {row['Abstract']}"
    text_vec = model.encode([text])

    # Similarity berbasis semantic meaning
    similarity = cosine_similarity(topic_vec, text_vec)[0][0]
    
    # Keyword-based score
    keyword_hit_1 = sum(text.lower().count(kw.lower()) for kw in keyword_1)
    keyword_hit_2 = sum(text.lower().count(kw.lower()) for kw in keyword_2)
    keyword_hit_3 = sum(text.lower().count(kw.lower()) for kw in keyword_3)
    
    # # Tentukan relevansi berdasarkan threshold
    # is_relevant = (similarity > 0.55) and (keyword_hits >= 1)
    # # is_relevant = (keyword_hits >= 2)

    # Simpan ke df
    df.at[idx, "SimilarityScore"] = round(similarity, 3)
    df.at[idx, "pos_tagging"] = keyword_hit_1
    df.at[idx, "ambiguity"] = keyword_hit_2
    df.at[idx, "MRL"] = keyword_hit_3
    # df.at[idx, "Relevant"] = "YES" if is_relevant else "NO"

# === 4. Simpan hasil ===
df.to_excel(output, index=False)
