"""
TalentRank-AI

Streamlit Recruiter Dashboard
"""

from time import perf_counter

import pandas as pd
import streamlit as st

from src.reasoning.reason_generator import ReasonGenerator
from src.jd_understanding.jd_analyzer import JDAnalyzer
from src.pipeline.ranking_pipeline import RankingPipeline


# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="TalentRank AI",
    page_icon="🎯",
    layout="wide"
)


# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "results" not in st.session_state:
    st.session_state.results = None

if "runtime" not in st.session_state:
    st.session_state.runtime = None


# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.title("🎯 TalentRank AI")

st.caption(
    "AI-Powered Candidate Ranking using Semantic Search + Hybrid Ranking"
)

st.divider()


# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.title("🎯 TalentRank AI")

    st.caption("AI-Powered Candidate Ranking System")

    st.divider()

    st.subheader("📊 System Overview")

    st.metric("Database", "100,000 Candidates")
    st.metric("Retrieval Pool", "Top 1000")
    st.metric("Final Ranking", "Top 100")

    st.divider()

    st.subheader("🧠 AI Engine")

    st.write("**Embedding Model**")
    st.caption("BAAI / bge-small-en-v1.5")

    st.write("**Vector Search**")
    st.caption("FAISS")

    st.write("**Ranking Engine**")
    st.caption("Hybrid AI Ranking")

    st.divider()

    st.subheader("🟢 System Status")

    st.success("Backend Online")

    if st.session_state.runtime is not None:
        st.metric(
            "Last Runtime",
            f"{st.session_state.runtime:.2f} sec"
        )


# -------------------------------------------------------
# Job Description
# -------------------------------------------------------

st.subheader("Job Description")

default_jd = """Senior AI Engineer

Experience Required: 5-9

Required Skills

Python
LLM
Embeddings
Retrieval
FAISS
Hybrid Search
Sentence Transformers
Ranking
Evaluation
Milvus
Qdrant
Pinecone
Weaviate

Preferred

PEFT
LoRA
QLoRA
Learning-to-Rank
Distributed Systems
"""

jd = st.text_area(

    "Paste Job Description",

    value=default_jd,

    height=300

)
analyzed_jd = JDAnalyzer(jd).analyze()


# -------------------------------------------------------
# Rank Button
# -------------------------------------------------------

rank_button = st.button(

    "🚀 Rank Candidates",

    use_container_width=True

)


# -------------------------------------------------------
# Ranking
# -------------------------------------------------------

if rank_button:

    with st.spinner("Ranking candidates..."):

        start = perf_counter()

        pipeline = RankingPipeline()

        results = pipeline.rank(

            jd,

            top_k=100

        )
        

        end = perf_counter()

        st.session_state.results = results

        st.session_state.runtime = round(

            end - start,

            3

        )

        st.success("Ranking Completed")


# -------------------------------------------------------
# Results
# -------------------------------------------------------

if st.session_state.results is not None:

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Candidates Ranked",

        len(st.session_state.results)

    )

    col2.metric(

        "Runtime",

        f"{st.session_state.runtime}s"

    )

    col3.metric(

        "FAISS Search",

        "100000 Candidates"

    )

    table = []

    for rank, candidate in enumerate(

        st.session_state.results,

        start=1

    ):

        table.append(

            {

                "Rank": rank,

                "Candidate ID": candidate["candidate_id"],

                "Score": candidate["final_score"]

            }

        )

    df = pd.DataFrame(table)

    st.subheader("Top Ranked Candidates")

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )

    # -------------------------------------------------------
# Candidate Details
# -------------------------------------------------------

if st.session_state.results is not None:

    st.divider()

    st.subheader("Candidate Details")

    candidate_ids = [
        candidate["candidate_id"]
        for candidate in st.session_state.results
    ]

    selected_candidate = st.selectbox(
        "Select Candidate",
        candidate_ids
    )

    candidate = next(
        item
        for item in st.session_state.results
        if item["candidate_id"] == selected_candidate
    )

    profile = candidate["candidate"]

    left, right = st.columns([2, 1])

    # ---------------------------------------------------
    # Left Column
    # ---------------------------------------------------

    with left:

        st.markdown("### Candidate Profile")

        st.write(
            f"**Candidate ID:** {candidate['candidate_id']}"
        )

        if profile.get("current_title"):
            st.write(
                f"**Current Title:** {profile['current_title']}"
            )

        st.write(
            f"**Experience:** {profile['experience']} years"
        )

        st.markdown("#### Skills")

        skills = profile.get("skills", [])

        if skills:

            skill_names = []

            for skill in skills:

                if isinstance(skill, dict):

                    skill_names.append(
                        skill.get("name", "")
                    )

                else:

                    skill_names.append(
                        str(skill)
                    )

            st.write(", ".join(skill_names))

        else:

            st.info("No skills available.")

        st.markdown("#### AI Explanation")

        reasoning = ReasonGenerator.generate(
            profile,
            analyzed_jd,
            {
                "semantic_score": candidate["semantic_score"],
                "experience_score": candidate["experience_score"],
                "skill_score": candidate["skill_score"],
                "behavior_score": candidate["behavior_score"],
                "career_score": candidate["career_score"],
                "recruiter_score": candidate["recruiter_score"],
                "final_score": candidate["final_score"],
            },
        )
        st.success(reasoning)
    # ---------------------------------------------------
    # Right Column
    # ---------------------------------------------------

    with right:

        st.markdown("### Scores")

        st.metric(
            "Final Score",
            candidate["final_score"]
        )

        st.metric(
            "Semantic",
            candidate["semantic_score"]
        )

        st.metric(
            "Skills",
            candidate["skill_score"]
        )

        st.metric(
            "Experience",
            candidate["experience_score"]
        )

        st.metric(
            "Career",
            candidate["career_score"]
        )

        st.metric(
            "Behavior",
            candidate["behavior_score"]
        )

        st.metric(
            "Recruiter",
            candidate["recruiter_score"]
        )

        if "honeypot_penalty" in candidate:

            st.metric(
                "Honeypot Penalty",
                candidate["honeypot_penalty"]
            )


# -------------------------------------------------------
# Download Submission
# -------------------------------------------------------

if st.session_state.results is not None:

    submission = []

    for rank, candidate in enumerate(
        st.session_state.results,
        start=1
    ):

        submission.append(
            {
                "candidate_id": candidate["candidate_id"],
                "rank": rank,
                "score": candidate["final_score"],
                "reasoning": ReasonGenerator.generate(
                    candidate["candidate"],
                    analyzed_jd,
                    {
                        "semantic_score": candidate["semantic_score"],
                        "experience_score": candidate["experience_score"],
                        "skill_score": candidate["skill_score"],
                        "behavior_score": candidate["behavior_score"],
                        "career_score": candidate["career_score"],
                        "recruiter_score": candidate["recruiter_score"],
                        "final_score": candidate["final_score"],
                    },
            ),
            }
        )

    submission_df = pd.DataFrame(submission)

    csv = submission_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Submission CSV",
        data=csv,
        file_name="submission.csv",
        mime="text/csv",
        use_container_width=True,
    )


# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()

st.markdown(
    """
    <center>

    <h4>TalentRank AI</h4>

    AI-Powered Candidate Ranking Engine

    Semantic Search • Hybrid Ranking • Explainable AI

    </center>
    """,
    unsafe_allow_html=True,
)