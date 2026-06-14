import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os


# LOAD API KEY


load_dotenv("key.env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# PAGE SETTINGS

st.set_page_config(
    page_title="CampusCopilot AI",
    page_icon="🎓",
    layout="centered"
)


# TITLE


st.title("🎓 CampusCopilot AI")
st.subheader("Your AI-Powered Student Success Assistant")

st.info(
    "Get help with studies, coding, careers, productivity, "
    "and skill development."
)


# SIDEBAR


with st.sidebar:

    st.header("🎯 Select Assistant Mode")

    mode = st.selectbox(
        "Choose a specialization:",
        [
            "Study Assistant",
            "Coding Mentor",
            "Career Coach",
            "Productivity Mentor"
        ]
    )

    st.divider()

    st.header("📌 Features")

    st.write("""
✅ Study Help  
✅ Coding Guidance  
✅ Career Advice  
✅ Productivity Help  
✅ Skill Development  
""")

    st.divider()

    st.header("⚙️ Tech Stack")

    st.write("""
- Python  
- Streamlit  
- Groq API  
- Llama 3 (via Groq)
""")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()



# PROMPTS


prompts = {

    "Study Assistant": """
You are ONLY a Study Assistant.

ONLY help with:
- academics
- study plans
- exam preparation
- concept explanations
- school/college subjects
- learning strategies

STRICT RULE:
Coding, Python, careers, internships, jobs, and productivity are NOT allowed.

If unrelated:
Reply ONLY:
I only help with studies, academics, and exam preparation.
""",

    "Coding Mentor": """
You are ONLY a Coding Mentor.

ONLY help with:
- Python
- programming
- debugging
- coding roadmap
- web development
- DSA

STRICT RULE:
Study, career, and productivity questions are NOT allowed.

If unrelated:
Reply ONLY:
I only help with coding and programming-related questions.
""",

    "Career Coach": """
You are ONLY a Career Coach.

ONLY help with:
- careers after 10th/12th
- engineering branches
- internships
- resumes
- skill development
- jobs
- college decisions

STRICT RULE:
Coding tutorials, study questions, and productivity questions are NOT allowed.

If unrelated:
Reply ONLY:
I only help with career and skill development questions.
""",

    "Productivity Mentor": """
You are ONLY a Productivity Mentor.

ONLY help with:
- procrastination
- focus
- discipline
- habits
- time management

STRICT RULE:
Study, coding, and career questions are NOT allowed.

If unrelated:
Reply ONLY:
I only help with productivity and self-improvement questions.
"""
}


# CHAT HISTORY


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# USER INPUT


prompt = st.chat_input("Ask your question...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": prompts[mode]
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_tokens=200
                )

                reply = completion.choices[0].message.content

            except Exception:
                reply = "Something went wrong. Please try again."

            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })