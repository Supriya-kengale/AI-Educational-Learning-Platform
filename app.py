from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import random
import datetime
from chatbot import get_chat_response

# -------------------- CONFIG --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)

# -------------------- MODELS --------------------
class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(150), nullable=False, unique=True)
    email: str = db.Column(db.String(150), nullable=False, unique=True)
    password: str = db.Column(db.String(200), nullable=False)
    role: str = db.Column(db.String(50), default="student")
    # Add relationship to quiz results
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
    
    def __init__(self, username: str, email: str, password: str, role: str = "student"):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

# Add QuizResult model to store quiz results
class QuizResult(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject: str = db.Column(db.String(50), nullable=False)
    score: int = db.Column(db.Integer, nullable=False)
    total: int = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __init__(self, user_id: int, subject: str, score: int, total: int):
        self.user_id = user_id
        self.subject = subject
        self.score = score
        self.total = total

with app.app_context():
    db.create_all()

# -------------------- HELPERS --------------------
# Import lessons content from lesson_data.py
from lesson_data import lessons_content

def get_lessons_for_course(course):
    # Use lesson_data.py if available, otherwise fallback to hardcoded data
    if course in lessons_content:
        return lessons_content[course]
    
    # Fallback to original implementation
    lessons = {
        "cs": [
            {"id": 1, "title": "Intro to Computing"},
            {"id": 2, "title": "Programming Basics"},
            {"id": 3, "title": "Data Structures"},
            {"id": 4, "title": "Sorting Algorithms"},
            {"id": 5, "title": "Search Algorithms"},
            {"id": 6, "title": "Graph Algorithms"}
        ],
        "ai": [
            {"id": 1, "title": "Machine Learning Intro"},
            {"id": 2, "title": "Neural Networks"},
            {"id": 3, "title": "Natural Language Processing"},
            {"id": 4, "title": "Computer Vision"},
            {"id": 5, "title": "Reinforcement Learning"},
            {"id": 6, "title": "Coming Soon"}
        ],
        # New CSE course
        "cse": [
            {"id": 1, "title": "Computer Architecture"},
            {"id": 2, "title": "Operating Systems"},
            {"id": 3, "title": "Database Systems"},
            {"id": 4, "title": "Computer Networks"},
            {"id": 5, "title": "Software Engineering"},
            {"id": 6, "title": "Cybersecurity"}
        ],
        # New AI/ML course
        "aiml": [
            {"id": 1, "title": "Supervised Learning"},
            {"id": 2, "title": "Unsupervised Learning"},
            {"id": 3, "title": "Deep Learning Fundamentals"},
            {"id": 4, "title": "Natural Language Processing"},
            {"id": 5, "title": "Computer Vision"},
            {"id": 6, "title": "Reinforcement Learning"}
        ]
    }
    return lessons.get(course, [{"id": i+1, "title": f"Lesson {i+1}"} for i in range(6)])

def get_course_content():
    return {
        "cs": {
            "title": "Computer Science - Foundations",
            "reading_text": "Computer Science covers programming, algorithms, data structures, and problem-solving.",
            "reading_pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/2SpuBqvNjHI",
            "model_external_url": "https://kagol.github.io/hanoi/"
        },
        "ai": {
            "title": "Artificial Intelligence - Machines that Think",
            "reading_text": "AI focuses on creating systems that can perform tasks requiring human intelligence.",
            "reading_pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/JMUxmLyrhSk",
            "model_external_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        # New CSE course
        "cse": {
            "title": "Computer Science & Engineering - Comprehensive Systems",
            "reading_text": "CSE combines computer science with engineering principles to design and build computer systems.",
            "reading_pdf": "ai_computer_vision.pdf",
            "video": "https://www.youtube.com/embed/9_39Va4c040",
            "model_external_url": "https://threejs.org/examples/#webgl_physics_cloth"
        },
        # New AI/ML course
        "aiml": {
            "title": "AI & Machine Learning - Intelligent Systems",
            "reading_text": "AI/ML focuses on creating algorithms that enable machines to learn from data and make intelligent decisions.",
            "reading_pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/qv6UVOQ0F44",
            "model_external_url": "https://threejs.org/examples/#webgl_neural_networks"
        }
    }

# Add helper function to get user progress
def get_user_progress(user_id):
    # Get quiz results for the user
    quiz_results = QuizResult.query.filter_by(user_id=user_id).all()
    
    # Initialize progress data
    progress_data = {
        "cs": {"completed": 0, "total": 6},
        "ai": {"completed": 0, "total": 6},
        "cse": {"completed": 0, "total": 6},
        "aiml": {"completed": 0, "total": 6}
    }
    
    # Count completed lessons based on quiz results
    for result in quiz_results:
        if result.subject in progress_data:
            # Consider a course completed if quiz score is >= 60%
            if (result.score / result.total) >= 0.6:
                progress_data[result.subject]["completed"] = progress_data[result.subject]["total"]
            else:
                # Partial progress based on score
                progress_data[result.subject]["completed"] = int((result.score / result.total) * progress_data[result.subject]["total"])
    
    return progress_data

# Import chatbot functionality
# Using the chatbot.py implementation instead of the simple echo function

# -------------------- ROUTES --------------------
@app.route("/")
def index(): return render_template("index.html")

@app.route("/about")
def about(): return render_template("about.html")

@app.route("/courses")
def courses():
    print(f"DEBUG: Courses access - Session: {dict(session)}")
    if "user_id" not in session:
        print("DEBUG: No user_id in session, redirecting to login")
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))
    print("DEBUG: User authorized to access courses")
    return render_template("courses.html")

# -------- AUTH --------
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username, email = request.form.get("username","").strip(), request.form.get("email","").strip()
        password = request.form.get("password","")
        # Force all new users to be students, ignore role selection
        role = "student"

        if not username or not email or not password:
            flash("All fields required.", "warning")
            return redirect(url_for("signup"))

        if User.query.filter(db.or_(User.username==username, User.email==email)).first():
            flash("User exists. Please login.", "warning")
            return redirect(url_for("login"))

        hashed = generate_password_hash(password, "pbkdf2:sha256")
        user = User(username=username, email=email, password=hashed, role=role)
        db.session.add(user); db.session.commit()

        # Redirect to login page instead of auto-logging in
        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email, password = request.form.get("email","").strip(), request.form.get("password","")
        user = User.query.filter_by(email=email).first()

        print(f"DEBUG: Login attempt for email: {email}")
        if user:
            print(f"DEBUG: User found: {user.username}, role: {user.role}")
            if check_password_hash(user.password, password):
                print(f"DEBUG: Password correct for user: {user.username}")
                # Set session data
                session["user_id"] = user.id
                session["role"] = user.role
                session["username"] = user.username
                print(f"DEBUG: Session set - user_id: {session.get('user_id')}, role: {session.get('role')}, username: {session.get('username')}")
                print(f"DEBUG: Session keys: {list(session.keys())}")
                
                # Check user role and redirect accordingly
                if user.role == "admin":
                    print(f"DEBUG: Redirecting admin user to admin dashboard")
                    return redirect(url_for("admin_dashboard"))
                else:
                    print(f"DEBUG: Redirecting student user to dashboard")
                    return redirect(url_for("dashboard"))
            else:
                print(f"DEBUG: Password incorrect for user: {user.username}")
        else:
            print(f"DEBUG: No user found with email: {email}")

        flash("Invalid credentials.", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/login_new")
def login_new():
    return render_template("login_new.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

# -------- Lessons --------
@app.route("/course/<course>")
def course_lessons(course):
    if "user_id" not in session: return redirect(url_for("login"))
    return render_template("course_lessons.html", course=course, lessons=get_lessons_for_course(course))

@app.route("/lesson/<course>/<int:lesson_id>")
def learning_hub(course, lesson_id):
    if "user_id" not in session: return redirect(url_for("login"))

    # Get course content (general info)
    content = get_course_content().get(course)
    
    # Get specific lesson data with YouTube links
    lessons = get_lessons_for_course(course)
    
    # Find the specific lesson
    selected = None
    for lesson in lessons:
        if lesson["id"] == lesson_id:
            selected = lesson
            break

    if not content or not selected:
        flash("Lesson not found.", "danger")
        return redirect(url_for("course_lessons", course=course))

    # Override content with lesson-specific data if available
    if "pdf" in selected:
        content["reading_pdf"] = selected["pdf"]
    if "video" in selected:
        content["video"] = selected["video"]
    if "reading_text" in selected:
        content["reading_text"] = selected["reading_text"]
    if "model_url" in selected:
        content["model_external_url"] = selected["model_url"]

    # Debug: Print the content being passed to template
    print(f"DEBUG: Course={course}, Lesson ID={lesson_id}")
    print(f"DEBUG: Content video URL={content.get('video', 'None')}")
    print(f"DEBUG: Selected lesson={selected}")

    return render_template("learning_hub.html", course=course, lesson=selected, content=content)

# -------- Quizzes with API Fallback --------
@app.route("/quizzes")
def quizzes():
    if "user_id" not in session: return redirect(url_for("login"))
    return render_template("quizzes.html")

# Sample quiz questions (fallback if API unavailable)
QUESTIONS = {
    "cs": [
        {"question": "Which data structure uses LIFO principle?", "options": ["Queue", "Stack", "Tree", "Graph"], "answer": "Stack"},
        {"question": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Processor Unit", "Central Program Unit"], "answer": "Central Processing Unit"},
        {"question": "Which sorting algorithm has best average time complexity?", "options": ["Bubble Sort", "Insertion Sort", "Quick Sort", "Selection Sort"], "answer": "Quick Sort"},
        {"question": "In which memory do variables declared inside a function get stored?", "options": ["Heap", "Stack", "Code", "Data"], "answer": "Stack"},
        {"question": "Which of these is not a programming paradigm?", "options": ["Object-Oriented", "Functional", "Procedural", "Sequential"], "answer": "Sequential"}
    ],
    "ai": [
        {"question": "What does ML stand for in AI?", "options": ["Machine Learning", "Manual Learning", "Mechanical Learning", "Managed Learning"], "answer": "Machine Learning"},
        {"question": "Which algorithm is inspired by the human brain?", "options": ["Decision Trees", "Neural Networks", "Support Vector Machines", "K-Means Clustering"], "answer": "Neural Networks"},
        {"question": "What is the purpose of training data in ML?", "options": ["To test the model", "To improve the model", "To delete the model", "To ignore the model"], "answer": "To improve the model"},
        {"question": "Which technique helps prevent overfitting?", "options": ["Increasing training data", "Reducing features", "Regularization", "All of the above"], "answer": "All of the above"},
        {"question": "What is supervised learning?", "options": ["Learning with labeled data", "Learning without data", "Learning with rewards", "Learning by observation"], "answer": "Learning with labeled data"}
    ],
    "cse": [
        {"question": "What is the main function of an operating system?", "options": ["Manage hardware resources", "Compile programs", "Design circuits", "Create websites"], "answer": "Manage hardware resources"},
        {"question": "Which protocol is used for sending emails?", "options": ["HTTP", "FTP", "SMTP", "TCP"], "answer": "SMTP"},
        {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"], "answer": "Structured Query Language"},
        {"question": "Which of these is a cybersecurity threat?", "options": ["Firewall", "Antivirus", "Phishing", "Encryption"], "answer": "Phishing"},
        {"question": "What is virtual memory?", "options": ["Physical RAM", "Storage device", "Disk space used as RAM", "Cache memory"], "answer": "Disk space used as RAM"}
    ],
    "aiml": [
        {"question": "What is supervised learning used for?", "options": ["Classification", "Clustering", "Association", "Dimensionality Reduction"], "answer": "Classification"},
        {"question": "Which algorithm groups similar data points?", "options": ["Linear Regression", "K-Means Clustering", "Decision Trees", "Naive Bayes"], "answer": "K-Means Clustering"},
        {"question": "What is overfitting?", "options": ["Model too simple", "Model too complex", "Perfect model", "No model"], "answer": "Model too complex"},
        {"question": "Which neural network is best for image recognition?", "options": ["RNN", "CNN", "LSTM", "GRU"], "answer": "CNN"},
        {"question": "What is reinforcement learning based on?", "options": ["Labels", "Rewards", "Clusters", "Rules"], "answer": "Rewards"}
    ]
}

# Mock API function (replace with real API call)
def fetch_quiz_from_api(subject):
    # Simulate API call failure to trigger fallback
    return None

@app.route("/quiz/<subject>", methods=["GET", "POST"])
def quiz(subject):
    # Validate subject
    valid_subjects = ['cs', 'ai', 'cse', 'aiml']
    if subject not in valid_subjects:
        flash("Invalid quiz subject.", "danger")
        return redirect(url_for("quizzes"))
        
    subject_q = fetch_quiz_from_api(subject) or QUESTIONS.get(subject, [])  # API first, fallback second
    score = None
    total = len(subject_q)
    result_message = None
    user_answers = []
    
    # If no questions found, redirect with error
    if total == 0:
        flash("No questions available for this quiz.", "warning")
        return redirect(url_for("quizzes"))

    if request.method == "POST":
        score = 0
        user_answers = []
        print(f"DEBUG: Processing quiz for subject: {subject}")
        print(f"DEBUG: Form data: {dict(request.form)}")
        print(f"DEBUG: Questions count: {len(subject_q)}")
        
        # Print all questions for debugging
        for idx, q in enumerate(subject_q, 1):
            print(f"DEBUG: Question {idx} in backend: '{q['question']}'")
            print(f"DEBUG: Options {idx}: {q['options']}")
            print(f"DEBUG: Answer {idx}: '{q['answer']}'")
        
        for i, q in enumerate(subject_q, 1):
            selected = request.form.get(f"q{i}")
            # Strip whitespace from both selected answer and correct answer for comparison
            selected_stripped = selected.strip() if selected else ""
            correct_answer_stripped = q["answer"].strip()
            user_answers.append(selected or "No answer")
            print(f"DEBUG: Processing Question {i}: '{q['question']}'")
            print(f"DEBUG: Options: {q['options']}")
            print(f"DEBUG: Selected='{selected}', Correct='{q['answer']}'")
            print(f"DEBUG: Stripped comparison: '{selected_stripped}' == '{correct_answer_stripped}' -> {selected_stripped == correct_answer_stripped}")
            # Compare stripped versions to handle whitespace issues
            if selected_stripped == correct_answer_stripped:
                score += 1
                print(f"DEBUG: Score incremented, now: {score}")

        pct = (score / total) * 100 if total else 0
        if pct < 60:
            result_message = "Need to work hard! Keep studying and try again."
        elif pct < 80:
            result_message = "Good work! You're on the right track."
        else:
            result_message = "Excellent! You've mastered this subject."
            
        # Save quiz result to database
        if "user_id" in session:
            quiz_result = QuizResult(
                user_id=session["user_id"],
                subject=subject,
                score=score,
                total=total
            )
            db.session.add(quiz_result)
            db.session.commit()

    return render_template("quiz.html",
                           subject=subject,
                           questions=subject_q,
                           score=score,
                           total=total,
                           result_message=result_message,
                           user_answers=user_answers)

@app.route("/dashboard")
def dashboard():
    # Debug session information
    print(f"DEBUG: Dashboard access - Session: {dict(session)}")
    
    if "user_id" not in session:
        print("DEBUG: No user_id in session, redirecting to login")
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))
    
    # Ensure username is in session (fix for basedpyright error)
    if "username" not in session:
        user = User.query.get(session["user_id"])
        if user:
            session["username"] = user.username
            print(f"DEBUG: Username set in session: {user.username}")
        else:
            print("DEBUG: User not found in database, redirecting to login")
            flash("User not found.", "danger")
            return redirect(url_for("login"))
    
    # Get user progress
    progress_data = get_user_progress(session["user_id"])
    print(f"DEBUG: Progress data retrieved: {progress_data}")
    
    return render_template("dashboard.html", progress_data=progress_data)

@app.route("/admin_dashboard")
def admin_dashboard():
    print(f"DEBUG: Accessing admin dashboard")
    print(f"DEBUG: Session user_id: {session.get('user_id')}")
    print(f"DEBUG: Session role: {session.get('role')}")
    print(f"DEBUG: Session username: {session.get('username')}")
    
    if "user_id" not in session or session.get("role") != "admin":
        print(f"DEBUG: Access denied - user_id in session: {'user_id' in session}")
        print(f"DEBUG: Role check: {session.get('role') != 'admin'}")
        flash("Access denied.", "danger")
        return redirect(url_for("login"))
    
    # Get statistics
    total_students = User.query.filter_by(role="student").count()
    total_courses = 4  # We have 4 courses (CS, AI, CSE, AI/ML)
    
    # Get all users and convert to serializable format
    users = User.query.all()
    users_serializable = []
    for user in users:
        users_serializable.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        })
    
    # Get real-time quiz results for statistics
    all_quiz_results = QuizResult.query.all()
    total_quizzes_taken = len(all_quiz_results)
    
    # Calculate average score
    if total_quizzes_taken > 0:
        total_score = sum(result.score for result in all_quiz_results)
        total_possible = sum(result.total for result in all_quiz_results)
        avg_score = int((total_score / total_possible) * 100) if total_possible > 0 else 0
    else:
        avg_score = 0
    
    # Get course completion data
    course_completion = {}
    courses = ['cs', 'ai', 'cse', 'aiml']
    for course in courses:
        # Count how many users have completed this course (score >= 60%)
        completed_count = QuizResult.query.filter(
            db.and_(
                QuizResult.subject == course,
                (QuizResult.score / QuizResult.total) >= 0.6
            )
        ).count()
        course_completion[course] = completed_count
    
    return render_template("admin_dashboard.html", 
                          total_students=total_students,
                          total_courses=total_courses,
                          avg_score=avg_score,
                          users=users_serializable,
                          course_completion=course_completion,
                          total_quizzes_taken=total_quizzes_taken)

# Add a route for adding new admins
@app.route("/add_admin", methods=["POST"])
def add_admin():
    print("DEBUG: add_admin route called")
    # Check if user is admin
    if "user_id" not in session or session.get("role") != "admin":
        print("DEBUG: Access denied - user not admin")
        flash("Access denied.", "danger")
        return redirect(url_for("login"))
    
    print("DEBUG: User authorized as admin")
    # Get form data
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    role = "admin"  # Force role to admin
    
    print(f"DEBUG: Form data - username: {username}, email: {email}, password: {'*' * len(password) if password else 'empty'}")
    
    # Validate input
    if not username or not email or not password:
        print("DEBUG: Validation failed - missing fields")
        flash("All fields required.", "warning")
        return redirect(url_for("admin_dashboard"))
    
    # Check if user already exists
    existing_user = User.query.filter(db.or_(User.username==username, User.email==email)).first()
    if existing_user:
        print(f"DEBUG: User already exists - username: {existing_user.username}, email: {existing_user.email}")
        flash("User with this username or email already exists.", "warning")
        return redirect(url_for("admin_dashboard"))
    
    print("DEBUG: Creating new admin user")
    # Create new admin user
    hashed = generate_password_hash(password, "pbkdf2:sha256")
    user = User(username=username, email=email, password=hashed, role=role)
    db.session.add(user)
    db.session.commit()
    
    print(f"DEBUG: Admin user created successfully - id: {user.id}, username: {user.username}")
    flash("Admin user created successfully.", "success")
    return redirect(url_for("admin_dashboard"))

# -------- Chatbot --------
@app.route("/chat", methods=["POST"])
def chat():
    result = get_chat_response((request.json or {}).get("message",""))
    return jsonify(result)

# Add API endpoint for student progress data
@app.route("/api/student/<int:student_id>/progress")
def student_progress(student_id):
    if "user_id" not in session or session.get("role") != "admin":
        return jsonify({"error": "Access denied"}), 403
    
    # Get student user
    student = User.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    # Get quiz results for this student
    quiz_results = QuizResult.query.filter_by(user_id=student_id).all()
    
    # Prepare course progress data
    course_progress = []
    quiz_scores = []
    
    # Group quiz results by subject
    subject_results = {}
    for result in quiz_results:
        if result.subject not in subject_results:
            subject_results[result.subject] = []
        subject_results[result.subject].append(result)
    
    # Calculate progress for each subject
    for subject, results in subject_results.items():
        # Get the latest quiz result for this subject
        latest_result = max(results, key=lambda r: r.timestamp)
        
        # Add to quiz scores
        quiz_scores.append({
            "subject": subject.upper(),
            "score": int((latest_result.score / latest_result.total) * 100),
            "correct": latest_result.score,
            "total": latest_result.total
        })
        
        # Add to course progress (assuming 6 lessons per course)
        course_progress.append({
            "name": subject.upper(),
            "progress": int((latest_result.score / latest_result.total) * 100),
            "completed": latest_result.score,
            "total": latest_result.total
        })
    
    # Recent activity (last 3 quiz results)
    recent_results = sorted(quiz_results, key=lambda r: r.timestamp, reverse=True)[:3]
    recent_activity = []
    for result in recent_results:
        recent_activity.append(
            f"Scored {int((result.score / result.total) * 100)}% on {result.subject.upper()} Quiz "
            f"({result.timestamp.strftime('%b %d, %Y') if result.timestamp else 'Recent'})"
        )
    
    return jsonify({
        "student_id": student_id,
        "username": student.username,
        "enrollment_date": "Oct 15, 2025",  # Placeholder
        "last_active": "Today",  # Placeholder
        "course_progress": course_progress,
        "quiz_scores": quiz_scores,
        "recent_activity": recent_activity
    })

# -------------------- MAIN --------------------
if __name__=="__main__":
    app.run(debug=True)