

import sqlite3
import json
from datetime import datetime

DB_NAME = "learning_coach.db"


# ----------------------------------
# DATABASE CONNECTION
# ----------------------------------

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# ----------------------------------
# INITIALIZE DATABASE TABLES
# ----------------------------------

def initialize_db():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learner_profiles (
            id INTEGER PRIMARY KEY,
            subject TEXT NOT NULL,
            goal TEXT NOT NULL,
            level TEXT NOT NULL,
            duration INTEGER NOT NULL,
            daily_time INTEGER NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            answers_json TEXT NOT NULL,
            review_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ----------------------------------
# SAVE LEARNER PROFILE
# ----------------------------------

def save_learner(learner):

    connection = get_connection()

    connection.execute("""
        INSERT INTO learner_profiles
        (id, subject, goal, level, duration, daily_time, updated_at)
        VALUES (1, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(id) DO UPDATE SET
            subject = excluded.subject,
            goal = excluded.goal,
            level = excluded.level,
            duration = excluded.duration,
            daily_time = excluded.daily_time,
            updated_at = excluded.updated_at
    """, (
        learner["subject"],
        learner["goal"],
        learner["level"],
        int(learner["duration"]),
        int(learner["daily_time"]),
        datetime.now().isoformat(timespec="seconds")
    ))

    connection.commit()
    connection.close()


# ----------------------------------
# GET SAVED LEARNER PROFILE
# ----------------------------------

def get_learner():

    connection = get_connection()

    row = connection.execute("""
        SELECT * FROM learner_profiles
        WHERE id = 1
    """).fetchone()

    connection.close()

    return dict(row) if row else None


# ----------------------------------
# SAVE STUDY PLAN
# ----------------------------------

def save_study_plan(plan):

    connection = get_connection()

    connection.execute("""
        INSERT INTO study_plans
        (plan_json, created_at)
        VALUES (?, ?)
    """, (
        json.dumps(plan),
        datetime.now().isoformat(timespec="seconds")
    ))

    connection.commit()
    connection.close()


# ----------------------------------
# GET LATEST STUDY PLAN
# ----------------------------------

def get_latest_study_plan():

    connection = get_connection()

    row = connection.execute("""
        SELECT plan_json
        FROM study_plans
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

    connection.close()

    return json.loads(row["plan_json"]) if row else None


# ----------------------------------
# CLEAR OLD STUDY PLANS
# ----------------------------------

def clear_study_plans():

    connection = get_connection()

    connection.execute("""
        DELETE FROM study_plans
    """)

    connection.commit()
    connection.close()


# ----------------------------------
# SAVE QUIZ ATTEMPT
# ----------------------------------

def save_quiz_attempt(subject, topic, result, answers):

    connection = get_connection()

    connection.execute("""
        INSERT INTO quiz_attempts
        (
            subject,
            topic,
            score,
            total,
            percentage,
            answers_json,
            review_json,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        subject,
        topic,
        result["score"],
        result["total"],
        result["percentage"],
        json.dumps(answers),
        json.dumps(result["review"]),
        datetime.now().isoformat(timespec="seconds")
    ))

    connection.commit()
    connection.close()


# ----------------------------------
# GET QUIZ HISTORY
# ----------------------------------

def get_quiz_history():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM quiz_attempts
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    history = []

    for row in rows:

        attempt = dict(row)

        attempt["answers"] = json.loads(
            attempt.pop("answers_json")
        )

        attempt["review"] = json.loads(
            attempt.pop("review_json")
        )

        history.append(attempt)

    return history


# ----------------------------------
# DASHBOARD STATISTICS
# ----------------------------------

def get_dashboard_stats():

    connection = get_connection()

    stats = connection.execute("""
        SELECT
            COUNT(*) AS total_attempts,
            COALESCE(AVG(percentage), 0) AS average_score,
            COALESCE(MAX(percentage), 0) AS best_score
        FROM quiz_attempts
    """).fetchone()

    connection.close()

    return {
        "total_attempts": stats["total_attempts"],
        "average_score": round(stats["average_score"], 2),
        "best_score": round(stats["best_score"], 2)
    }
