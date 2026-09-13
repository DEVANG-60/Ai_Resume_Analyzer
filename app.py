import streamlit as st
import pandas as pd
import plotly.express as px

from resume_parser import extract_resume_text
from text_cleaner import clean_text

from skill_extractor import (
    extract_skills,
    get_skill_categories
)

from job_matcher import (
    calculate_match_scores,
    get_role_skills,
    find_missing_skills
)

from roadmap_generator import generate_roadmap


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 650;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered Resume Analysis & Job Recommendation System'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload your resume to discover suitable job roles, "
    "analyze your skills, identify skill gaps and generate "
    "a personalized learning roadmap."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Resume Analyzer")

st.sidebar.write(
    "Upload your resume to begin the analysis."
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX"
)

st.sidebar.divider()

st.sidebar.info(
    "The system evaluates job-related skills, "
    "text similarity and project/experience evidence."
)


# =========================================================
# MAIN APPLICATION
# =========================================================

if uploaded_file:

    # -----------------------------------------------------
    # FILE INFORMATION
    # -----------------------------------------------------

    st.success(
        f"✅ Resume uploaded successfully: {uploaded_file.name}"
    )

    # -----------------------------------------------------
    # RESUME TEXT EXTRACTION
    # -----------------------------------------------------

    with st.spinner("📖 Reading and extracting resume text..."):

        raw_text = extract_resume_text(
            uploaded_file
        )

    if not raw_text.strip():

        st.error(
            "❌ Could not extract text from this resume."
        )

        st.warning(
            "Please make sure your PDF contains selectable "
            "text or upload another resume."
        )

        st.stop()

    # -----------------------------------------------------
    # TEXT CLEANING
    # -----------------------------------------------------

    cleaned_text = clean_text(
        raw_text
    )

    # -----------------------------------------------------
    # SKILL EXTRACTION
    # -----------------------------------------------------

    with st.spinner("🧠 Detecting skills..."):

        skills = extract_skills(
            cleaned_text
        )

    # -----------------------------------------------------
    # SKILL CATEGORIES
    # -----------------------------------------------------

    categories = get_skill_categories(
        skills
    )

    # -----------------------------------------------------
    # JOB ROLE MATCHING
    # -----------------------------------------------------

    with st.spinner("🎯 Analyzing job-role compatibility..."):

        results = calculate_match_scores(
            cleaned_text,
            skills
        )

    # =====================================================
    # RESUME OVERVIEW
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Resume Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🧠 Skills Detected",
        len(skills)
    )

    col2.metric(
        "💼 Roles Analyzed",
        len(results)
    )

    col3.metric(
        "🏆 Top Match",
        results.iloc[0]["Role"]
    )

    st.divider()


    # =====================================================
    # SKILLS DETECTED
    # =====================================================

    st.markdown(
        '<div class="section-title">🧠 Skills Detected</div>',
        unsafe_allow_html=True
    )

    if skills:

        st.write(
            f"The system detected **{len(skills)} job-related "
            f"skills** from your resume."
        )

        for category, category_skills in categories.items():

            st.markdown(
                f"### {category}"
            )

            skill_text = " • ".join(
                category_skills
            )

            st.success(
                skill_text
            )

    else:

        st.warning(
            "⚠️ No predefined technical skills were detected."
        )

        st.info(
            "Try uploading a resume containing clearly "
            "listed technical skills."
        )

    st.divider()


    # =====================================================
    # TOP JOB RECOMMENDATIONS
    # =====================================================

    st.markdown(
        '<div class="section-title">🎯 Recommended Job Roles</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Based on your resume, these are the three roles "
        "with the highest calculated match scores."
    )

    top_roles = results.head(3)

    display_results = top_roles[
        [
            "Role",
            "Match Score",
            "Skill Coverage",
            "Text Similarity"
        ]
    ].copy()

    display_results["Match Score"] = (
            display_results["Match Score"]
            .round(2)
            .astype(str)
            + "%"
    )

    display_results["Skill Coverage"] = (
            display_results["Skill Coverage"]
            .round(2)
            .astype(str)
            + "%"
    )

    display_results["Text Similarity"] = (
            display_results["Text Similarity"]
            .round(2)
            .astype(str)
            + "%"
    )

    display_results.columns = [
        "Job Role",
        "Overall Match",
        "Skill Coverage",
        "Text Similarity"
    ]

    st.dataframe(
        display_results,
        use_container_width=True,
        hide_index=True
    )

    st.divider()


    # =====================================================
    # MATCH SCORE CHART
    # =====================================================

    st.markdown(
        '<div class="section-title">📈 Role Match Analysis</div>',
        unsafe_allow_html=True
    )

    chart_data = results.copy()

    chart_data["Match Score"] = (
        chart_data["Match Score"]
        .astype(float)
    )

    fig = px.bar(
        chart_data,
        x="Match Score",
        y="Role",
        orientation="h",
        title="Resume-to-Role Match Score",
        labels={
            "Match Score": "Match Score (%)",
            "Role": "Job Role"
        }
    )

    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        },
        xaxis={
            "range": [0, 100]
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()


    # =====================================================
    # TARGET ROLE ANALYSIS
    # =====================================================

    st.markdown(
        '<div class="section-title">🎯 Analyze a Target Role</div>',
        unsafe_allow_html=True
    )

    selected_role = st.selectbox(
        "Select a job role to analyze in detail:",
        results["Role"].tolist()
    )


    # -----------------------------------------------------
    # SELECTED ROLE SCORE
    # -----------------------------------------------------

    selected_result = results[
        results["Role"] == selected_role
        ].iloc[0]


    selected_score = selected_result[
        "Match Score"
    ]

    skill_coverage = selected_result[
        "Skill Coverage"
    ]

    text_similarity = selected_result[
        "Text Similarity"
    ]

    evidence_score = selected_result[
        "Evidence Score"
    ]


    st.subheader(
        f"📌 {selected_role}"
    )


    # -----------------------------------------------------
    # MAIN SCORE
    # -----------------------------------------------------

    st.metric(
        "Overall Resume Match",
        f"{selected_score}%"
    )


    # -----------------------------------------------------
    # SCORE BREAKDOWN
    # -----------------------------------------------------

    st.write(
        "**Explainable Score Breakdown**"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Skill Coverage",
        f"{skill_coverage}%"
    )

    col2.metric(
        "Text Similarity",
        f"{text_similarity}%"
    )

    col3.metric(
        "Project / Experience Evidence",
        f"{evidence_score}%"
    )


    st.caption(
        "Final score = 50% Skill Coverage + "
        "30% Text Similarity + 20% Project/Experience Evidence"
    )

    st.divider()


    # =====================================================
    # REQUIRED SKILLS
    # =====================================================

    role_skills = get_role_skills(
        selected_role
    )


    # =====================================================
    # SKILLS FOUND FOR ROLE
    # =====================================================

    st.subheader(
        "✅ Skills Found for This Role"
    )

    found_for_role = []

    for skill in role_skills:

        if skill.lower() in [
            resume_skill.lower()
            for resume_skill in skills
        ]:

            found_for_role.append(
                skill
            )


    if found_for_role:

        for skill in found_for_role:

            st.success(
                f"✓ {skill}"
            )

    else:

        st.info(
            "No required skills for this role "
            "were detected in the resume."
        )


    # =====================================================
    # MISSING SKILLS
    # =====================================================

    missing_skills = find_missing_skills(
        skills,
        role_skills
    )


    st.subheader(
        "⚠️ Skill Gap Analysis"
    )

    if missing_skills:

        st.write(
            f"The system identified **{len(missing_skills)} "
            f"skills** that are currently not detected "
            f"in your resume for this role."
        )

        for skill in missing_skills:

            st.warning(
                f"⚠️ {skill}"
            )

    else:

        st.success(
            "🎉 Excellent! All listed role skills "
            "were detected in your resume."
        )

    st.divider()


    # =====================================================
    # LEARNING ROADMAP
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🚀 Personalized Learning Roadmap'
        '</div>',
        unsafe_allow_html=True
    )

    if missing_skills:

        st.write(
            "Based on the identified skill gaps, "
            "the system recommends the following "
            "learning path:"
        )

        roadmap = generate_roadmap(
            missing_skills
        )

        if roadmap:

            for index, item in enumerate(
                    roadmap,
                    start=1
            ):

                st.subheader(
                    f"Step {index}: {item['skill']}"
                )

                for step in item["steps"]:

                    st.write(
                        f"• {step}"
                    )

        else:

            st.info(
                "A roadmap is not available yet for "
                "the detected missing skills."
            )

    else:

        st.success(
            "🎓 No additional learning topics are "
            "required based on the current role dataset."
        )

    st.divider()


    # =====================================================
    # ROLE DESCRIPTION
    # =====================================================

    st.markdown(
        '<div class="section-title">💼 Role Information</div>',
        unsafe_allow_html=True
    )

    role_description = selected_result[
        "Description"
    ]

    st.info(
        role_description
    )

    st.divider()


    # =====================================================
    # RESPONSIBLE AI
    # =====================================================

    st.markdown(
        '<div class="section-title">ℹ️ Responsible AI</div>',
        unsafe_allow_html=True
    )

    st.info(
        "This application is designed for career guidance "
        "and educational purposes. Match scores are estimates "
        "based on job-related resume information and should "
        "not be treated as automatic hiring or rejection decisions."
    )

    st.write(
        "The system focuses on skills, projects, education "
        "and relevant experience rather than protected "
        "personal attributes."
    )


else:

    # =====================================================
    # EMPTY STATE
    # =====================================================

    st.info(
        "👈 Upload a PDF or DOCX resume from the sidebar "
        "to begin your analysis."
    )

    st.markdown(
        """
        ### 🔍 What this system can do

        **1. 📄 Resume Analysis**  
        Extract text from PDF and DOCX resumes.

        **2. 🧠 Skill Detection**  
        Identify technical and job-related skills.

        **3. 🎯 Job Recommendation**  
        Compare your resume with multiple job roles.

        **4. 📊 Match Score**  
        Calculate an explainable resume-to-role score.

        **5. ⚠️ Skill Gap Analysis**  
        Identify skills missing for your target role.

        **6. 🚀 Learning Roadmap**  
        Generate learning topics based on your skill gaps.
        """
    )