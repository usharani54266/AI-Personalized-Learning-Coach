

from ai_service import generate_json


# ----------------------------------
# GENERATE AI QUIZ
# ----------------------------------

def generate_quiz(subject, topic, level):

    prompt = f"""
    You are an expert educational quiz creator.

    Create exactly 5 multiple-choice questions.

    Subject: {subject}
    Topic: {topic}
    Student Level: {level}

    Requirements:
    1. Create exactly 5 questions.
    2. Each question must have 4 options.
    3. Options must use labels A, B, C, D.
    4. Only one option must be correct.
    5. Questions must match the student's level.
    6. Provide a clear explanation for every answer.

    Return valid JSON in this exact structure:

    {{
        "questions": [
            {{
                "question": "Question text",
                "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
                }},
                "correct_answer": "A",
                "explanation": "Explanation of the correct answer"
            }}
        ]
    }}

    Return JSON only.
    """

    data = generate_json(prompt)

    if not isinstance(data, dict):
        raise ValueError("Invalid quiz response from Gemini.")

    questions = data.get("questions")

    if not isinstance(questions, list) or len(questions) != 5:
        raise ValueError("Gemini must generate exactly 5 questions.")

    for question in questions:

        if not isinstance(question, dict):
            raise ValueError("Invalid question format.")

        required_fields = [
            "question",
            "options",
            "correct_answer",
            "explanation"
        ]

        for field in required_fields:
            if field not in question:
                raise ValueError(
                    f"Missing quiz field: {field}"
                )

        options = question["options"]

        if not isinstance(options, dict):
            raise ValueError("Question options must be a dictionary.")

        if set(options.keys()) != {"A", "B", "C", "D"}:
            raise ValueError(
                "Every question must have A, B, C and D options."
            )

        if question["correct_answer"] not in ["A", "B", "C", "D"]:
            raise ValueError("Invalid correct answer.")

        if not isinstance(question["question"], str):
            raise ValueError("Invalid question text.")

        if not isinstance(question["explanation"], str):
            raise ValueError("Invalid answer explanation.")

    return questions


# ----------------------------------
# EVALUATE QUIZ ANSWERS
# ----------------------------------

def evaluate_quiz(questions, answers):

    score = 0
    review = []

    for index, question in enumerate(questions):

        selected_answer = answers.get(str(index))

        correct_answer = question["correct_answer"]

        is_correct = (
            selected_answer == correct_answer
        )

        if is_correct:
            score += 1

        review.append({

            "question": question["question"],

            "selected_answer": (
                selected_answer if selected_answer else "Not answered"
            ),

            "correct_answer": correct_answer,

            "is_correct": is_correct,

            "explanation": question["explanation"]

        })

    total = len(questions)

    percentage = (
        (score / total) * 100
        if total > 0 else 0
    )

    return {

        "score": score,

        "total": total,

        "percentage": round(percentage, 2),

        "review": review

    }


# ----------------------------------
# PERSONALIZED RECOMMENDATION
# ----------------------------------

def get_recommendation(percentage, topic):

    if percentage >= 80:

        return (
            f"Excellent performance! You understand {topic} well. "
            "You can move to the next topic."
        )

    elif percentage >= 60:

        return (
            f"Good effort! Revise important concepts in {topic} "
            "and practise a few more questions."
        )

    else:

        return (
            f"You need more practice in {topic}. "
            "Review the topic carefully and try the quiz again."
        )


# ----------------------------------
# IDENTIFY WEAK TOPICS
# ----------------------------------

def identify_weak_topics(quiz_history):

    topic_scores = {}

    for attempt in quiz_history:

        topic = attempt["topic"]

        percentage = float(attempt["percentage"])

        if topic not in topic_scores:
            topic_scores[topic] = []

        topic_scores[topic].append(percentage)

    weak_topics = []

    for topic, scores in topic_scores.items():

        average = sum(scores) / len(scores)

        if average < 60:

            weak_topics.append({

                "topic": topic,

                "average_score": round(average, 2),

                "recommendation": (
                    f"Revise {topic} and practise more questions."
                )

            })

    return weak_topics
