-- schema.sql
-- Schema for the student performance analytics database (SQLite/PostgreSQL compatible)

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id          INTEGER PRIMARY KEY,
    gender               TEXT NOT NULL,
    ethnicity_group       TEXT NOT NULL,
    parent_education      TEXT NOT NULL,
    lunch_type            TEXT NOT NULL,
    test_preparation      TEXT NOT NULL,
    study_hours_week      REAL NOT NULL,
    attendance_rate       REAL NOT NULL,
    tutoring              TEXT NOT NULL,
    extracurricular       TEXT NOT NULL,
    math_score            REAL NOT NULL,
    reading_score         REAL NOT NULL,
    writing_score         REAL NOT NULL,
    final_grade_pct       REAL NOT NULL,
    passed                INTEGER NOT NULL
);

CREATE INDEX idx_students_ethnicity ON students(ethnicity_group);
CREATE INDEX idx_students_parent_ed ON students(parent_education);
CREATE INDEX idx_students_passed ON students(passed);
