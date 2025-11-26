# 📄 paperfetcher-expert

**Automated Snowballing & Screening Tool for Systematic Literature Review (SLR)**

paperfetcher-expert is a Python-based toolkit to **automate forward & backward snowballing, retrieve metadata**, and **screen academic papers** using both **semantic similarity (SentenceTransformer)** and **keyword matching**.
This tool is designed to support **Systematic Literature Review (SLR)** and **Mapping Studies**, especially in fields related to NLP, POS Tagging, and Morphologically Rich Languages (MRL).


## 🚀 Key Features


### 🔍 1. Snowballing Search (Forward & Backward)

- Uses **CrossRef COCI API** to fetch:

    - Backward references (papers cited by a target paper)

    - Forward citations (papers that cite a target paper)

- Supports batch processing from Excel (ID, DOI format)


### 📄 2. Metadata Extraction

- Fetches metadata using **Semantic Scholar API**, including:

    - Title

    - Authors

    - Abstract

    - Venue

    - Year

    - Citation count & Reference count

    - URL and Fields of Study


### 🎯 3. Smart Screening for SLR

- Computes **semantic similarity** between article content (Title + Abstract) and research topic description

- Detects **keyword frequency** across three levels:

    - POS Tagging terminology

    - Ambiguity concepts

    - Morphological Language indicators (MRL)

- Generates Excel sheet with **SimilarityScore + keyword hit counts**

## 📁 Repository Structure
```bash
paperfetcher-expert/
│
├── data/
│   ├── articles.xlsx           # Input: Primary studies with ID and DOI
│   ├── backward_articles.xlsx  # Output of backward snowballing results
│   ├── forward_articles.xlsx   # Output of forward snowballing results
│   ├── backward_screening.xlsx # Screening results (semantic + keyword-based)
│
├── snowball_backward.py        # Script for backward citation search
├── snowball_forward.py         # Script for forward citation search
├── metadata_extractor.py       # Fetch metadata via Semantic Scholar API
├── screening_semantic.py       # Semantic + keyword-based relevance screening
│
├── README.md                   # You are here
└── requirements.txt            # Dependencies list
```

## 🛠️ Installation
### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/paperfetcher-expert.git
cd paperfetcher-expert
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

## 📦 Dependencies

Minimal required libraries:
```bash
pandas
requests
openpyxl
tqdm
sentence-transformers
scikit-learn
torch
```

## ▶️ Usage Guide

### 🧭 Step 1: Prepare Input File

Ensure your `data/articles.xlsx` contains a sheet named `"Primary"` with columns:

| ID	| DOI                   |
|-------|-----------------------|
| P01	| 10.1109/5.771073      |
| P02	| 10.1145/338358.338367 |

### 🔄 Step 2: Run Snowballing

**Backward Citations**
```bash
python snowball_backward.py
```

**Forward Citations**
```bash
python snowball_forward.py
```

Outputs saved to `/data/backward_articles.xlsx` and `/data/forward_articles.xlsx`.


### 🧠 Step 3: Screen Articles (Semantic Similarity)
```bash
python screening_semantic.py
```

Output file:
```bash
➡️ data/backward_screening.xlsx
```

Includes columns:

| DOI	| Title	| SimilarityScore	| pos_tagging	| ambiguity	| MRL	| URL |
|---|---|---|---|---|---|---|


## ⭐ Scoring Interpretation
| Score Type	| Meaning |
|---------------|----------|
| SimilarityScore	| Semantic similarity to research topic (0–1) |
| pos_tagging	| Keyword frequency matching POS Tagging concepts |
| ambiguity	| Keyword hits related to syntactic/morphological ambiguity |
| MRL	| Keyword hits for Morphologically Rich Language |

You can apply thresholds such as:

- `SimilarityScore > 0.50`

- `pos_tagging ≥ 2`

- `ambiguity ≥ 1`


## 📌 Roadmap

- 🔜 Streamlit-based user interface

- 🔜 Export to RIS/BibTeX format

- 🔜 Automatic deduplication of DOIs

- 🔜 Integration with Zotero and Mendeley


## 🙌 Acknowledgments

- Semantic Scholar API

- Crossref COCI citation API

- SentenceTransformers

- Pandas, PyTorch, scikit-learn


## 📬 Contact & Contribution

Contributions are welcome!
If you want to collaborate, improve screening algorithms, or extend to full SLR automation, feel free to open an issue or pull request.