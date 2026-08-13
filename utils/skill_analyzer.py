def find_skills(resume_text, skills):
    resume_text = resume_text.lower()

    found_skills = []

    for skill in skills:
        if skill["name"].lower() in resume_text:
            found_skills.append(skill["name"])

    return found_skills


def calculate_score(found_skills, total_skills):
    if total_skills == 0:
        return 0

    score = (len(found_skills) / total_skills) * 100

    return round(score, 2)


def generate_recommendations(missing_skills):
    recommendations = []

    for skill in missing_skills:
        recommendations.append(
            f"Consider adding or improving {skill} in your resume."
        )

    return recommendations


def calculate_job_match(resume_text, job_description, skills):
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    required_skills = []

    for skill in skills:
        if skill["name"].lower() in job_description:
            required_skills.append(skill["name"])

    if not required_skills:
        return 0, []

    matched_skills = []

    for skill in required_skills:
        if skill.lower() in resume_text:
            matched_skills.append(skill)

    match_score = (len(matched_skills) / len(required_skills)) * 100

    return round(match_score, 2), required_skills
def get_match_level(score):
    if score >= 80:
        return "Excellent Match"
    elif score >= 60:
        return "Good Match"
    elif score >= 40:
        return "Average Match"
    else:
        return "Needs Improvement"