
import streamlit as st

from learning_plan import create_learning_plan

from quiz_manager import (
    generate_quiz,
    evaluate_quiz,
    get_recommendation,
    identify_weak_topics
)

from database import (
    initialize_db,
    save_learner,
    get_learner,
    save_study_plan,
    get_latest_study_plan,
    clear_study_plans,
    save_quiz_attempt,
    get_quiz_history,
    get_dashboard_stats
)


# ==================================
# PAGE CONFIGURATION
# ==================================

st.set_page_config(
    page_title="AI Personalized Learning Coach",
    page_icon="🎓",
    layout="wide"
)


# ==================================
# INITIALIZE DATABASE
# ==================================

initialize_db()


# ==================================
# LOAD SAVED DATA
# ==================================

if "learner" not in st.session_state:
    st.session_state.learner = get_learner()

if "study_plan" not in st.session_state:
    st.session_state.study_plan = get_latest_study_plan()

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

if "active_quiz_topic" not in st.session_state:
    st.session_state.active_quiz_topic = None


# ==================================
# SIDEBAR NAVIGATION
# ==================================

st.sidebar.title("🎓 AI Learning Coach")

st.sidebar.write(
    "Your personal AI-powered learning assistant."
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Learner Setup",
        "Study Plan",
        "Practice Quiz",
        "Progress Dashboard"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Learn smarter with personalized AI study plans and practice."
)


# ==================================
# HOME PAGE
# ==================================

if page == "Home":

    st.title("🎓 AI Personalized Learning Coach")

    st.subheader(
        "Your Personal AI-Powered Learning Assistant"
    )

    st.write(
        """
        Welcome! This application helps students learn according
        to their goals, current knowledge, and available study time.

        Our AI learning coach creates personalized study plans,
        generates practice quizzes, evaluates performance,
        and recommends what to learn next.
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📚 Personalized Study Plans")

    with col2:
        st.info("📝 AI Generated Quizzes")

    with col3:
        st.info("📊 Learning Progress")

    st.header("How It Works")

    steps = [
        "Enter your learning details.",
        "Generate a personalized AI study plan.",
        "Choose a topic and take an AI quiz.",
        "Receive answers and explanations.",
        "Identify weak topics and improve.",
        "Track your learning progress."
    ]

    for i, step in enumerate(steps, start=1):
        st.write(f"**{i}.** {step}")

    st.divider()

    if st.session_state.learner:

        st.success(
            f"Welcome back! Your subject is "
            f"{st.session_state.learner['subject']}."
        )

    else:

        st.warning(
            "Start by completing your Learner Setup."
        )


# ==================================
# LEARNER SETUP PAGE
# ==================================

elif page == "Learner Setup":

    st.title("👩‍🎓 Learner Setup")

    st.write(
        "Enter your learning preferences to create "
        "a personalized study plan."
    )

    existing = st.session_state.learner or {}

    level_options = [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    current_level = existing.get(
        "level",
        "Beginner"
    )

    if current_level not in level_options:
        current_level = "Beginner"

    with st.form("learner_setup_form"):

        subject = st.text_input(
            "Subject",
            value=existing.get("subject", ""),
            placeholder="Example: Python Programming"
        )

        goal = st.text_area(
            "Learning Goal",
            value=existing.get("goal", ""),
            placeholder="Example: Learn Python fundamentals"
        )

        level = st.selectbox(
            "Current Knowledge Level",
            level_options,
            index=level_options.index(current_level)
        )

        duration = st.number_input(
            "Target Duration (Days)",
            min_value=1,
            max_value=365,
            value=int(existing.get("duration", 7))
        )

        daily_time = st.number_input(
            "Daily Study Time (Minutes)",
            min_value=5,
            max_value=600,
            value=int(existing.get("daily_time", 45))
        )

        submitted = st.form_submit_button(
            "💾 Save Learning Details"
        )

        if submitted:

            if not subject.strip() or not goal.strip():

                st.error(
                    "Please enter both subject and learning goal."
                )

            else:

                new_learner = {
                    "subject": subject.strip(),
                    "goal": goal.strip(),
                    "level": level,
                    "duration": int(duration),
                    "daily_time": int(daily_time)
                }

                if new_learner != st.session_state.learner:

                    st.session_state.study_plan = None
                    st.session_state.current_quiz = None
                    st.session_state.quiz_result = None
                    st.session_state.selected_topic = None
                    st.session_state.active_quiz_topic = None

                    clear_study_plans()

                st.session_state.learner = new_learner

                save_learner(new_learner)

                st.success(
                    "Your learning details have been saved successfully!"
                )

    if st.session_state.learner:

        st.subheader("Your Learning Profile")

        learner = st.session_state.learner

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Subject:**", learner["subject"])
            st.write("**Goal:**", learner["goal"])
            st.write("**Level:**", learner["level"])

        with col2:

            st.write(
                "**Duration:**",
                learner["duration"],
                "days"
            )

            st.write(
                "**Daily Study Time:**",
                learner["daily_time"],
                "minutes"
            )


# ==================================
# STUDY PLAN PAGE
# ==================================

elif page == "Study Plan":

    st.title("📚 Personalized AI Study Plan")

    learner = st.session_state.learner

    if not learner:

        st.warning(
            "Please complete Learner Setup before generating a plan."
        )

    else:

        st.subheader("Your Learning Details")

        st.write("**Subject:**", learner["subject"])
        st.write("**Goal:**", learner["goal"])
        st.write("**Level:**", learner["level"])

        st.write(
            "**Duration:**",
            learner["duration"],
            "days"
        )

        st.write(
            "**Daily Study Time:**",
            learner["daily_time"],
            "minutes"
        )

        st.divider()

        if st.button(
            "✨ Generate / Regenerate AI Study Plan",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Gemini AI is creating your personalized study plan..."
                ):

                    plan = create_learning_plan(
                        subject=learner["subject"],
                        goal=learner["goal"],
                        level=learner["level"],
                        duration=learner["duration"],
                        daily_time=learner["daily_time"]
                    )

                    st.session_state.study_plan = plan

                    save_study_plan(plan)

                    # Reset quiz when a new plan is generated
                    st.session_state.current_quiz = None
                    st.session_state.quiz_result = None
                    st.session_state.selected_topic = None
                    st.session_state.active_quiz_topic = None

                st.success(
                    "Your personalized study plan is ready and saved!"
                )

            except Exception as error:

                st.error(
                    "Unable to generate your study plan."
                )

                st.warning(str(error))

        plan = st.session_state.study_plan

        if plan:

            st.divider()

            st.header("Your Day-wise Learning Plan")

            for item in plan["days"]:

                with st.expander(
                    f"Day {item['day']}: {item['topic']}"
                ):

                    st.write("### Learning Objective")

                    st.write(item["objective"])

                    st.write(
                        f"**Estimated Time:** "
                        f"{item['duration_minutes']} minutes"
                    )

                    st.write("### Practice Activities")

                    for activity in item["activities"]:

                        st.write(f"✅ {activity}")


# ==================================
# PRACTICE QUIZ PAGE
# ==================================

elif page == "Practice Quiz":

    st.title("📝 AI Practice Quiz")

    learner = st.session_state.learner

    plan = st.session_state.study_plan

    if not learner:

        st.warning(
            "Please complete Learner Setup first."
        )

    elif not plan:

        st.warning(
            "Please generate your study plan first."
        )

    else:

        st.write(
            "Choose a topic from your personalized study plan."
        )

        topics = [
            item["topic"] for item in plan["days"]
        ]

        selected_topic = st.selectbox(
            "Choose a topic",
            topics,
            key="quiz_topic_selector"
        )

        # Reset previous quiz if topic changes
        if selected_topic != st.session_state.active_quiz_topic:

            st.session_state.current_quiz = None
            st.session_state.quiz_result = None
            st.session_state.active_quiz_topic = selected_topic

        st.divider()

        # Generate quiz button
        if st.button(
            "✨ Generate AI Quiz",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Gemini AI is preparing five questions..."
                ):

                    questions = generate_quiz(
                        subject=learner["subject"],
                        topic=selected_topic,
                        level=learner["level"]
                    )

                    st.session_state.current_quiz = questions
                    st.session_state.quiz_result = None
                    st.session_state.selected_topic = selected_topic

                st.success(
                    "Your five-question AI quiz is ready!"
                )

            except Exception as error:

                st.error(
                    "Unable to generate the quiz."
                )

                st.warning(str(error))

        questions = st.session_state.current_quiz

        # Display quiz questions
        if questions:

            st.divider()

            st.subheader(
                f"Quiz Topic: {st.session_state.selected_topic}"
            )

            st.write(
                "Answer all five questions and submit your answers."
            )

            if st.session_state.quiz_result is None:

                answers = {}

                with st.form("quiz_answer_form"):

                    for index, question in enumerate(questions):

                        st.markdown(
                            f"**Question {index + 1}: "
                            f"{question['question']}**"
                        )

                        options = question["options"]

                        selected_answer = st.radio(
                            "Choose your answer:",
                            options=["A", "B", "C", "D"],
                            format_func=lambda option, opts=options:
                                f"{option}. {opts[option]}",
                            index=None,
                            key=f"quiz_question_{index}"
                        )

                        answers[str(index)] = selected_answer

                        st.divider()

                    submitted = st.form_submit_button(
                        "📤 Submit Quiz",
                        use_container_width=True
                    )

                if submitted:

                    if any(
                        answer is None
                        for answer in answers.values()
                    ):

                        st.warning(
                            "Please answer all five questions before submitting."
                        )

                    else:

                        try:

                            result = evaluate_quiz(
                                questions,
                                answers
                            )

                            save_quiz_attempt(
                                subject=learner["subject"],
                                topic=selected_topic,
                                result=result,
                                answers=answers
                            )

                            st.session_state.quiz_result = result

                            st.success(
                                "Your quiz result has been saved successfully!"
                            )

                            st.rerun()

                        except Exception as error:

                            st.error(
                                "Unable to submit your quiz."
                            )

                            st.warning(str(error))

            # Display result after submission
            if st.session_state.quiz_result:

                result = st.session_state.quiz_result

                st.divider()

                st.header("📊 Your Quiz Result")

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Your Score",
                        f"{result['score']} / {result['total']}"
                    )

                with col2:

                    st.metric(
                        "Percentage",
                        f"{result['percentage']}%"
                    )

                st.progress(
                    result["percentage"] / 100
                )

                recommendation = get_recommendation(
                    result["percentage"],
                    selected_topic
                )

                st.info(recommendation)

                st.subheader("Answer Review")

                for index, item in enumerate(result["review"]):

                    if item["is_correct"]:

                        st.success(
                            f"Question {index + 1}: Correct!"
                        )

                    else:

                        st.error(
                            f"Question {index + 1}: Incorrect"
                        )

                    st.write(
                        "**Your answer:**",
                        item["selected_answer"]
                    )

                    st.write(
                        "**Correct answer:**",
                        item["correct_answer"]
                    )

                    st.write(
                        "**Explanation:**",
                        item["explanation"]
                    )

                    st.divider()

                if st.button(
                    "🔄 Generate Another Quiz",
                    use_container_width=True
                ):

                    st.session_state.current_quiz = None
                    st.session_state.quiz_result = None

                    st.rerun()


# ==================================
# PROGRESS DASHBOARD
# ==================================

elif page == "Progress Dashboard":

    st.title("📊 Learning Progress Dashboard")

    learner = st.session_state.learner

    plan = st.session_state.study_plan

    if not learner:

        st.warning(
            "Complete Learner Setup to view your dashboard."
        )

    else:

        st.subheader("Learner Information")

        st.write("**Subject:**", learner["subject"])
        st.write("**Learning Goal:**", learner["goal"])
        st.write("**Current Level:**", learner["level"])

        st.divider()

        if plan:

            total_topics = len(plan["days"])

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Total Topics",
                    total_topics
                )

            with col2:

                st.metric(
                    "Study Plan Duration",
                    learner["duration"],
                    "days"
                )

            st.subheader("Topics to Learn")

            for item in plan["days"]:

                st.write(
                    f"📘 Day {item['day']}: {item['topic']}"
                )

        else:

            st.info(
                "Generate a study plan to see your learning topics."
            )

        st.divider()

        st.subheader("Quiz Performance")

        stats = get_dashboard_stats()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Quiz Attempts",
                stats["total_attempts"]
            )

        with col2:

            st.metric(
                "Average Score",
                f"{stats['average_score']}%"
            )

        with col3:

            st.metric(
                "Best Score",
                f"{stats['best_score']}%"
            )

        st.divider()

        st.subheader("Quiz History")

        history = get_quiz_history()

        if history:

            display_history = [

                {
                    "Subject": item["subject"],
                    "Topic": item["topic"],
                    "Score": f"{item['score']}/{item['total']}",
                    "Percentage": f"{item['percentage']}%",
                    "Date": item["created_at"]
                }

                for item in history

            ]

            st.dataframe(
                display_history,
                use_container_width=True
            )

            st.divider()

            st.subheader("Topics That Need Improvement")

            weak_topics = identify_weak_topics(history)

            if weak_topics:

                for item in weak_topics:

                    st.warning(
                        f"**{item['topic']}** — "
                        f"Average score: {item['average_score']}%"
                    )

                    st.write(
                        item["recommendation"]
                    )

            else:

                st.success(
                    "Great work! No weak topics identified "
                    "from your quiz history."
                )

        else:

            st.info(
                "No quiz attempts yet. Start practicing to see your scores."
            )


# ==================================
# FOOTER
# ==================================

st.divider()

st.caption(
    "AI Personalized Learning Coach | "
    "Powered by Python, Streamlit, SQLite and Gemini AI"
)

