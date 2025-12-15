import streamlit as st
from src.database import save_candidate_profile
from src.llm_engine import generate_tech_questions

def app():
    st.markdown("## 🤖 TalentScout <span style='color:#4169E1; font-size:0.8em'>Automated Screener</span>", unsafe_allow_html=True)
    st.caption("I will collect your details and ask technical questions based on your stack.")

    # Initialize State
    if "recruiter_step" not in st.session_state:
        st.session_state.recruiter_step = 0
        st.session_state.candidate_data = {}
        st.session_state.recruiter_history = []
        # Initial greeting
        st.session_state.recruiter_history.append({"role": "ai", "content": "Hello! I am TalentScout. Let's start. What is your Full Name?"})

    # Render Chat History
    for msg in st.session_state.recruiter_history:
        role = "assistant" if msg['role'] == 'ai' else "user"
        with st.chat_message(role):
            st.write(msg['content'])

    # Define the linear flow of questions
    # Key = Field to store, Question = What to ask NEXT
    info_flow = [
        ("full_name", "Thank you. What is your Email Address?"),
        ("email", "Great. What Position are you applying for?"),
        ("position", "Understood. Please list your Tech Stack (languages, frameworks)."),
        ("tech_stack", "Analyzing your stack..."), # This triggers the tech round
    ]

    step = st.session_state.recruiter_step
    
    # Input Area
    if step < 100: # 100 = Finished state
        user_input = st.chat_input("Type your answer here...")
        
        if user_input:
            # 1. Add User Message
            st.session_state.recruiter_history.append({"role": "user", "content": user_input})
            
            # 2. Process Info Gathering
            if step < len(info_flow):
                current_key = info_flow[step][0] # e.g., "full_name" is being answered now (actually logic is slightly offset, handled below)
                
                # Logic: The user just answered the question for step 'step'
                # We need to map inputs correctly. 
                # Let's use a simpler mapping based on index.
                keys = ["full_name", "email", "position", "tech_stack"]
                if step < len(keys):
                    st.session_state.candidate_data[keys[step]] = user_input
                
                # Move to next step
                st.session_state.recruiter_step += 1
                next_step = st.session_state.recruiter_step
                
                # Ask next question or trigger tech round
                if next_step < len(info_flow):
                    next_q = info_flow[step][1] # Ask the question defined in the tuple
                    st.session_state.recruiter_history.append({"role": "ai", "content": next_q})
                else:
                    # Trigger Tech Round
                    stack = st.session_state.candidate_data.get('tech_stack')
                    with st.spinner("Generating questions with Gemini AI..."):
                        tech_qs = generate_tech_questions(stack)
                    
                    st.session_state.tech_questions = tech_qs
                    st.session_state.current_tech_q = 0
                    
                    st.session_state.recruiter_history.append({"role": "ai", "content": f"I have generated {len(tech_qs)} technical questions based on {stack}."})
                    st.session_state.recruiter_history.append({"role": "ai", "content": f"Q1: {tech_qs[0]}"})
                    
                    # Set a specific state for tech round
                    st.session_state.recruiter_step = 50 

            # 3. Process Technical Round
            elif step == 50:
                # User answered a technical question
                q_idx = st.session_state.current_tech_q
                questions = st.session_state.tech_questions
                
                # Save answer (in memory for now)
                # In a real app, we'd store specific Q&A pairs
                
                q_idx += 1
                st.session_state.current_tech_q = q_idx
                
                if q_idx < len(questions):
                    next_q = questions[q_idx]
                    st.session_state.recruiter_history.append({"role": "ai", "content": f"Q{q_idx+1}: {next_q}"})
                else:
                    st.session_state.recruiter_history.append({"role": "ai", "content": "Thank you! That concludes the screening. Your profile has been saved."})
                    save_candidate_profile(st.session_state.candidate_data, st.session_state.recruiter_history)
                    st.session_state.recruiter_step = 100 # Done

            st.rerun()