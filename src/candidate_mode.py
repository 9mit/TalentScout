"""
PrepMaster - Candidate Mode UI & Logic
MCQ Quiz System for Programming Languages
"""

import time
from typing import List, Dict
from src.llm_engine import generate_mcq_questions
from src.database import (
    save_quiz_result, 
    get_quiz_history, 
    get_analytics_by_language,
    get_analytics_by_difficulty,
    get_overall_analytics
)


class PrepMaster:
    """PrepMaster mode for candidates - MCQ Quiz System"""
    
    LANGUAGES = ["C", "C++", "Java", "JavaScript", "HTML", "CSS"]
    DIFFICULTIES = ["Easy", "Medium", "Hard"]
    QUESTIONS_PER_QUIZ = 10
    
    def __init__(self):
        """Initialize PrepMaster"""
        self.current_quiz = None
        self.user_answers = []
        self.score = 0
        
    def run(self):
        """Run the PrepMaster interface"""
        self.clear_screen()
        self.print_header()
        
        while True:
            choice = self.show_main_menu()
            
            if choice == "1":
                self.show_study_roadmap()
            elif choice == "2":
                self.start_quiz()
            elif choice == "3":
                self.view_analytics()
            elif choice == "4":
                self.view_quiz_history()
            elif choice == "5":
                print("\n👋 Thank you for using PrepMaster! Good luck with your preparation!\n")
                break
            else:
                print("\n❌ Invalid choice. Please try again.\n")
                time.sleep(1)
    
    def clear_screen(self):
        """Clear the console screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print PrepMaster header"""
        print("=" * 70)
        print("🎓 PREPMASTER - MCQ Quiz System".center(70))
        print("Master Programming Languages with AI-Powered Questions".center(70))
        print("=" * 70)
        print()
    
    def show_main_menu(self) -> str:
        """Display main menu and get user choice"""
        print("\n" + "─" * 70)
        print("📚 MAIN MENU")
        print("─" * 70)
        print("1. 📖 Study Roadmap")
        print("2. 🚀 Start New Quiz")
        print("3. 📊 View Analytics")
        print("4. 📜 Quiz History")
        print("5. 🚪 Exit")
        print("─" * 70)
        return input("\nEnter your choice (1-5): ").strip()
    
    def show_study_roadmap(self):
        """Display structured preparation plan"""
        self.clear_screen()
        self.print_header()
        
        print("\n📖 STUDY ROADMAP - Structured Preparation Plan")
        print("=" * 70)
        
        # Category 1: Computer Science Fundamentals
        print("\n" + "─" * 70)
        print("📘 1. COMPUTER SCIENCE FUNDAMENTALS")
        print("─" * 70)
        print("   • Arrays - Linear data structures, indexing, traversal")
        print("   • Trees - Binary trees, BST, traversal algorithms")
        print("   • Graphs - Representations, traversal, shortest paths")
        print("   • Hash Maps - Hash functions, collision handling, applications")
        
        # Category 2: Algorithms
        print("\n" + "─" * 70)
        print("📗 2. ALGORITHMS")
        print("─" * 70)
        print("   • Sorting - QuickSort, MergeSort, HeapSort, complexity analysis")
        print("   • BFS/DFS - Breadth-first and depth-first search strategies")
        print("   • Dynamic Programming - Memoization, tabulation, optimization")
        
        # Category 3: System Design
        print("\n" + "─" * 70)
        print("📙 3. SYSTEM DESIGN")
        print("─" * 70)
        print("   • Scalability - Load balancing, caching, horizontal scaling")
        print("   • DB Design - Schema design, normalization, indexing")
        print("   • API Design - RESTful APIs, versioning, authentication")
        
        # Category 4: Behavioral
        print("\n" + "─" * 70)
        print("📕 4. BEHAVIORAL INTERVIEWS")
        print("─" * 70)
        print("   • STAR Method - Situation, Task, Action, Result framework")
        print("   • Leadership Principles - Team collaboration, decision making")
        
        print("\n" + "=" * 70)
        print("\n💡 Tip: Use the MCQ Quiz to practice these topics!")
        print("   Select relevant programming languages to test your knowledge.")
        
        print("\n" + "=" * 70)
        input("\nPress Enter to return to main menu...")
    
    def start_quiz(self):
        """Start a new MCQ quiz"""
        self.clear_screen()
        self.print_header()
        
        # Language selection
        print("\n📌 SELECT PROGRAMMING LANGUAGE")
        print("─" * 70)
        for i, lang in enumerate(self.LANGUAGES, 1):
            print(f"{i}. {lang}")
        print("─" * 70)
        
        lang_choice = input(f"\nEnter choice (1-{len(self.LANGUAGES)}): ").strip()
        try:
            language = self.LANGUAGES[int(lang_choice) - 1]
        except (ValueError, IndexError):
            print("\n❌ Invalid selection!")
            time.sleep(2)
            return
        
        # Difficulty selection
        print("\n📌 SELECT DIFFICULTY LEVEL")
        print("─" * 70)
        for i, diff in enumerate(self.DIFFICULTIES, 1):
            emoji = "🟢" if diff == "Easy" else "🟡" if diff == "Medium" else "🔴"
            print(f"{i}. {emoji} {diff}")
        print("─" * 70)
        
        diff_choice = input(f"\nEnter choice (1-{len(self.DIFFICULTIES)}): ").strip()
        try:
            difficulty = self.DIFFICULTIES[int(diff_choice) - 1]
        except (ValueError, IndexError):
            print("\n❌ Invalid selection!")
            time.sleep(2)
            return
        
        # Generate questions
        print(f"\n⏳ Generating {self.QUESTIONS_PER_QUIZ} {difficulty} questions for {language}...")
        print("   This may take a moment...\n")
        
        start_time = time.time()
        questions = generate_mcq_questions(language, difficulty, self.QUESTIONS_PER_QUIZ)
        
        if not questions:
            print("\n❌ Failed to generate questions. Please try again.")
            time.sleep(2)
            return
        
        # Run the quiz
        self.run_quiz(questions, language, difficulty, start_time)
    
    def run_quiz(self, questions: List[Dict], language: str, difficulty: str, start_time: float):
        """Execute the quiz with given questions"""
        self.user_answers = []
        correct_count = 0
        
        for i, q in enumerate(questions, 1):
            self.clear_screen()
            self.print_header()
            
            print(f"\n📝 Question {i}/{self.QUESTIONS_PER_QUIZ}")
            print("─" * 70)
            print(f"\n{q['question']}\n")
            
            # Display options
            for option, text in q['options'].items():
                print(f"  {option}. {text}")
            
            print("\n" + "─" * 70)
            
            # Get user answer
            while True:
                answer = input("\nYour answer (A/B/C/D): ").strip().upper()
                if answer in ['A', 'B', 'C', 'D']:
                    break
                print("❌ Invalid input! Please enter A, B, C, or D.")
            
            # Check answer
            is_correct = (answer == q['correct_answer'])
            if is_correct:
                correct_count += 1
            
            # Store answer
            self.user_answers.append({
                'question': q['question'],
                'options': q['options'],
                'user_answer': answer,
                'correct_answer': q['correct_answer'],
                'is_correct': is_correct,
                'explanation': q['explanation']
            })
        
        # Calculate time taken
        time_taken = int(time.time() - start_time)
        
        # Save results
        quiz_data = {
            'language': language,
            'difficulty': difficulty,
            'questions': self.user_answers
        }
        save_quiz_result(language, difficulty, correct_count, self.QUESTIONS_PER_QUIZ, quiz_data, time_taken)
        
        # Show results
        self.show_quiz_results(correct_count, language, difficulty, time_taken)
    
    def show_quiz_results(self, correct_count: int, language: str, difficulty: str, time_taken: int):
        """Display quiz results and detailed review"""
        self.clear_screen()
        self.print_header()
        
        score_percentage = (correct_count / self.QUESTIONS_PER_QUIZ) * 100
        
        print("\n" + "=" * 70)
        print("🎯 QUIZ COMPLETED!".center(70))
        print("=" * 70)
        print(f"\n📚 Language: {language}")
        print(f"⚡ Difficulty: {difficulty}")
        print(f"⏱️  Time Taken: {time_taken // 60}m {time_taken % 60}s")
        print(f"\n✅ Correct Answers: {correct_count}/{self.QUESTIONS_PER_QUIZ}")
        print(f"❌ Wrong Answers: {self.QUESTIONS_PER_QUIZ - correct_count}/{self.QUESTIONS_PER_QUIZ}")
        
        # Score display with emoji
        if score_percentage >= 80:
            emoji = "🏆"
            message = "Excellent!"
        elif score_percentage >= 60:
            emoji = "👍"
            message = "Good job!"
        elif score_percentage >= 40:
            emoji = "📚"
            message = "Keep practicing!"
        else:
            emoji = "💪"
            message = "Don't give up!"
        
        print(f"\n{emoji} SCORE: {score_percentage:.1f}% - {message}")
        print("=" * 70)
        
        # Ask if user wants detailed review
        print("\n")
        review = input("Would you like to review your answers? (y/n): ").strip().lower()
        
        if review == 'y':
            self.show_detailed_review()
        
        input("\n\nPress Enter to return to main menu...")
    
    def show_detailed_review(self):
        """Show detailed question-by-question review"""
        for i, answer_data in enumerate(self.user_answers, 1):
            self.clear_screen()
            self.print_header()
            
            print(f"\n📋 REVIEW - Question {i}/{self.QUESTIONS_PER_QUIZ}")
            print("=" * 70)
            print(f"\n{answer_data['question']}\n")
            
            # Show options with indicators
            for option, text in answer_data['options'].items():
                prefix = ""
                if option == answer_data['correct_answer']:
                    prefix = "✅ "
                elif option == answer_data['user_answer'] and not answer_data['is_correct']:
                    prefix = "❌ "
                else:
                    prefix = "   "
                print(f"{prefix}{option}. {text}")
            
            print("\n" + "─" * 70)
            
            if answer_data['is_correct']:
                print("\n🎉 Your answer is CORRECT!")
            else:
                print(f"\n❌ Your answer: {answer_data['user_answer']}")
                print(f"✅ Correct answer: {answer_data['correct_answer']}")
            
            print(f"\n💡 Explanation:")
            print(f"   {answer_data['explanation']}")
            
            print("\n" + "=" * 70)
            
            if i < len(self.user_answers):
                input("\nPress Enter for next question...")
    
    def view_analytics(self):
        """Display comprehensive analytics"""
        self.clear_screen()
        self.print_header()
        
        print("\n📊 PERFORMANCE ANALYTICS")
        print("=" * 70)
        
        # Overall analytics
        overall = get_overall_analytics()
        
        if overall['total_quizzes'] == 0:
            print("\n📭 No quiz data available yet.")
            print("   Complete some quizzes to see your analytics!\n")
            input("\nPress Enter to return to main menu...")
            return
        
        print(f"\n🎯 OVERALL PERFORMANCE")
        print("─" * 70)
        print(f"Total Quizzes Completed: {overall['total_quizzes']}")
        print(f"Average Score: {overall['avg_score']:.1f}%")
        print(f"Best Score: {overall['best_score']:.1f}%")
        print(f"Total Questions Attempted: {overall['total_questions']}")
        print(f"Overall Accuracy: {overall['accuracy']:.1f}%")
        
        # Analytics by language
        print(f"\n\n📚 PERFORMANCE BY LANGUAGE")
        print("─" * 70)
        lang_analytics = get_analytics_by_language()
        
        if lang_analytics:
            for lang_data in lang_analytics:
                print(f"\n{lang_data['language']}:")
                print(f"  Attempts: {lang_data['total_attempts']}")
                print(f"  Average Score: {lang_data['avg_score']:.1f}%")
        else:
            print("No language-specific data available.")
        
        # Analytics by difficulty
        print(f"\n\n⚡ PERFORMANCE BY DIFFICULTY")
        print("─" * 70)
        diff_analytics = get_analytics_by_difficulty()
        
        if diff_analytics:
            for diff_data in diff_analytics:
                emoji = "🟢" if diff_data['difficulty'] == "Easy" else "🟡" if diff_data['difficulty'] == "Medium" else "🔴"
                print(f"\n{emoji} {diff_data['difficulty']}:")
                print(f"  Attempts: {diff_data['total_attempts']}")
                print(f"  Average Score: {diff_data['avg_score']:.1f}%")
        else:
            print("No difficulty-specific data available.")
        
        print("\n" + "=" * 70)
        input("\nPress Enter to return to main menu...")
    
    def view_quiz_history(self):
        """Display recent quiz history"""
        self.clear_screen()
        self.print_header()
        
        print("\n📜 QUIZ HISTORY (Last 10 Attempts)")
        print("=" * 70)
        
        history = get_quiz_history(limit=10)
        
        if history.empty:
            print("\n📭 No quiz history available yet.\n")
        else:
            print(f"\n{'#':<4} {'Language':<12} {'Difficulty':<10} {'Score':<8} {'Date & Time':<20}")
            print("─" * 70)
            
            for idx, row in history.iterrows():
                score_str = f"{row['score_percentage']:.1f}%"
                timestamp = row['timestamp'][:16] if len(row['timestamp']) > 16 else row['timestamp']
                print(f"{idx+1:<4} {row['language']:<12} {row['difficulty']:<10} {score_str:<8} {timestamp:<20}")
        
        print("\n" + "=" * 70)
        input("\nPress Enter to return to main menu...")


# Streamlit Web Interface
def app():
    """Streamlit app interface for PrepMaster MCQ Quiz System"""
    import streamlit as st
    from src.llm_engine import generate_mcq_questions
    from src.database import (
        save_quiz_result,
        get_quiz_history,
        get_analytics_by_language,
        get_analytics_by_difficulty,
        get_overall_analytics
    )
    
    st.markdown("## 🎓 PrepMaster <span style='color:#4169E1; font-size:0.8em'>MCQ Quiz System</span>", unsafe_allow_html=True)
    
    # Initialize session state
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = None
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'quiz_language' not in st.session_state:
        st.session_state.quiz_language = None
    if 'quiz_difficulty' not in st.session_state:
        st.session_state.quiz_difficulty = None
    if 'quiz_start_time' not in st.session_state:
        st.session_state.quiz_start_time = None
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Study Roadmap", "🚀 MCQ Quiz", "📊 Analytics", "📜 History"])

    # --- TAB 1: STUDY ROADMAP ---
    with tab1:
        st.markdown("### 📚 Structured Preparation Plan")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **📘 1. Computer Science Fundamentals**
            
            • Arrays - Linear data structures, indexing, traversal
            
            • Trees - Binary trees, BST, traversal algorithms
            
            • Graphs - Representations, traversal, shortest paths
            
            • Hash Maps - Hash functions, collision handling
            """)
            
            st.warning("""
            **📙 3. System Design**
            
            • Scalability - Load balancing, caching, horizontal scaling
            
            • DB Design - Schema design, normalization, indexing
            
            • API Design - RESTful APIs, versioning, authentication
            """)
        
        with col2:
            st.success("""
            **📗 2. Algorithms**
            
            • Sorting - QuickSort, MergeSort, HeapSort, complexity
            
            • BFS/DFS - Breadth-first and depth-first search
            
            • Dynamic Programming - Memoization, tabulation
            """)
            
            st.error("""
            **📕 4. Behavioral Interviews**
            
            • STAR Method - Situation, Task, Action, Result
            
            • Leadership Principles - Team collaboration, decision making
            """)
        
        st.markdown("---")
        st.markdown("💡 **Tip:** Use the MCQ Quiz tab to practice these topics with programming questions!")

    # --- TAB 2: MCQ QUIZ ---
    with tab2:
        if not st.session_state.quiz_completed and st.session_state.quiz_questions is None:
            # Quiz Setup
            st.markdown("### 🎯 Start New Quiz")
            st.markdown("Select your programming language and difficulty level to begin!")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                language = st.selectbox(
                    "📌 Programming Language",
                    ["C", "C++", "Java", "JavaScript", "HTML", "CSS"],
                    key="lang_select"
                )
            
            with col_b:
                difficulty = st.selectbox(
                    "⚡ Difficulty Level",
                    ["Easy", "Medium", "Hard"],
                    key="diff_select"
                )
            
            st.markdown("---")
            
            if st.button("🚀 Generate Quiz (10 Questions)", use_container_width=True, type="primary"):
                with st.spinner(f"🤖 Generating {difficulty} questions for {language}... This may take a moment..."):
                    import time
                    st.session_state.quiz_start_time = time.time()
                    questions = generate_mcq_questions(language, difficulty, 10)
                    
                    if questions and len(questions) == 10:
                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_language = language
                        st.session_state.quiz_difficulty = difficulty
                        st.session_state.current_question_idx = 0
                        st.session_state.user_answers = []
                        st.session_state.quiz_completed = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to generate questions. Please try again.")
        
        elif st.session_state.quiz_questions and not st.session_state.quiz_completed:
            # Quiz In Progress
            questions = st.session_state.quiz_questions
            idx = st.session_state.current_question_idx
            
            # Progress bar
            progress = (idx) / len(questions)
            st.progress(progress, text=f"Question {idx + 1} of {len(questions)}")
            
            # Display current question
            q = questions[idx]
            st.markdown(f"### 📝 Question {idx + 1}")
            st.markdown("---")
            st.markdown(f"**{q['question']}**")
            st.markdown("")
            
            # Display options as radio buttons
            answer = st.radio(
                "Select your answer:",
                options=list(q['options'].keys()),
                format_func=lambda x: f"{x}. {q['options'][x]}",
                key=f"q_{idx}"
            )
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if idx > 0:
                    if st.button("⬅️ Previous", use_container_width=True):
                        st.session_state.current_question_idx -= 1
                        st.rerun()
            
            with col3:
                if answer:
                    if idx < len(questions) - 1:
                        if st.button("Next ➡️", use_container_width=True, type="primary"):
                            # Save answer
                            if len(st.session_state.user_answers) <= idx:
                                st.session_state.user_answers.append(answer)
                            else:
                                st.session_state.user_answers[idx] = answer
                            st.session_state.current_question_idx += 1
                            st.rerun()
                    else:
                        if st.button("✅ Submit Quiz", use_container_width=True, type="primary"):
                            # Save final answer
                            if len(st.session_state.user_answers) <= idx:
                                st.session_state.user_answers.append(answer)
                            else:
                                st.session_state.user_answers[idx] = answer
                            
                            # Calculate results
                            import time
                            correct_count = 0
                            for i, q in enumerate(questions):
                                if i < len(st.session_state.user_answers):
                                    if st.session_state.user_answers[i] == q['correct_answer']:
                                        correct_count += 1
                            
                            time_taken = int(time.time() - st.session_state.quiz_start_time)
                            
                            # Save to database
                            quiz_data = {
                                'language': st.session_state.quiz_language,
                                'difficulty': st.session_state.quiz_difficulty,
                                'questions': [
                                    {
                                        'question': q['question'],
                                        'user_answer': st.session_state.user_answers[i] if i < len(st.session_state.user_answers) else None,
                                        'correct_answer': q['correct_answer'],
                                        'is_correct': st.session_state.user_answers[i] == q['correct_answer'] if i < len(st.session_state.user_answers) else False,
                                        'explanation': q['explanation']
                                    }
                                    for i, q in enumerate(questions)
                                ]
                            }
                            
                            save_quiz_result(
                                st.session_state.quiz_language,
                                st.session_state.quiz_difficulty,
                                correct_count,
                                len(questions),
                                quiz_data,
                                time_taken
                            )
                            
                            st.session_state.quiz_completed = True
                            st.session_state.quiz_score = correct_count
                            st.rerun()
        
        elif st.session_state.quiz_completed:
            # Quiz Results
            questions = st.session_state.quiz_questions
            score = st.session_state.quiz_score
            total = len(questions)
            percentage = (score / total) * 100
            
            st.markdown("## 🎯 Quiz Completed!")
            st.markdown("---")
            
            # Score display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Language", st.session_state.quiz_language)
            with col2:
                st.metric("Difficulty", st.session_state.quiz_difficulty)
            with col3:
                st.metric("Score", f"{score}/{total}")
            with col4:
                st.metric("Percentage", f"{percentage:.1f}%")
            
            # Performance message
            if percentage >= 80:
                st.success("🏆 Excellent! You have a strong understanding of this topic!")
            elif percentage >= 60:
                st.info("👍 Good job! Keep practicing to improve further.")
            elif percentage >= 40:
                st.warning("📚 Keep practicing! Review the explanations below.")
            else:
                st.error("💪 Don't give up! Study the concepts and try again.")
            
            st.markdown("---")
            
            # Detailed Review
            st.markdown("### 📋 Detailed Review")
            
            for i, q in enumerate(questions):
                user_ans = st.session_state.user_answers[i] if i < len(st.session_state.user_answers) else None
                is_correct = user_ans == q['correct_answer']
                
                with st.expander(f"Question {i+1} - {'✅ Correct' if is_correct else '❌ Incorrect'}", expanded=not is_correct):
                    st.markdown(f"**{q['question']}**")
                    st.markdown("")
                    
                    for opt, text in q['options'].items():
                        if opt == q['correct_answer']:
                            st.success(f"✅ {opt}. {text} **(Correct Answer)**")
                        elif opt == user_ans and not is_correct:
                            st.error(f"❌ {opt}. {text} **(Your Answer)**")
                        else:
                            st.write(f"   {opt}. {text}")
                    
                    st.markdown("---")
                    st.markdown(f"**💡 Explanation:** {q['explanation']}")
            
            st.markdown("---")
            
            if st.button("🔄 Start New Quiz", use_container_width=True, type="primary"):
                st.session_state.quiz_questions = None
                st.session_state.current_question_idx = 0
                st.session_state.user_answers = []
                st.session_state.quiz_completed = False
                st.session_state.quiz_language = None
                st.session_state.quiz_difficulty = None
                st.rerun()

    # --- TAB 3: ANALYTICS ---
    with tab3:
        st.markdown("### 📊 Performance Analytics")
        
        overall = get_overall_analytics()
        
        if overall['total_quizzes'] == 0:
            st.info("📭 No quiz data available yet. Complete some quizzes to see your analytics!")
        else:
            # Overall Stats
            st.markdown("#### 🎯 Overall Performance")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Quizzes", overall['total_quizzes'])
            with col2:
                st.metric("Average Score", f"{overall['avg_score']:.1f}%")
            with col3:
                st.metric("Best Score", f"{overall['best_score']:.1f}%")
            with col4:
                st.metric("Accuracy", f"{overall['accuracy']:.1f}%")
            
            st.markdown("---")
            
            # Performance by Language
            st.markdown("#### 📚 Performance by Language")
            lang_analytics = get_analytics_by_language()
            
            if lang_analytics:
                import pandas as pd
                df_lang = pd.DataFrame(lang_analytics)
                st.dataframe(
                    df_lang[['language', 'total_attempts', 'avg_score']],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "language": "Language",
                        "total_attempts": "Attempts",
                        "avg_score": st.column_config.NumberColumn("Avg Score (%)", format="%.1f")
                    }
                )
            
            st.markdown("---")
            
            # Performance by Difficulty
            st.markdown("#### ⚡ Performance by Difficulty")
            diff_analytics = get_analytics_by_difficulty()
            
            if diff_analytics:
                import pandas as pd
                df_diff = pd.DataFrame(diff_analytics)
                
                col1, col2, col3 = st.columns(3)
                for i, row in enumerate(diff_analytics):
                    with [col1, col2, col3][i % 3]:
                        emoji = "🟢" if row['difficulty'] == "Easy" else "🟡" if row['difficulty'] == "Medium" else "🔴"
                        st.metric(
                            f"{emoji} {row['difficulty']}",
                            f"{row['avg_score']:.1f}%",
                            f"{row['total_attempts']} attempts"
                        )

    # --- TAB 4: HISTORY ---
    with tab4:
        st.markdown("### 📜 Quiz History")
        
        history = get_quiz_history(limit=20)
        
        if history.empty:
            st.info("📭 No quiz history available yet.")
        else:
            st.dataframe(
                history[['language', 'difficulty', 'score_percentage', 'timestamp']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "language": "Language",
                    "difficulty": "Difficulty",
                    "score_percentage": st.column_config.NumberColumn("Score (%)", format="%.1f"),
                    "timestamp": "Date & Time"
                }
            )


if __name__ == "__main__":
    # Run console version
    prep_master = PrepMaster()
    prep_master.run()

