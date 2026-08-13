CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS resume_skills (
    resume_id INTEGER,
    skill_id INTEGER,
    FOREIGN KEY (resume_id) REFERENCES resumes(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id),
    PRIMARY KEY (resume_id, skill_id)
);


CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER,
    skill_id INTEGER,
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id),
    PRIMARY KEY (job_id, skill_id)
);
INSERT OR IGNORE INTO skills (name) VALUES ('Python');
INSERT OR IGNORE INTO skills (name) VALUES ('Java');
INSERT OR IGNORE INTO skills (name) VALUES ('C++');
INSERT OR IGNORE INTO skills (name) VALUES ('SQL');
INSERT OR IGNORE INTO skills (name) VALUES ('HTML');
INSERT OR IGNORE INTO skills (name) VALUES ('MATLAB');
INSERT OR IGNORE INTO skills (name) VALUES ('Machine Learning');
INSERT OR IGNORE INTO skills (name) VALUES ('Deep Learning');
INSERT OR IGNORE INTO skills (name) VALUES ('Data Structures and Algorithms');
INSERT OR IGNORE INTO skills (name) VALUES ('Database Management');