import sqlite3

DATABASE = "database/skills.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def add_skill(name):
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO skills (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    conn.close()


def get_skills():
    conn = get_connection()
    skills = conn.execute("SELECT * FROM skills").fetchall()
    conn.close()
    return skills


def save_resume(filename):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO resumes (filename) VALUES (?)",
        (filename,)
    )
    conn.commit()
    resume_id = cursor.lastrowid
    conn.close()
    return resume_id


def save_resume_skills(resume_id, skill_names):
    conn = get_connection()

    for skill_name in skill_names:
        row = conn.execute(
            "SELECT id FROM skills WHERE name = ?",
            (skill_name,)
        ).fetchone()

        if row:
            conn.execute(
                "INSERT OR IGNORE INTO resume_skills (resume_id, skill_id) VALUES (?, ?)",
                (resume_id, row["id"])
            )

    conn.commit()
    conn.close()


def save_job(title, description):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO jobs (title, description) VALUES (?, ?)",
        (title, description)
    )
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return job_id


def save_job_skills(job_id, skill_names):
    conn = get_connection()

    for skill_name in skill_names:
        row = conn.execute(
            "SELECT id FROM skills WHERE name = ?",
            (skill_name,)
        ).fetchone()

        if row:
            conn.execute(
                "INSERT OR IGNORE INTO job_skills (job_id, skill_id) VALUES (?, ?)",
                (job_id, row["id"])
            )

    conn.commit()
    conn.close()