
# AI Personalized Learning Coach 🎓

An AI-powered personalized learning application built using Python, Streamlit, Gemini API, and SQLite.

The application helps learners create personalized study plans, practice topic-based quizzes, understand their mistakes, and track their learning progress.

## ✨ Features

- **Learner Profile:** Enter learning preferences, subject, skill level, and daily study time.
- **AI Study Plan:** Generate a day-wise personalized study plan using Google Gemini.
- **AI Quiz Generation:** Generate 5 multiple-choice questions for selected topics.
- **Automatic Evaluation:** Calculate quiz scores using Python.
- **Instant Feedback:** Display correct answers and explanations.
- **Weak Topic Identification:** Identify topics that need more practice.
- **Progress Dashboard:** View quiz attempts, average scores, and learning progress.
- **SQLite Database:** Save learner details, study plans, and quiz history.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- SQLite
- python-dotenv
- Git and GitHub

## 📁 Project Structure

```text
AI-Personalized-Learning-Coach/
│
├── app.py
├── ai_service.py
├── learning_plan.py
├── quiz_manager.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/usharani54266/AI-Personalized-Learning-Coach.git
```

### 2. Open the project folder

```bash
cd AI-Personalized-Learning-Coach
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment (Windows)

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Create a `.env` file in the project folder and add:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Replace `your_gemini_api_key` with your own Gemini API key.

**Important:** Never upload your `.env` file or API key to GitHub.

### 7. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 🚀 How to Use

1. Open the application.
2. Enter your learner profile details.
3. Generate a personalized study plan.
4. Select a topic for quiz practice.
5. Generate an AI-powered quiz.
6. Submit your answers.
7. Review your score and explanations.
8. Check your progress dashboard.

## 🔐 Security

- API keys are stored in a local `.env` file.
- `.env` is excluded from Git using `.gitignore`.
- Learner data and quiz history are stored locally in SQLite.

## 👩‍💻 Developer

**Nayaki Usha Rani**

B.Tech Computer Science and Engineering

GitHub: https://github.com/usharani54266

---

*Developed as an AI Personalized Learning Coach project.*
