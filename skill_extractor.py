import pandas as pd
import re


def load_skills():
    skills_df = pd.read_csv("data/skill_dictionary.csv")
    return skills_df


def extract_skills(text):
    skills_df = load_skills()

    found_skills = []

    for skill in skills_df["Skill"]:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text.lower()):
            found_skills.append(skill)

    return found_skills


def get_skill_categories(skills):
    skills_df = load_skills()

    result = {}

    for _, row in skills_df.iterrows():

        if row["Skill"] in skills:
            category = row["Category"]

            if category not in result:
                result[category] = []

            result[category].append(row["Skill"])

    return result