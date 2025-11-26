import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# === 1. Research Topic Definition ===
# This description acts as a semantic reference to compare article relevance.
topic_description = """
Ambiguity in POS (part-of-speech) Tagging for Morphologically Rich Languages.
Focus on syntactic ambiguity, morphological ambiguity, tagging errors,
and challenges in rich morphology languages.
"""

# Input and output file paths
input = "data/backward_articles.xlsx"
output = "data/backward_screening.xlsx"

# === Keyword categories for lexical matching ===
# These keywords represent core aspects of the research topic.
keyword_1 = ["POS tagging", "part-of-speech", "parts-of-speech", "part of speech"]
keyword_2 = ["ambiguity", "ambiguous", "tagging errors", "syntactic ambiguity", "morphological ambiguity"]
keyword_3 = ["morphology", "morphologically rich language", "MRL", "morphological"]

# === 2. Load semantic model and dataset ===
# SentenceTransformer is used to generate semantic embeddings for similarity comparison.
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load the list of articles (must contain Title and Abstract columns)
df = pd.read_excel(input)

# Prepare new columns to store evaluation results
df["SimilarityScore"] = 0.0

# === 3. Relevance Processing for Each Article ===
# Encode the topic description into a vector as the semantic reference prototype
topic_vec = model.encode([topic_description])

for idx, row in df.iterrows():
    # Combine Title and Abstract into a single text block for analysis
    text = f"{row['Title']} {row['Abstract']}"
    
    # Generate semantic vector for the article text
    text_vec = model.encode([text])

    # Calculate semantic similarity using cosine similarity
    similarity = cosine_similarity(topic_vec, text_vec)[0][0]
    
    # Count keyword occurrences (lexical matching) across keyword groups
    keyword_hit_1 = sum(text.lower().count(kw.lower()) for kw in keyword_1)
    keyword_hit_2 = sum(text.lower().count(kw.lower()) for kw in keyword_2)
    keyword_hit_3 = sum(text.lower().count(kw.lower()) for kw in keyword_3)

    # Save computed values back to the DataFrame
    df.at[idx, "SimilarityScore"] = round(similarity, 3)
    df.at[idx, "pos_tagging"] = keyword_hit_1
    df.at[idx, "ambiguity"] = keyword_hit_2
    df.at[idx, "MRL"] = keyword_hit_3

# === 4. Save results into a new Excel file ===
df.to_excel(output, index=False)
