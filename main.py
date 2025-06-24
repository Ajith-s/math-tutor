import os
from dotenv import load_dotenv
import streamlit as st
from agent_graph import question_generator_node, hint_generator_node, answer_checker_node
from helper_functions import init_static_session_state, process_submission, load_user_into_session
from auth import check_login, update_user

# Load environment
load_dotenv()
openai_api_key = st.secrets.get("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize session state
init_static_session_state()

# Check login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

if not check_login():
    st.stop()

# Load user data
load_user_into_session(st.session_state.user)

# App title
st.title("📚 AI Powered Math Tutor")

# User profile sync
user = st.session_state.user
user.setdefault("total_score", 0)
user.setdefault("streak", 0)
st.session_state.total_score = user["total_score"]
st.session_state.answer_streak = user["streak"]

st.markdown(f"👋 Welcome **{user['name']}** | 🧠 Streak: `{user['streak']}` | 🌟 Score: `{user['total_score']}`")

# Sidebar logout
def logout():
    st.session_state.clear()
    st.rerun()

with st.sidebar:
    st.markdown(f"👤 Logged in as **{user['name']}**")
    if st.button("🚪 Log out"):
        logout()

# Selectors
TOPICS = ["General", "Algebra", "Geometry", "Arithmetic", "Statistics"]
selected_grade = st.selectbox("Select your grade", ["5th Grade", "6th Grade", "7th Grade", "8th Grade", "9th Grade"])
selected_topic = st.selectbox("Select a topic", TOPICS)
selected_difficulty = st.selectbox("Choose your starting difficulty level:", ["Easy", "Medium", "Hard"])

# Generate question
if st.button("🎯 Generate New Question"):
    st.session_state.graph_state.pop("solution", None)
    st.session_state.graph_state["grade"] = selected_grade
    st.session_state.graph_state["difficulty"] = selected_difficulty
    st.session_state.graph_state["topic"] = selected_topic
    st.session_state.graph_state = question_generator_node(st.session_state.graph_state)
    # 🧹 Reset answer input
    st.session_state["user_answer_input"] = ""

if "current_question" not in st.session_state.graph_state:
    st.info("👋 Select a topic and difficulty, then click **Generate New Question** to begin.")
    st.stop()

# Display question
question_data = st.session_state.graph_state["current_question"]
points = question_data.get("points_possible", "?")
question_topic = question_data.get("topic", selected_topic)

st.markdown(f"### {question_data['question']}")
st.markdown(f"**📘 Topic:** `{question_topic}`")
emoji = "🏆" if isinstance(points, int) and points >= 20 else "🎯" if isinstance(points, int) and points >= 12 else "💡"
st.markdown(f"<div style='font-size:20px; margin-top:8px; color:#006400;'><b>{emoji} {points} points</b></div>", unsafe_allow_html=True)

user_answer = st.text_area("✍️ Enter your answer here:", key="user_answer_input")

col1, col2 = st.columns(2)
submit_answer = col1.button("✅ Submit Answer")
get_hint = col2.button("💡 Get a Hint")

# Initialize score/hint counters
st.session_state.setdefault("score_total", 0)
st.session_state.setdefault("hint_count", 0)

# Submit logic
if submit_answer and user_answer.strip():
    st.session_state.graph_state["user_answer"] = user_answer.strip()
    st.session_state.graph_state = answer_checker_node(st.session_state.graph_state)
    result = process_submission(st.session_state.graph_state, user)

    # Update session + persist
    st.session_state.user = result["updated_user"]
    st.session_state.total_score = user["total_score"]
    st.session_state.answer_streak = user["streak"]
    update_user(user)

    if result["answer_correct"]:
        st.success(f"✅ **Correct Answer!** You earned **{result['score']} points**.")
    else:
        st.error(f"❌ **Incorrect Answer!** Please try again {user.get('name', '')}.")
    
    if result["feedback"]:
        st.info(f"💬 Feedback: {result['feedback']}")

# Hint logic
if get_hint:
    st.session_state.graph_state = hint_generator_node(st.session_state.graph_state)
    hint = st.session_state.graph_state.get("hint", "No hint available.")
    st.info(f"💬 Hint: {hint}")

# Footer
st.markdown("---")
st.subheader("About This App")
st.markdown("Github Repo: [https://github.com/Ajith-s/math-tutor](https://github.com/Ajith-s/math-tutor)")
st.markdown("This app is developed by Ajith Sharma for educational purposes. It uses OpenAI's GPT-4 model to provide personalized Math tutoring.")
st.markdown("Please provide feedback to help improve it! Open an issue on the GitHub repository.")
