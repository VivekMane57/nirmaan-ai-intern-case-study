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

Where:

Keyword Score (0–1) → keyword overlap

Semantic Score (0–1) → embedding similarity

Length Penalty (0.4–1) → target word count

Weight → from rubric file

## 📸 Project Screenshots

Here are sample outputs from the Streamlit evaluation tool:

### 🖥️ Application Interface
<img src="https://github.com/user-attachments/assets/b7ae427d-9a56-49d4-90cd-04a8c2e62ba1" width="800"/>

---

### 📊 Scoring Result (Overall Score + Word Count)
<img src="https://github.com/user-attachments/assets/8073c39c-a96c-4f1e-8b69-735be394e671" width="800"/>

---

### 📈 Per-Criterion Breakdown & Feedback
<img src="https://github.com/user-attachments/assets/b6ac432e-7e87-4aa3-9205-2174ad0fad5b" width="800"/>


📂 Project Structure
<img width="784" height="492" alt="image" src="https://github.com/user-attachments/assets/fc6913de-1dcf-4478-bd3f-93b925dc82d5" />

🛠️ Installation
1️⃣ Clone the repository
git clone https://github.com/VivekMane57/nirmaan-ai-intern-case-study.git
cd nirmaan-ai-intern-case-study
2️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
▶️ Running the App
streamlit run app.py
🖥️ User Flow
Open the Streamlit app

Expand “View rubric (from Excel)” to inspect the rubric

Paste a student’s transcript into the text area

Click Score

View:Overall score

Word count

Per-criterion breakdown

Detailed feedback and JSON output

🎯 Purpose

This project demonstrates:

Converting a rubric-based evaluation problem into a reproducible scoring pipeline

Combining classical rule-based checks with modern NLP similarity models

Building a simple but effective evaluation dashboard with Streamlit

Writing clean, modular, and readable code suitable for collaboration

It is designed specifically for the Nirmaan Education AI Intern Case Study.
---

👤 Author

Vivek Mane
B.Tech CSE – DY Patil College of Engineering & Technology
AI/ML • Data Engineering • Full Stack

GitHub: VivekMane57
## 📸 Project Screenshots

Here are sample outputs from the Streamlit evaluation tool:

### 🖥️ Application Interface
<img src="https://github.com/user-attachments/assets/b7ae427d-9a56-49d4-90cd-04a8c2e62ba1" width="800"/>

---

### 📊 Scoring Result (Overall Score + Word Count)
<img src="https://github.com/user-attachments/assets/8073c39c-a96c-4f1e-8b69-735be394e671" width="800"/>

---

### 📈 Per-Criterion Breakdown & Feedback
<img src="https://github.com/user-attachments/assets/b6ac432e-7e87-4aa3-9205-2174ad0fad5b" width="800"/>



 





