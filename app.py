# app.py

import streamlit as st
import pandas as pd

from scoring import load_rubric, score_transcript

# -------------------- File Paths -------------------- #
RUBRIC_PATH = "data/rubric.xlsx"
SAMPLE_TRANSCRIPT_PATH = "data/sample_transcript.txt"


# -------------------- Caching -------------------- #
@st.cache_data
def get_rubric_df():
    return load_rubric(RUBRIC_PATH)


@st.cache_data
def load_sample_transcript():
    try:
        with open(SAMPLE_TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""


# -------------------- Main App -------------------- #
def main():

    st.set_page_config(
        page_title="Nirmaan – Spoken Introduction Scoring Tool",
        page_icon="🧠",
        layout="wide",
    )

    st.title("Nirmaan – Spoken Introduction Scoring Tool")

    st.write(
        """
Paste a student's self-introduction transcript below and click **Score**
to get a rubric-based evaluation **(0–100)** with per-criterion feedback.
"""
    )

    # ---------------- Load Rubric ---------------- #
    rubric_df = get_rubric_df()

    with st.expander("View rubric (from Excel)"):
        # FIX: Convert everything to string so Arrow doesn't crash
        st.dataframe(rubric_df.astype(str), use_container_width=True)

    # ---------------- Transcript Input ---------------- #
    default_text = load_sample_transcript()

    transcript_input = st.text_area(
        "Transcript text",
        value=default_text,
        height=220,
        help="Paste the student's self-introduction transcript here.",
    )

    # ---------------- Score Button ---------------- #
    if st.button("Score", type="primary"):

        if not transcript_input.strip():
            st.warning("Please paste a transcript first.")
            return

        with st.spinner("Scoring transcript..."):
            result = score_transcript(transcript_input, rubric_df)

        st.success("Scoring complete!")

        # ---------------- Overall Result ---------------- #
        st.subheader("Overall Result")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Score (0–100)", result["overall_score"])
        with col2:
            st.metric("Word Count", result["word_count"])

        # ---------------- Criterion Table ---------------- #
        st.subheader("Per-criterion Breakdown")

        crit_df = pd.DataFrame(result["per_criterion"])

        st.dataframe(
            crit_df[
                [
                    "criterion",
                    "weight",
                    "keyword_score",
                    "semantic_score",
                    "length_penalty",
                    "final_score_0_1",
                ]
            ],
            use_container_width=True,
        )

        # ---------------- Detailed Feedback ---------------- #
        st.subheader("Detailed Feedback")

        for c in result["per_criterion"]:
            with st.expander(f"{c['criterion']}"):
                st.write(f"**Final Score (0–1):** {c['final_score_0_1']}")
                st.write(f"- Keyword Score: **{c['keyword_score']}**")
                st.write(f"- Semantic Score: **{c['semantic_score']}**")
                st.write(f"- Length Penalty: **{c['length_penalty']}**")

                if c["keywords_found"]:
                    st.write(
                        "- Keywords Found:",
                        ", ".join(sorted(set(c["keywords_found"]))),
                    )

                if c["keywords_missing"]:
                    st.write(
                        "- Keywords Missing:",
                        ", ".join(sorted(set(c["keywords_missing"]))),
                    )

                if c["length_feedback"]:
                    st.write(f"- Length Feedback: {c['length_feedback']}")

        # ---------------- Raw JSON Output ---------------- #
        st.subheader("Raw JSON Output (for debugging / API use)")
        st.json(result)


# -------------------- Run App -------------------- #
if __name__ == "__main__":
    main()
