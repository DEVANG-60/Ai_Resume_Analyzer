import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_job_roles():
    return pd.read_csv("data/job_roles.csv")


def get_role_skills(role):
    jobs = load_job_roles()

    selected = jobs[jobs["Role"] == role]

    if selected.empty:
        return []

    skills = selected.iloc[0]["Skills"]

    return [
        skill.strip()
        for skill in skills.split(",")
    ]


def calculate_text_similarity(resume_text, role_skills):
    """
    Calculates similarity between resume text
    and required skills for a role.
    """

    role_text = " ".join(role_skills)

    documents = [
        resume_text,
        role_text
    ]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return similarity * 100


def calculate_skill_coverage(resume_skills, role_skills):
    """
    Calculates percentage of required skills
    found in the resume.
    """

    if not role_skills:
        return 0

    resume_skills_lower = {
        skill.lower()
        for skill in resume_skills
    }

    found = 0

    for skill in role_skills:

        if skill.lower() in resume_skills_lower:
            found += 1

    coverage = (
                       found / len(role_skills)
               ) * 100

    return coverage


def calculate_evidence_score(resume_text):
    """
    Gives a simple evidence score based on
    presence of project and experience sections.
    """

    text = resume_text.lower()

    project_keywords = [
        "project",
        "projects",
        "developed",
        "built",
        "implemented",
        "created"
    ]

    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "worked",
        "employment"
    ]

    project_count = sum(
        1 for word in project_keywords
        if word in text
    )

    experience_count = sum(
        1 for word in experience_keywords
        if word in text
    )

    project_score = min(
        project_count * 10,
        50
    )

    experience_score = min(
        experience_count * 10,
        50
    )

    return project_score + experience_score


def calculate_role_score(
        resume_text,
        resume_skills,
        role_skills
):

    text_similarity = calculate_text_similarity(
        resume_text,
        role_skills
    )

    skill_coverage = calculate_skill_coverage(
        resume_skills,
        role_skills
    )

    evidence_score = calculate_evidence_score(
        resume_text
    )

    final_score = (
            (skill_coverage * 0.50)
            + (text_similarity * 0.30)
            + (evidence_score * 0.20)
    )

    return {
        "Final Score": round(final_score, 2),
        "Skill Coverage": round(skill_coverage, 2),
        "Text Similarity": round(text_similarity, 2),
        "Evidence Score": round(evidence_score, 2)
    }


def calculate_match_scores(
        resume_text,
        resume_skills
):

    jobs = load_job_roles()

    results = []

    for _, job in jobs.iterrows():

        role = job["Role"]

        role_skills = [
            skill.strip()
            for skill in job["Skills"].split(",")
        ]

        scores = calculate_role_score(
            resume_text,
            resume_skills,
            role_skills
        )

        results.append({
            "Role": role,
            "Match Score": scores["Final Score"],
            "Skill Coverage": scores["Skill Coverage"],
            "Text Similarity": scores["Text Similarity"],
            "Evidence Score": scores["Evidence Score"],
            "Description": job["Description"]
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="Match Score",
        ascending=False
    )

    return results_df.reset_index(drop=True)


def find_missing_skills(
        resume_skills,
        role_skills
):

    resume_lower = {
        skill.lower()
        for skill in resume_skills
    }

    missing = []

    for skill in role_skills:

        if skill.lower() not in resume_lower:
            missing.append(skill)

    return missing