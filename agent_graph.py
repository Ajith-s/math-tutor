from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph
from typing import TypedDict
from dotenv import load_dotenv

import os


# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Define the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

class GraphState(TypedDict, total=False):
    grade: str
    topic: dict
    user_answer: str
    feedback: str
    hint: str

QUESTION_PROMPT_TEMPLATE = """
You are a smart and helpful mathematics tutor. You will generate a math question based on the given grade, topic and difficulty. Questions should be reasonable and make the student think critically.
Generate a new question and do not repeat the previous question.
Grade: {grade}
Topic: {topic}
Difficulty: {difficulty}

Higher difficulty and grade means more complex questions.
This is used by kids, so make sure to use simple and clear language.

Format your response as follows:
Question: <question>
"""

def question_generator_node(state: GraphState) -> GraphState:
    difficulty = state.get("difficulty", "easy")
    
    prompt_template = PromptTemplate(
        input_variables=["grade", "topic", "difficulty"],
        template=QUESTION_PROMPT_TEMPLATE
    )
    
    formatted_prompt = prompt_template.format(
        grade=state.get("grade", "5th Grade"),
        topic=state.get("topic", "general"),
        difficulty=difficulty
    )
    
    question = llm.invoke(formatted_prompt)
    question_text = question.content.strip() if hasattr(question, "content") else str(question).strip()

    # 🎯 Assign points
    points = assign_point_value(question_text, difficulty)

    # Update the state
    state["current_question"] = {
        "question": question_text,
        "topic": state.get("topic", "General"),
        "grade": state.get("grade", "5th Grade"),
        "difficulty": difficulty,
        "points_possible": points
    }

    return state

def assign_point_value(question_text, difficulty):
    prompt = f"""
    You are an expert coding tutor.

    Given the following Mathematical  question and its difficulty level, assign a point value based on its depth, complexity, and required reasoning.
    Rules:
    - Easy: 5 to 10 points
    - Medium: 12 to 18 points
    - Hard: 20 to 25 points

    Return just the number. No explanation.

    Difficulty: {difficulty}
    Question: {question_text}
    """
    response = llm.invoke(prompt)
    try:
        return int(response.content.strip())
    except:
        return 5  # fallback
    
def hint_generator_node(state: GraphState) -> GraphState:
    question_text = state.get("current_question", {}).get("question", "")
    prompt = f"""
    You are a helpful Mathematics tutor.
    Given the question:\n\n{question_text}
    Provide a hint to help the student.
    """
    response = llm.invoke(prompt)
    state["hint"] = response.content
    # Track number of hints used
    state["hint_count"] = state.get("hint_count", 0) + 1
    return state

def answer_checker_node(state: GraphState) -> GraphState:
    user_answer = state.get("user_answer", "")
    question_text = state.get("current_question", {}).get("question", "")
    prompt = f"""
    You are a helpful math tutor.

    Given the question:\n\n{question_text}
    and the student's answer:\n\n{user_answer}

    First, determine if the answer is correct. Then, give a brief feedback in under 15 words.

    Format:
    Correct: <Yes or No>
    Feedback: <your feedback>
    """
    response = llm.invoke(prompt)
    content = response.content.strip()

    # Simple parsing logic
    is_correct = "correct: yes" in content.lower()
    feedback = ""
    for line in content.splitlines():
        if line.lower().startswith("feedback:"):
            feedback = line.split(":", 1)[-1].strip()

    state["feedback"] = feedback or "No feedback."
    state["answer_correct"] = is_correct
    return state

def compute_score(base_points: int, hint_count: int) -> int:
    deduction = min(hint_count * 2, base_points - 1)  # 2 points per hint
    return base_points - deduction

graph = StateGraph(GraphState)


graph.add_node("question_generator", question_generator_node)
graph.add_node("answer_checker", answer_checker_node)
graph.add_node("hint_generator", hint_generator_node)

# Connect the nodes
graph.set_entry_point("question_generator")
graph.add_edge("question_generator", "answer_checker")
graph.add_edge("answer_checker", "hint_generator")

# Define entry point
graph.set_entry_point("question_generator")

# Compile the graph
graph = graph.compile()