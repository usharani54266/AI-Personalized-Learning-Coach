
from ai_service import generate_json


def create_learning_plan(
    subject,
    goal,
    level,
    duration,
    daily_time
):
    prompt = f"""
    You are an expert personal learning coach.

    Create a personalized study plan using these details:

    Subject: {subject}
    Learning Goal: {goal}
    Current Level: {level}
    Duration: {duration} days
    Daily Study Time: {daily_time} minutes

    Requirements:
    1. Create exactly {duration} days.
    2. Follow the learner's current level.
    3. Keep daily study time within {daily_time} minutes.
    4. Include practical learning activities.
    5. Make topics progressive and beginner-friendly.

    Return valid JSON in this structure:

    {{
        "subject": "{subject}",
        "goal": "{goal}",
        "days": [
            {{
                "day": 1,
                "topic": "Topic name",
                "objective": "Learning objective",
                "duration_minutes": 45,
                "activities": [
                    "Read the topic",
                    "Practice examples"
                ]
            }}
        ]
    }}
    """

    plan = generate_json(prompt)

    # Validate the AI response
    if not isinstance(plan, dict):
        raise ValueError("Invalid study plan format.")

    days = plan.get("days")

    if not isinstance(days, list) or len(days) != duration:
        raise ValueError("Study plan has an incorrect number of days.")

    for item in days:
        required = [
            "day",
            "topic",
            "objective",
            "duration_minutes",
            "activities"
        ]

        if not isinstance(item, dict):
            raise ValueError("Invalid day format.")

        if not all(key in item for key in required):
            raise ValueError("Study plan is missing required fields.")

        if not isinstance(item["activities"], list):
            raise ValueError("Invalid activities format.")

        if not isinstance(item["duration_minutes"], int):
            raise ValueError("Invalid duration format.")

        if not 1 <= item["duration_minutes"] <= daily_time:
            raise ValueError("Daily study time exceeds the limit.")

    return plan
