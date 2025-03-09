import streamlit as st
import gradio as gr
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google AI with free API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def generate_study_plan(inputs):
    """Generate personalized study plan using Google's Free AI API"""
    # try:
    #     # Try different available models
    model = genai.GenerativeModel('models/gemini-2.0-flash')  # Newer model name
    # except:
    # model = genai.GenerativeModel('text-bison-001')  # Fallback model

    prompt = f"""Create a personalized study plan for {inputs['name']} focusing on {inputs['subjects']}.
    Goals: {inputs['goals']}
    Strengths: {inputs['strengths']}
    Weaknesses: {inputs['weaknesses']}
    Preferences: {inputs['preferences']}
    Available hours/day: {inputs['hours']}
    Include: time allocation, learning methods, exercises, progress tracking"""

    response = model.generate_content(prompt)
    return response.text


# Streamlit UI
st.title("🎓 Free Studbud: AI Study Planner")
st.markdown("### Free Academic Planning Tool")

with st.form("study_form"):
    name = st.text_input("Student Name")
    subjects = st.multiselect("Subjects", ["Math", "Science", "History", "Languages", "Computer Science"])
    hours = st.slider("Daily Study Hours", 1, 8, 2)
    goals = st.text_area("Learning Objectives")
    strengths = st.text_input("Strong Areas")
    weaknesses = st.text_input("Weak Areas")
    preferences = st.multiselect("Learning Styles", ["Visual", "Audio", "Reading", "Practice"])

    submitted = st.form_submit_button("Generate Plan")

if submitted:
    inputs = {
        'name': name,
        'subjects': ', '.join(subjects),
        'goals': goals,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'preferences': ', '.join(preferences),
        'hours': hours
    }

    with st.spinner("Creating your plan..."):
        try:
            plan = generate_study_plan(inputs)
            st.subheader("Your Study Plan")
            st.write(plan)
            st.download_button("Download Plan", plan, "study_plan.txt")
        except Exception as e:
            st.error(f"Please try again. Error: {str(e)}")

# Gradio Interface
gr.Interface(
    fn=generate_study_plan,
    inputs=[
        gr.Textbox(label="Name"),
        gr.Dropdown(["Math", "Science", "History"], label="Subjects", multiselect=True),
        gr.Slider(1, 8, label="Hours/Day"),
        gr.Textbox(label="Goals"),
        gr.Textbox(label="Strengths"),
        gr.Textbox(label="Weaknesses"),
        gr.CheckboxGroup(["Visual", "Reading", "Practice"], label="Preferences")
    ],
    outputs=gr.Textbox(label="Study Plan"),
    title="Free Studbud Planner",
    description="Generate personalized study plans with free AI"
).launch()