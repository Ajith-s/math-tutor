# AI Powered Math Tutor

An interactive, AI-driven math tutoring app that generates personalized math questions, provides guided hints, checks answers, and tracks user progress. Designed to create an engaging and data-driven learning experience for students.
Streamlit link: https://ai-math-tutor.streamlit.app/

⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻
## Features

	•	Dynamic question generation: Math questions tailored by grade, topic, and difficulty (Easy, Medium, Hard).
	•	Smart scoring system: Awards points based on difficulty level and reduces points for hint usage. Tracks both total score and answer streaks.
	•	Hint engine: Provides contextually relevant hints without revealing the answer.
	•	User authentication and persistence: User scores, streaks, and progress are securely saved in Firestore.
	•	Minimalist, functional UI: Built with Streamlit for a clean and intuitive interface.

⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻
## Tech Stack
	•	Streamlit (frontend and app logic)
	•	OpenAI GPT-4 (question generation, hint creation, answer validation)
	•	Firebase / Firestore (user data storage)
	•	Python (3.10+ recommended)
⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻

## Application Workflow
<img width="695" alt="image" src="https://github.com/user-attachments/assets/421060a6-cbb6-4ba5-9e84-6843dab5f825" />

⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻

## Installation
``` bash
# Clone the repository
git clone https://github.com/your-username/ai-math-tutor.git
cd ai-math-tutor

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻
## Configuration
Create a .streamlit/secrets.toml file and add your credentials:
``` toml
OPENAI_API_KEY = "your-openai-api-key"
FIREBASE_PROJECT_ID = "your-firebase-project-id"
FIREBASE_PRIVATE_KEY = "your-firebase-private-key"
FIREBASE_CLIENT_EMAIL = "your-firebase-client-email"
```
*Important:* 
Do not commit your secrets.toml. This file should stay local or be configured using Streamlit Cloud’s Secrets Manager.

⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻

## Example Screens
<img width="751" alt="image" src="https://github.com/user-attachments/assets/76434fce-87b1-468d-bd39-1158bb425357" />
<img width="751" alt="image" src="https://github.com/user-attachments/assets/075bc94e-ee8e-4ea1-9973-c5a209e4287c" />



