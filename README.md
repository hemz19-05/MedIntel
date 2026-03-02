# MedIntel — AI-Powered Drug Information Assistant

## Overview
**MedIntel** is a rule-based + AI-powered drug information app designed to provide **accurate, factual, FDA-backed drug information**.

Instead of showing users long drug label documents like Google searches, MedIntel:
- detects the **user’s intent**
- retrieves verified data from trusted drug APIs
- generates a **clear educational summary** using an LLM (OpenAI)

✅ This reduces confusion, improves clarity, and helps avoid hallucinated responses.

The results:

Variant A - short bullet points responses achieved higher BERTScore (semantic similarity) - 0.7742
Variant B - detailed explanatory responses achieved slightly lower BERTScore (semantic similarity) - 0.7176
Variant A achieved 7% higher BERTScore F1 due to closer lexical and semantic alignment with OpenFDA reference text.

---

## Key Features

### 🔍 Drug Search (FDA Verified)
- Search by **generic name** (e.g., *Metformin*)
- Search by **brand name** (e.g., *Exforge*)
- Retrieves official drug details using **OpenFDA + RxNorm**

### 🎯 Intent Detection
MedIntel detects the user’s intent and tailors the answer, for example:
- dosage / usage
- warnings
- pregnancy safety
- side effects
- contraindications

### 🧠 AI Educational Summary (OpenAI)
Generates a short, user-friendly response that is:
- easy to understand
- grounded in drug label context
- safer than general search AI outputs

### 📊 Analytics Dashboard (Persistent)
Every drug search is logged into a database, allowing:
- total searches
- unique drugs searched
- top searched drugs
- A/B testing tracking via response variants

---

## Tech Stack

| Layer | Technologies |
|------|--------------|
| **Frontend / UI** | Streamlit |
| **Backend** | Python |
| **Drug Data APIs** | OpenFDA, RxNorm |
| **AI Layer** | OpenAI API |
| **Database** | PostgreSQL |
| **Deployment** | Render |

---

## Database Logging (Postgres)
All searches are stored in the table:

### `query_logs`
- `drug_name`
- `variant`
- `created_at`

This enables analytics to persist across deployments and refreshes.

---

## Setup (Run Locally)

### 1️⃣ Clone repo
```bash
git clone https://github.com/<your-username>/MedIntel.git
cd MedIntel









