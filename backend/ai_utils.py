import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

def is_mock_mode():
    return not API_KEY

if not is_mock_mode():
    client = OpenAI(api_key=API_KEY)

def generate_study_plan(subjects: str, exam_date: str, daily_hours: float, weak_subjects: str):
    if is_mock_mode():
        return f"""
        **Mock Study Plan**
        - Subjects: {subjects}
        - Exam Date: {exam_date}
        - Daily Target: {daily_hours} hours
        
        *Focus strongly on {weak_subjects} as you indicated.*
        
        Day 1: 
        - 1h {weak_subjects} basics
        - 1h Revision of other subjects
        
        Day 2:
        - 1h {weak_subjects} exercises
        - 1h Practice test
        """

    prompt = f"""
    You are an expert Study Planner AI. Create a detailed daily study timetable and weekly revision plan.
    Student parameters:
    - Subjects: {subjects}
    - Exam date: {exam_date}
    - Daily available study hours: {daily_hours}
    - Weak subjects: {weak_subjects}

    Create a priority-based distributed plan where weak subjects get more time, and closer to exam means more revision. Include break times.
    Format your response cleanly in Markdown.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def explain_doubt(question: str, difficulty: str):
    if is_mock_mode():
        return f"""
        **Mock Explanation ({difficulty} mode)**
        
        *Simple Explanation:* 
        This is a mock response for "{question}". It usually means breaking down the problem into smaller steps.
        
        *Example/Analogy:*
        Imagine you have a big pizza. You slice it to eat it.
        """

    prompt = f"""
    You are a Smart Doubt Explainer AI. Explain the following question: "{question}"
    
    Difficulty level chosen by student: "{difficulty}" (options: 'like I'm 10', 'intermediate', 'technical').
    
    Provide:
    1. A clear explanation at the chosen difficulty.
    2. An example.
    3. Step-by-step breakdown.
    4. A real-world analogy.
    Format using Markdown.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
<<<<<<< HEAD


def analyze_weak_subjects(study_data: dict):
    if is_mock_mode():
        subject = study_data.get('least_studied_subject', 'your subjects')
        return f"""
        **📊 AI Mentor Analysis**
        
        Based on your study patterns, here's what we found:
        
        🔍 *Weak Area Identified:* {subject}
        You've been spending less time on this subject compared to others.
        
        💡 **Personalized Improvement Tips:**
        1. Dedicate 30 minutes daily specifically to {subject}
        2. Start with foundational concepts before moving to advanced topics
        3. Use active recall techniques - test yourself after each study session
        4. Review notes within 24 hours of studying
        5. Mix practice problems with theory for better retention
        
        🎯 *Weekly Goal:* Increase study time for {subject} by 20% this week!
        """

    prompt = f"""
    You are an expert AI Study Mentor. Analyze the following student study pattern data and provide personalized improvement suggestions.

    Student Study Data:
    - Most studied subject: {study_data.get('most_studied_subject', 'N/A')}
    - Least studied subject: {study_data.get('least_studied_subject', 'N/A')}
    - Average daily study time: {study_data.get('average_daily_minutes', 0)} minutes
    - Total study sessions: {study_data.get('total_sessions', 0)}
    - Total study time: {study_data.get('total_minutes', 0)} minutes
    - Most productive hour: {study_data.get('most_productive_hour', 'N/A')}

    Provide:
    1. Identify potential weak subject areas based on study time distribution
    2. 3-5 specific, actionable improvement tips
    3. A realistic weekly goal
    4. Motivation and encouragement

    Keep the tone supportive and encouraging. Use Markdown formatting.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
=======
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
