# 🎯 TalentRank AI

<p align="center">

### AI-Powered Candidate Ranking System using Semantic Search, Hybrid AI Scoring & Explainable AI

Automatically retrieve, rank, and explain the best candidates from a large talent database using modern NLP, vector search, and intelligent ranking techniques.

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge\&logo=python)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge\&logo=streamlit)
![Sentence Transformers](https://img.shields.io/badge/SentenceTransformers-Embeddings-green?style=for-the-badge)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Artifacts-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</p>

---

## 🌐 Live Hosting

**🔗 Streamlit Application:**

https://talent-rank-ai.streamlit.app/

---

# 🎥 Project Demo

Watch TalentRank AI in action.

▶️ **Demo Video**

https://youtu.be/WK2JSu0zjaA



## 📖 Project Overview

TalentRank AI is an intelligent AI-powered candidate ranking system that helps recruiters efficiently identify the most suitable candidates from a large talent database.

Traditional resume screening relies heavily on keyword matching, which often overlooks strong candidates with relevant experience expressed differently. TalentRank AI addresses this challenge by combining semantic understanding, vector similarity search, hybrid ranking algorithms, and explainable AI to deliver more accurate candidate recommendations.

The system retrieves candidates using dense vector embeddings, evaluates them using multiple ranking signals, and generates human-readable explanations describing why each candidate is recommended.

Designed with scalability in mind, TalentRank AI efficiently searches across **100,000 candidate profiles** while maintaining fast retrieval times using FAISS vector indexing.

---

# ✨ Key Features

### 🔍 Semantic Candidate Search

* Dense vector embeddings using **BAAI/bge-small-en-v1.5**
* Semantic similarity instead of simple keyword matching
* High-speed FAISS vector retrieval
* Top-1000 candidate retrieval from a 100K database

---

### 🧠 Hybrid AI Ranking

TalentRank AI combines multiple intelligent ranking signals:

* Semantic Similarity
* Technical Skill Matching
* Experience Evaluation
* Career Progression Analysis
* Behavioral Assessment
* Recruiter Intelligence
* Honeypot Candidate Detection

These signals are combined using a weighted hybrid scoring engine to produce the final ranking.

---

### 💡 Explainable AI

Unlike traditional ranking systems, TalentRank AI explains every recommendation.

For each ranked candidate, the system generates AI-powered reasoning describing:

* Skill alignment
* Experience relevance
* Semantic similarity
* Career fit
* Overall suitability

This improves transparency and recruiter trust.

---

### ⚡ High Performance

* Supports **100,000+ candidates**
* FAISS Approximate Nearest Neighbor Search
* Lightweight embedding model
* Fast ranking pipeline
* Optimized artifact loading from Hugging Face

---

### ☁️ Cloud Ready

The application is designed for cloud deployment.

Large artifacts such as:

* FAISS Index
* Candidate Lookup
* Skill Vocabulary
* Dataset Statistics

are automatically downloaded from Hugging Face during startup, keeping the GitHub repository lightweight and deployment-friendly.

---

# 🎯 Problem Statement

Recruiters often spend significant time manually reviewing resumes, while traditional Applicant Tracking Systems depend heavily on keyword matching.

This approach may:

* Miss highly qualified candidates
* Ignore semantic relevance
* Produce inaccurate rankings
* Lack transparency
* Scale poorly for large datasets

TalentRank AI solves these challenges by combining modern NLP techniques with hybrid AI ranking and explainable recommendations.

---

# 🚀 Core Capabilities

✅ Semantic Resume Search

✅ Hybrid AI Ranking

✅ Explainable Candidate Recommendations

✅ Recruiter Intelligence Scoring

✅ Behavioral Assessment

✅ Career Progression Evaluation

✅ FAISS Vector Search

✅ Streamlit Interactive Dashboard

✅ Automatic Artifact Management

✅ Cloud Deployment Ready

---
# 🏗️ System Architecture

```
                         Recruiter
                             │
                             ▼
                  Enter Job Description
                             │
                             ▼
                  JD Understanding Module
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
   Skill Extraction    Experience Parsing   Requirement Analysis
         │
         ▼
    Sentence Embedding
 (BAAI/bge-small-en-v1.5)
         │
         ▼
      FAISS Vector Search
         │
         ▼
 Retrieve Top 1000 Candidates
         │
         ▼
   Hybrid AI Ranking Engine
         │
 ┌───────┼────────┬─────────┬────────┬──────────┬──────────┐
 ▼       ▼        ▼         ▼        ▼          ▼
Semantic Skills Experience Career Behavior Recruiter Intelligence
         │
         ▼
  Honeypot Candidate Detection
         │
         ▼
      Final AI Ranking
         │
         ▼
 Explainable AI Reasoning
         │
         ▼
 Streamlit Recruiter Dashboard
```

---

# ⚙️ Technology Stack

| Category             | Technology                |
| -------------------- | ------------------------- |
| Programming Language | Python 3.11               |
| Frontend             | Streamlit                 |
| Vector Search        | FAISS                     |
| Embedding Model      | BAAI/bge-small-en-v1.5    |
| NLP                  | Sentence Transformers     |
| Machine Learning     | Scikit-learn              |
| Data Processing      | Pandas, NumPy             |
| Artifact Storage     | Hugging Face Datasets     |
| Version Control      | Git & GitHub              |
| Deployment           | Streamlit Community Cloud |

---

# 📂 Project Structure

```
TalentRank-AI
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── src
│   │
│   ├── config.py
│   │
│   ├── pipeline
│   │      └── ranking_pipeline.py
│   │
│   ├── vector_store
│   │      └── faiss_manager.py
│   │
│   ├── ranking
│   │      ├── hybrid_ranker.py
│   │      ├── recruiter_intelligence.py
│   │      ├── experience_ranker.py
│   │      ├── skill_ranker.py
│   │      ├── behavior_ranker.py
│   │      └── career_ranker.py
│   │
│   ├── jd_understanding
│   │      ├── jd_analyzer.py
│   │      └── jd_skill_extractor.py
│   │
│   ├── reasoning
│   │      └── reason_generator.py
│   │
│   ├── validation
│   │      └── honeypot_detector.py
│   │
│   └── utils
│          ├── artifact_downloader.py
│          └── artifact_utils.py
│
├── data
│
└── artifacts
      (Downloaded automatically from Hugging Face)
```

---

# 🔄 End-to-End Workflow

### Step 1 — Job Description Analysis

The recruiter provides a job description through the Streamlit interface.

The JD Analyzer extracts:

* Required technical skills
* Experience range
* Preferred technologies
* Candidate expectations

---

### Step 2 — Semantic Embedding

The complete job description is converted into a dense vector representation using the **BAAI/bge-small-en-v1.5** embedding model.

Unlike traditional keyword matching, semantic embeddings capture contextual meaning, allowing the system to identify relevant candidates even when different terminology is used.

---

### Step 3 — FAISS Candidate Retrieval

The generated embedding is searched against a FAISS vector index containing embeddings for **100,000 candidate profiles**.

The system retrieves the **Top 1000 semantically similar candidates** within milliseconds.

---

### Step 4 — Hybrid AI Ranking

Each retrieved candidate is evaluated using multiple ranking signals:

* Semantic similarity
* Skill matching
* Experience evaluation
* Career progression
* Behavioral assessment
* Recruiter intelligence
* Honeypot detection

These scores are combined using a weighted hybrid ranking algorithm to produce the final ranking score.

---

### Step 5 — Explainable AI

For every ranked candidate, TalentRank AI generates a human-readable explanation describing why the candidate is a strong match.

This provides transparency, improves recruiter confidence, and supports better hiring decisions.

---

### Step 6 — Interactive Dashboard

The Streamlit dashboard displays:

* Top ranked candidates
* Individual score breakdown
* Candidate profile
* AI-generated reasoning
* Downloadable submission report

---

# 🧩 Core Components

### 📌 JD Analyzer

Extracts structured hiring requirements from unstructured job descriptions.

---

### 📌 FAISS Manager

Performs high-speed semantic retrieval using dense vector embeddings.

---

### 📌 Hybrid Ranker

Combines multiple independent ranking signals into a unified candidate score.

---

### 📌 Recruiter Intelligence Module

Incorporates recruiter-focused heuristics to improve ranking quality.

---

### 📌 Honeypot Detector

Detects potentially suspicious or low-quality candidate profiles and applies ranking penalties when necessary.

---

### 📌 Reason Generator

Produces explainable AI reasoning that justifies the ranking of each candidate, making recommendations transparent and easier to interpret.

---
# 🧠 Hybrid AI Ranking Methodology

TalentRank AI does not rely solely on semantic similarity. Instead, it combines multiple independent ranking signals to evaluate each candidate comprehensively.

The final ranking score is computed using a weighted hybrid scoring approach that balances technical relevance, professional experience, career progression, and recruiter-oriented insights.

## Ranking Signals

| Signal                 | Description                                                                                              |
| ---------------------- | -------------------------------------------------------------------------------------------------------- |
| Semantic Score         | Measures contextual similarity between the Job Description and candidate profile using dense embeddings. |
| Skill Score            | Evaluates overlap between required and candidate skills.                                                 |
| Experience Score       | Assesses alignment between required and candidate experience.                                            |
| Career Score           | Rewards consistent career growth and relevant progression.                                               |
| Behavior Score         | Evaluates behavioral indicators extracted from candidate data.                                           |
| Recruiter Intelligence | Applies recruiter-focused heuristics to improve ranking quality.                                         |
| Honeypot Penalty       | Reduces the score of suspicious or low-quality profiles.                                                 |

---

# 📊 Candidate Scoring Pipeline

```text
Job Description
       │
       ▼
Semantic Retrieval (Top 1000)
       │
       ▼
Experience Evaluation
       │
       ▼
Skill Matching
       │
       ▼
Career Analysis
       │
       ▼
Behavior Assessment
       │
       ▼
Recruiter Intelligence
       │
       ▼
Honeypot Detection
       │
       ▼
Weighted Hybrid Score
       │
       ▼
Final Top 100 Candidates
```

---

# 🤖 Explainable AI

One of the key objectives of TalentRank AI is transparency.

Instead of returning only a numerical score, the system generates an explanation for every ranked candidate describing why they were selected.

Example:

```text
Candidate demonstrates strong semantic alignment with the job
requirements, possesses the required Python and LLM expertise,
matches the desired experience range, and shows consistent
career progression. Overall profile indicates an excellent fit
for the role.
```

This helps recruiters understand the reasoning behind every recommendation.

---

# ⚡ Performance

TalentRank AI is optimized for large-scale candidate retrieval.

| Metric                  |                     Value |
| ----------------------- | ------------------------: |
| Candidate Database      |          100,000 Profiles |
| Vector Search Engine    |                     FAISS |
| Retrieval Pool          |                  Top 1000 |
| Final Ranked Candidates |                   Top 100 |
| Embedding Model         |    BAAI/bge-small-en-v1.5 |
| Deployment              | Streamlit Community Cloud |

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/YashwanthDhadi/TalentRank-AI.git

cd TalentRank-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

# ☁️ Artifact Management

Large runtime artifacts are **not stored in the GitHub repository**.

Instead, TalentRank AI downloads them automatically from Hugging Face during application startup.

Downloaded artifacts include:

* FAISS Index
* Candidate Lookup Cache
* Candidate IDs
* Skill Vocabulary
* Dataset Statistics

This approach keeps the repository lightweight while supporting scalable deployment.

---

# 🌍 Deployment

TalentRank AI is deployed using **Streamlit Community Cloud**.

Deployment workflow:

```text
GitHub Repository
        │
        ▼
Streamlit Cloud
        │
        ▼
Install Dependencies
        │
        ▼
Download Artifacts from Hugging Face
        │
        ▼
Load FAISS Index
        │
        ▼
Launch Dashboard
```

---

# 📸 Application Screenshots

Add screenshots here after deployment.

## Dashboard

```text
docs/dashboard.png
```

## Candidate Ranking

```text
docs/ranking.png
```

## AI Explanation

```text
docs/reasoning.png
```

---

# 📈 Scalability

TalentRank AI is designed with scalability in mind.

Current capabilities include:

* Semantic search across 100,000 candidate profiles
* Automatic artifact management
* Modular ranking architecture
* Explainable AI reasoning
* Cloud-ready deployment

The modular design allows additional ranking signals, embedding models, or vector databases to be integrated with minimal changes.

---

# 🔮 Future Improvements

Planned enhancements include:

* Support for multiple embedding models
* Hybrid dense + sparse retrieval
* Learning-to-Rank algorithms
* Recruiter feedback loop
* Resume PDF parsing
* Multi-job batch ranking
* Candidate recommendation history
* Advanced analytics dashboard
* REST API for enterprise integration
* Docker-based deployment

---
