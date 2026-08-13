from flask import Flask, render_template, request
from database.database import (
    get_connection,
    get_skills,
    save_resume,
    save_resume_skills,
    save_job,
    save_job_skills
)
from utils.pdf_reader import extract_text_from_pdf
from utils.skill_analyzer import (
    find_skills,
    calculate_score,
    generate_recommendations,
    calculate_job_match,
    get_match_level
)
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test-db")
def test_db():
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()

        return "<h2>Database connected successfully! ✅</h2>"

    except Exception as e:
        return f"""
        <h2>Database connection failed ❌</h2>
        <p>{e}</p>
        """


@app.route("/skills")
def skills():
    skills = get_skills()

    html = "<h1>My Skills</h1><ul>"

    for skill in skills:
        html += f"<li>{skill['name']}</li>"

    html += "</ul>"

    return html


@app.route("/upload", methods=["POST"])
def upload():

    # Check resume file
    if "resume" not in request.files:
        return "<h2>No resume selected ❌</h2>"

    file = request.files["resume"]

    if file.filename == "":
        return "<h2>No resume selected ❌</h2>"

    # Get job description
    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    if not job_description:
        return "<h2>Please enter a job description ❌</h2>"

    # Save uploaded file
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(file_path)

    try:

        # -------------------------------------------------
        # 1. SAVE RESUME
        # -------------------------------------------------

        resume_id = save_resume(
            file.filename
        )


        # -------------------------------------------------
        # 2. SAVE JOB DESCRIPTION
        # -------------------------------------------------

        job_id = save_job(
            "Job Description",
            job_description
        )


        # -------------------------------------------------
        # 3. EXTRACT RESUME TEXT
        # -------------------------------------------------

        resume_text = extract_text_from_pdf(
            file_path
        )


        # -------------------------------------------------
        # 4. GET SKILLS FROM DATABASE
        # -------------------------------------------------

        skills_from_database = get_skills()


        # -------------------------------------------------
        # 5. FIND SKILLS IN RESUME
        # -------------------------------------------------

        found_skills = find_skills(
            resume_text,
            skills_from_database
        )


        # -------------------------------------------------
        # 6. SAVE RESUME SKILLS
        # -------------------------------------------------

        save_resume_skills(
            resume_id,
            found_skills
        )


        # -------------------------------------------------
        # 7. CALCULATE RESUME SCORE
        # -------------------------------------------------

        total_skills = len(
            skills_from_database
        )

        score = calculate_score(
            found_skills,
            total_skills
        )


        # -------------------------------------------------
        # 8. FIND MISSING RESUME SKILLS
        # -------------------------------------------------

        missing_skills = [
            skill["name"]
            for skill in skills_from_database
            if skill["name"] not in found_skills
        ]


        # -------------------------------------------------
        # 9. GENERATE RECOMMENDATIONS
        # -------------------------------------------------

        recommendations = generate_recommendations(
            missing_skills
        )


        # -------------------------------------------------
        # 10. CALCULATE JOB MATCH
        # -------------------------------------------------

        job_match_score, required_skills = calculate_job_match(
            resume_text,
            job_description,
            skills_from_database
        )


        # -------------------------------------------------
        # 11. GET MATCH LEVEL
        # -------------------------------------------------

        match_level = get_match_level(
            job_match_score
        )


        # -------------------------------------------------
        # 12. SAVE REQUIRED JOB SKILLS
        # -------------------------------------------------

        save_job_skills(
            job_id,
            required_skills
        )


        # -------------------------------------------------
        # 13. FIND MATCHED JOB SKILLS
        # -------------------------------------------------

        resume_text_lower = resume_text.lower()

        matched_job_skills = [
            skill
            for skill in required_skills
            if skill.lower() in resume_text_lower
        ]


        # -------------------------------------------------
        # 14. FIND MISSING JOB SKILLS
        # -------------------------------------------------

        missing_job_skills = [
            skill
            for skill in required_skills
            if skill not in matched_job_skills
        ]


        # -------------------------------------------------
        # 15. DISPLAY RESULT PAGE
        # -------------------------------------------------

        return render_template(
            "result.html",

            filename=file.filename,

            score=score,

            found_skills=found_skills,

            missing_skills=missing_skills,

            recommendations=recommendations,

            job_description=job_description,

            job_match_score=job_match_score,

            match_level=match_level,

            required_skills=required_skills,

            matched_job_skills=matched_job_skills,

            missing_job_skills=missing_job_skills,

            resume_id=resume_id,

            job_id=job_id
        )


    except Exception as e:

        return f"""
        <h2>Resume analysis failed ❌</h2>

        <p>{e}</p>

        <br>

        <a href="/">
            ← Try Again
        </a>
        """


if __name__ == "__main__":
    app.run(
        debug=True
    )