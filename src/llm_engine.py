import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict

# Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Fail gracefully if key is missing (for UI handling)
    print("WARNING: GEMINI_API_KEY not found in .env")

# Configure Gemini
genai.configure(api_key=api_key)
MODEL_NAME = "gemini-1.5-flash" # Optimized for speed and JSON tasks

def get_json_model():
    """Returns a model configured to output strict JSON."""
    return genai.GenerativeModel(
        MODEL_NAME,
        generation_config={"response_mime_type": "application/json"}
    )

def get_text_model():
    """Returns a standard text generation model."""
    return genai.GenerativeModel(MODEL_NAME)

def generate_tech_questions(tech_stack: str):
    """(TalentScout) Generates 3 interview questions based on stack."""
    model = get_json_model()
    prompt = (
        f"You are a Senior Technical Recruiter. "
        f"Generate 3 challenging technical interview questions for a candidate specializing in: {tech_stack}. "
        f"Return ONLY a JSON list of strings. Example: [\"Question 1\", \"Question 2\"]"
    )
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print(f"LLM Error: {e}")
        return ["Describe your experience with this stack.", "What is the hardest bug you've solved?", "Explain a core concept."]

def generate_prep_question(topic: str, difficulty: str):
    """(PrepMaster) Generates a single practice question."""
    model = get_text_model()
    prompt = (
        f"Generate exactly one {difficulty}-level interview question about '{topic}'. "
        "Do not provide the answer, just the question text."
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Tell me about your experience with {topic}."

def analyze_answer(question: str, answer: str):
    """(PrepMaster) Grades the user's answer."""
    model = get_json_model()
    prompt = (
        f"You are an Expert Interview Coach. Evaluate the following answer.\n\n"
        f"Question: {question}\n"
        f"Candidate Answer: {answer}\n\n"
        "Return a JSON object with exactly these keys:\n"
        "- score (integer 0-100)\n"
        "- feedback (string, constructive critique)\n"
        "- sample_answer (string, a perfect example response)\n"
    )
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {"score": 0, "feedback": "Error analyzing answer via API.", "sample_answer": "N/A"}

# ============ MCQ Quiz Generation ============

def generate_mcq_questions(language: str, difficulty: str, count: int = 10) -> List[Dict]:
    """
    Generate MCQ questions for a programming language at specified difficulty.
    
    Args:
        language: Programming language (C, C++, Java, JavaScript, HTML, CSS)
        difficulty: Difficulty level (Easy, Medium, Hard)
        count: Number of questions to generate (default: 10)
    
    Returns:
        List of dictionaries with question, options, correct_answer, and explanation
    """
    model = get_json_model()
    
    prompt = f"""You are an expert programming instructor creating MCQ questions.

Generate exactly {count} multiple-choice questions for {language} programming at {difficulty} difficulty level.

Requirements:
- Questions should test practical knowledge and understanding
- Each question must have exactly 4 options (A, B, C, D)
- Only ONE option should be correct
- Include a brief explanation for the correct answer
- For {difficulty} difficulty:
  * Easy: Basic syntax, fundamental concepts
  * Medium: Practical applications, common patterns
  * Hard: Advanced concepts, edge cases, optimization

Return a JSON array with this exact structure:
[
  {{
    "question": "Question text here?",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "correct_answer": "A",
    "explanation": "Brief explanation why this is correct"
  }}
]

Generate {count} questions now for {language} at {difficulty} level."""

    try:
        response = model.generate_content(prompt)
        questions = json.loads(response.text)
        
        # Validate structure
        if isinstance(questions, list) and len(questions) == count:
            for q in questions:
                if not all(key in q for key in ['question', 'options', 'correct_answer', 'explanation']):
                    raise ValueError("Invalid question structure")
            return questions
        else:
            raise ValueError(f"Expected {count} questions, got {len(questions) if isinstance(questions, list) else 0}")
            
    except Exception as e:
        print(f"MCQ Generation Error: {e}")
        # Return fallback questions
        return generate_fallback_questions(language, difficulty, count)

def generate_fallback_questions(language: str, difficulty: str, count: int) -> List[Dict]:
    """Generate simple fallback questions if API fails."""
    fallback = {
        "C": {
            "question": f"What is the output of printf(\"%d\", 5 + 3); in C?",
            "options": {"A": "8", "B": "53", "C": "5 + 3", "D": "Error"},
            "correct_answer": "A",
            "explanation": "The printf function evaluates the expression 5 + 3 and prints 8."
        },
        "C++": {
            "question": f"Which keyword is used to define a class in C++?",
            "options": {"A": "struct", "B": "class", "C": "object", "D": "define"},
            "correct_answer": "B",
            "explanation": "The 'class' keyword is used to define classes in C++."
        },
        "Java": {
            "question": f"What is the default value of a boolean variable in Java?",
            "options": {"A": "true", "B": "false", "C": "0", "D": "null"},
            "correct_answer": "B",
            "explanation": "Boolean variables in Java are initialized to false by default."
        },
        "JavaScript": {
            "question": f"What does '===' operator check in JavaScript?",
            "options": {"A": "Value only", "B": "Type only", "C": "Both value and type", "D": "Neither"},
            "correct_answer": "C",
            "explanation": "The === operator checks for both value and type equality (strict equality)."
        },
        "HTML": {
            "question": f"Which tag is used to create a hyperlink in HTML?",
            "options": {"A": "<link>", "B": "<a>", "C": "<href>", "D": "<url>"},
            "correct_answer": "B",
            "explanation": "The <a> (anchor) tag is used to create hyperlinks in HTML."
        },
        "CSS": {
            "question": f"Which property is used to change text color in CSS?",
            "options": {"A": "text-color", "B": "font-color", "C": "color", "D": "text-style"},
            "correct_answer": "C",
            "explanation": "The 'color' property is used to change text color in CSS."
        }
    }
    
    base_question = fallback.get(language, fallback["C"])
    return [base_question.copy() for _ in range(count)]
