# 📘 Nirmaan – Spoken Introduction Scoring Tool

An AI-assisted evaluation tool that analyzes a student’s **spoken introduction transcript** and scores it using a **rubric-driven, hybrid NLP scoring system**.  
This project is built as part of the **Nirmaan Education AI Internship Case Study (2025–26)**.

---

## 🚀 Overview

This system evaluates a student’s self-introduction by combining:

- ✔ **Rule-based scoring** (keywords, weights, rubric criteria)  
- ✔ **Semantic similarity** (Transformer embeddings)  
- ✔ **Length and formatting analysis** (word count, duration, etc.)  
- ✔ **Weighted scoring** (0–100 final score)  
- ✔ **Per-criterion transparent feedback**

All evaluation logic is powered by the **rubric Excel file**, which makes the tool fully configurable.

The UI is developed using **Streamlit** so evaluators can simply paste a transcript and instantly view the results.

---

## ✨ Features

### 🔹 1. Rubric-Driven Evaluation  
The system reads scoring rules from `data/rubric.xlsx`, including:
- Criterion name  
- Keywords  
- Weight  
- Target length  
- Meta rows (word count, duration, etc.)

### 🔹 2. Hybrid Scoring System  
Each rubric criterion is scored using:

| Component | Description |
|----------|-------------|
| **Keyword Score** | Percentage of rubric keywords found in transcript |
| **Semantic Score** | Cosine similarity using `sentence-transformers/all-MiniLM-L6-v2` |
| **Length Penalty** | Penalizes too short / too long responses |
| **Weighted Aggregation** | Each criterion contributes based on its weight |

### 🔹 3. Clean Web Interface  
Built with Streamlit:
- Paste transcript  
- Click **Score**  
- View results instantly  
- Includes per-criterion table and detailed expandable feedback

### 🔹 4. Transparent Output  
The tool shows:
- Overall Score (0–100)  
- Word Count  
- Criterion breakdown  
- Keywords found vs missing  
- Semantic alignment  
- Length feedback  
- JSON output for debugging

---

## 🧠 How Scoring Works

For each rubric row:

```text
final_score = (0.5 * keyword_score + 0.5 * semantic_score) * length_penalty
