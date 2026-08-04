-- queries.sql
-- Analytical queries answering real reporting questions.
-- Run with: sqlite3 db/students.db < sql/queries.sql
-- (load_db.py builds db/students.db first)

-- 1. Overall pass rate
SELECT
    ROUND(100.0 * SUM(passed) / COUNT(*), 2) AS pass_rate_pct,
    COUNT(*) AS total_students
FROM students;

-- 2. Average final grade by parental education level
SELECT
    parent_education,
    COUNT(*) AS n_students,
    ROUND(AVG(final_grade_pct), 2) AS avg_grade,
    ROUND(100.0 * SUM(passed) / COUNT(*), 2) AS pass_rate_pct
FROM students
GROUP BY parent_education
ORDER BY avg_grade DESC;

-- 3. Impact of test preparation and tutoring (combined effect)
SELECT
    test_preparation,
    tutoring,
    COUNT(*) AS n_students,
    ROUND(AVG(final_grade_pct), 2) AS avg_grade
FROM students
GROUP BY test_preparation, tutoring
ORDER BY avg_grade DESC;

-- 4. Attendance buckets vs performance
SELECT
    CASE
        WHEN attendance_rate >= 0.95 THEN '95-100%'
        WHEN attendance_rate >= 0.85 THEN '85-94%'
        WHEN attendance_rate >= 0.75 THEN '75-84%'
        ELSE 'Below 75%'
    END AS attendance_bucket,
    COUNT(*) AS n_students,
    ROUND(AVG(final_grade_pct), 2) AS avg_grade
FROM students
GROUP BY attendance_bucket
ORDER BY avg_grade DESC;

-- 5. Ethnicity group performance breakdown by subject
SELECT
    ethnicity_group,
    ROUND(AVG(math_score), 2) AS avg_math,
    ROUND(AVG(reading_score), 2) AS avg_reading,
    ROUND(AVG(writing_score), 2) AS avg_writing
FROM students
GROUP BY ethnicity_group
ORDER BY ethnicity_group;

-- 6. Top and bottom decile students (window functions)
SELECT student_id, final_grade_pct, decile
FROM (
    SELECT student_id, final_grade_pct,
           NTILE(10) OVER (ORDER BY final_grade_pct DESC) AS decile
    FROM students
)
WHERE decile IN (1, 10)
ORDER BY decile, final_grade_pct DESC;

-- 7. Free/Reduced lunch as an equity indicator
SELECT
    lunch_type,
    COUNT(*) AS n_students,
    ROUND(AVG(final_grade_pct), 2) AS avg_grade,
    ROUND(100.0 * SUM(passed) / COUNT(*), 2) AS pass_rate_pct
FROM students
GROUP BY lunch_type;
