# quiz_feedback.py
def evaluate_quiz(subject_q, form_data):
    score = 0
    feedback = []
    weak_areas = []

    for i, q in enumerate(subject_q, 1):
        selected = form_data.get(f"q{i}")
        if selected == q["answer"]:
            score += 1
        else:
            feedback.append({
                "question": q["question"],
                "correct": q["answer"],
                "your_answer": selected or "Not answered"
            })
            weak_areas.append(q["question"])

    recommendations = generate_recommendations(weak_areas)
    return score, feedback, recommendations


def generate_recommendations(weak_areas):
    recommendations = []
    for q in weak_areas:
        if "cell" in q.lower():
            recommendations.append("Review the cell structure and its functions in Biology.")
        elif "force" in q.lower():
            recommendations.append("Revise Newton's Laws of Motion in Physics.")
        elif "2 + 2" in q:
            recommendations.append("Practice basic arithmetic in Mathematics.")
        else:
            recommendations.append("Revise the concept related to this question.")
    return recommendations