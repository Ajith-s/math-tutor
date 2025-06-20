import streamlit as st

def init_static_session_state():
    static_defaults = {
        "graph_state": {"difficulty": "easy"},
        "submit_requested": False,
        "selected_topic": "General",
        "points_earned": 0,
        "hints_used": 0,
    }
    for key, value in static_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_user_into_session(user):
    st.session_state.user = user
    st.session_state.total_score = user.get("total_score", 0)
    st.session_state.answer_streak = user.get("streak", 0)
    st.session_state.hints_used = user.get("hints_used", 0)
    # Backfill defaults if missing (esp. for older users)
    if "answered_questions" not in user:
        user["answered_questions"] = []
    if "last_answered_question" not in user:
        user["last_answered_question"] = None


def process_submission(graph_state, user):
    feedback = graph_state.get("feedback", "")
    answer_correct = graph_state.get("answer_correct", False)
    question_data = graph_state.get("current_question", {})
    question_text = question_data.get("question", "")
    points = int(question_data.get("points_possible", 0) or 0)
    hints_used = graph_state.get("hint_count", 0)

    score = max(points - (2 * hints_used), 0)

    # Initialize keys if missing
    user["total_score"] = user.get("total_score", 0)
    user["streak"] = user.get("streak", 0)
    user["answered_questions"] = user.get("answered_questions", [])

    if answer_correct:
        user["total_score"] += score
        user["streak"] += 1
        user["last_answered_question"] = question_text
        user["hints_used"] = hints_used

        already_answered = any(q["question"] == question_text for q in user["answered_questions"])
        if not already_answered:
            user["answered_questions"].append({
                "question": question_text,
                "topic": question_data.get("topic", "General"),
                "difficulty": question_data.get("difficulty", "easy"),
                "points_possible": question_data.get("points_possible", 0),
                "score_earned": score,
                "test_cases": question_data.get("test_cases", []),
                "user_code": graph_state.get("user_answer", "")
            })
    else:
        user["streak"] = 0

    return {
        "answer_correct": answer_correct,
        "score": score,
        "feedback": feedback,
        "updated_user": user
    }


# def process_submission(graph_state):
#     feedback = graph_state.get("feedback", "")
#     answer_correct = graph_state.get("answer_correct", False)
#     question_data = graph_state.get("current_question", {})
#     question_text = question_data.get("question", "")
#     points = int(question_data.get("points_possible", 0) or 0)
#     hints_used = graph_state.get("hint_count", 0)
#     user_answer = graph_state.get("user_answer", "")

#     score = max(points - (2 * hints_used), 0)

#     # Build result object
#     result = {
#         "answer_correct": answer_correct,
#         "score": score,
#         "feedback": feedback,
#         "question_summary": {
#             "question": question_text,
#             "topic": question_data.get("topic", "General"),
#             "difficulty": question_data.get("difficulty", "easy"),
#             "points_possible": points,
#             "score_earned": score,
#             "hints_used": hints_used,
#             "test_cases": question_data.get("test_cases", []),
#             "user_code": user_answer
#         }
#     }

#     return result