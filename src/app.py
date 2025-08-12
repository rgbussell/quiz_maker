import streamlit as st
import pytesseract
from PIL import Image
from openai import OpenAI as Client
import json
import os
from dotenv import load_dotenv


# load the environment
load_dotenv("../.env")

# Set your xAI API key (or use environment variable for security)
api_key = os.getenv("API_KEY")
client = Client(api_key=api_key, base_url="https://api.x.ai/v1")  # Replace with your key

st.title("Fun Homework Quiz Generator 🎉")
st.write("Snap a photo of your homework or reading, and I'll create an engaging quiz to help you learn!")

# Step 1: Capture photo from webcam
img_file = st.camera_input("Take a photo of the assignment")

if img_file:
    # Step 2: Extract text using OCR
    st.write("Extracting text from the photo...")
    image = Image.open(img_file)
    extracted_text = pytesseract.image_to_string(image)
    
    st.subheader("Extracted Text:")
    st.text_area("", extracted_text, height=150)
    
    if extracted_text.strip():  # Proceed if text was extracted
        # Step 3: Generate quiz using AI
        if st.button("Generate Quiz! 🚀"):
            with st.spinner("Creating fun questions..."):
                prompt = f"""
                Based on this middle school homework text: "{extracted_text}"
                
                Generate a fun, engaging quiz with 5 multiple-choice questions. Make it exciting for kids with emojis!
                Return ONLY JSON in this format:
                {{
                    "questions": [
                        {{
                            "question": "Question text?",
                            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                            "correct_index": 0  // 0-based index of correct option
                        }}
                    ]
                }}
                """
                
                response = client.chat.completions.create(
                    model="grok-4-0709",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                try:
                    quiz_data = json.loads(response.choices[0].message.content)
                    st.session_state.quiz = quiz_data["questions"]
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.answers = {}
                except:
                    st.error("Oops! Quiz generation failed. Try again or check the text.")
    
    # Step 4: Deliver the quiz interactively
    if "quiz" in st.session_state:
        questions = st.session_state.quiz
        current = st.session_state.current_question
        
        if current < len(questions):
            q = questions[current]
            st.subheader(f"Question {current + 1}/{len(questions)}: {q['question']}")
            
            # Display options as radio buttons
            selected = st.radio("Choose your answer:", q["options"], key=f"q{current}")
            selected_index = q["options"].index(selected) if selected else -1
            
            if st.button("Submit Answer"):
                correct_index = q["correct_index"]
                if selected_index == correct_index:
                    st.success("Correct! 🎊")
                    st.session_state.score += 1
                else:
                    st.error(f"Wrong! The correct answer is: {q['options'][correct_index]} 😔")
                
                st.session_state.answers[current] = selected_index
                st.session_state.current_question += 1
                st.experimental_rerun()  # Refresh to next question
        
        else:
            # Quiz complete
            st.subheader("Quiz Complete! 🏆")
            st.write(f"Your score: {st.session_state.score}/{len(questions)}")
            if st.button("Restart Quiz"):
                del st.session_state.quiz
                st.experimental_rerun()

else:
    st.info("Start by taking a photo!")