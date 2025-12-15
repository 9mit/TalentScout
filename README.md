# PrepMaster MCQ Quiz System - Quick Start Guide

## 🚀 Running the Application

### Option 1: Streamlit Web Interface (Recommended)
```bash
streamlit run main.py
```
Then select "🎓 PrepMaster (Candidate)" from the sidebar.

### Option 2: Console Application
```bash
python run_console.py
```

## 📋 Features Implemented

### ✅ Language Selection
- C
- C++
- Java
- JavaScript
- HTML
- CSS

### ✅ Difficulty Levels
- 🟢 Easy - Basic syntax and fundamental concepts
- 🟡 Medium - Practical applications and common patterns
- 🔴 Hard - Advanced concepts, edge cases, optimization

### ✅ Quiz System
- 10 AI-generated MCQ questions per quiz
- Real-time answer validation
- Detailed explanations for each question
- Time tracking
- Score calculation

### ✅ Analytics Dashboard
- Overall performance metrics
- Performance by language
- Performance by difficulty level
- Quiz history (last 10 attempts)
- Best/worst scores tracking

## 📊 How to Use

1. **Start a Quiz**
   - Select your programming language
   - Choose difficulty level
   - Answer 10 MCQ questions
   - Review your score and explanations

2. **View Analytics**
   - See your overall performance
   - Track progress by language
   - Analyze difficulty-wise performance

3. **Review History**
   - View past quiz attempts
   - Track improvement over time

## 🔧 Requirements

Make sure you have:
- Python 3.8+
- Google Gemini API key in `.env` file
- All dependencies installed: `pip install -r requirements.txt`

## 📝 Database

All quiz results are automatically saved to `career_suite.db` for analytics and history tracking.
