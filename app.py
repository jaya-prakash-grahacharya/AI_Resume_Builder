import streamlit as st
import google.generativeai as genai
from markdown_pdf import MarkdownPdf, Section
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="AI Resume Builder", page_icon="📄")

# --- GET API KEY (Works on Hugging Face & Streamlit Cloud) ---
# We look for the key in the "Environment Variables"
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    # If the key is missing, check Streamlit secrets (backup)
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.error("⚠️ API Key not found! Please set 'GOOGLE_API_KEY' in your Environment Variables.")
        st.stop()

# --- MAIN PAGE ---
st.title("🚀 AI Resume Builder")
st.markdown("Enter your details below to generate a professional resume.")
st.caption("Free to use! (Powered by Google Gemini)")

with st.form("resume_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="Jane Doe")
        email = st.text_input("Email", placeholder="jane@example.com")
    with col2:
        phone = st.text_input("Phone", placeholder="+1 234 567 890")
        linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/jane")

    st.subheader("🎓 Education")
    education = st.text_area("University, Degree, Year, GPA", 
                             placeholder="Example: B.Tech in CS, Mumbai University, 2024")

    st.subheader("📝 Skills & Experience")
    skills = st.text_area("Top Skills", placeholder="Python, SQL, Communication...")
    experience = st.text_area("Experience (Optional for Freshers)", height=150, 
                              placeholder="Leave blank if you are a fresher.")
    
    submitted = st.form_submit_button("✨ Generate Resume")

# --- THE AI BRAIN ---
if submitted:
    if not name or not skills or not education:
        st.warning("⚠️ Please fill in Name, Education, and Skills.")
    else:
        with st.spinner("AI is writing your resume..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')

                prompt = f"""
                You are an expert resume writer. Create a professional resume for:
                Name: {name} | Contact: {email}, {phone}, {linkedin}
                
                EDUCATION: {education}
                SKILLS: {skills}
                EXPERIENCE: {experience if experience else "NO EXPERIENCE - User is a fresher"}
                
                STRICT INSTRUCTIONS:
                1. If experience is missing, focus heavily on Education and Skills.
                2. Format cleanly in Markdown.
                """

                response = model.generate_content(prompt)
                resume_content = response.text

                st.success("Resume Generated!")
                st.markdown(resume_content)

                # PDF Generation
                pdf = MarkdownPdf(toc_level=2)
                pdf.add_section(Section(resume_content))
                pdf.meta["title"] = f"Resume - {name}"
                pdf.save("resume.pdf")

                with open("resume.pdf", "rb") as f:
                    st.download_button("⬇️ Download PDF", f, f"{name}_Resume.pdf")

            except Exception as e:
                st.error(f"Error: {e}")
