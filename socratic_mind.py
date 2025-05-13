import streamlit as st
import openai
from dotenv import load_dotenv
import os
import speech_recognition as sr

# Load the API key from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up the app title and instructions
st.title("Socratic Mind - Oral Assessment")
st.write("Answer by typing or speaking!")

# Set the sample question
question = "What is photosynthesis?"
st.write(f"Question: {question}")

# Store the conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an Oral Examiner. Use Socratic questioning to guide the student to the answer without giving it directly. Focus on how plants use sunlight."},
        {"role": "assistant", "content": question}
    ]

# Add a button for speech input
if st.button("Speak Answer"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak now...")
        audio = r.listen(source)
    try:
        answer = r.recognize_google(audio)
        st.write(f"You said: {answer}")
    except:
        answer = ""
        st.write("Sorry, I didn’t hear you.")
else:
    answer = st.text_input("Type your answer here:")

# Process the answer with OpenAI
if answer:
    st.session_state.messages.append({"role": "user", "content": answer})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use gpt-4-turbo if you have access
        messages=st.session_state.messages
    )
    ai_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.write(f"AI Teacher: {ai_reply}")

# Show the conversation history
for msg in st.session_state.messages[1:]:  # Skip the system prompt
    if msg["role"] == "user":
        st.write(f"You: {msg['content']}")
    else:
        st.write(f"AI Teacher: {msg['content']}")