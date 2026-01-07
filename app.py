import streamlit as st
import google.generativeai as genai
from markdown_pdf import MarkdownPdf, Section

# --- CONFIGURATION ---
st.set_page_config(page_title="AI Resume Builder", page_icon="📄")

# --- SIDEBAR: API KEY ---
st.sidebar.header("🔐 Setup")
st.sidebar.markdown("Get your free key [here](https://aistudio.google.com/app/apikey)")
api_key = st.sidebar.text_input("Enter your Google API Key", type="password")

# --- MAIN PAGE: USER INPUTS ---
st.title("🚀 AI Resume & Portfolio Builder")
st.markdown("Enter your details below, and let AI build a professional resume for you (Free Version).")

with st.form("resume_form"):
    # Personal Info
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="Jane Doe")
        email = st.text_input("Email", placeholder="jane@example.com")
    with col2:
        phone = st.text_input("Phone", placeholder="+1 234 567 890")
        linkedin = st.text_input("LinkedIn/Portfolio URL", placeholder="linkedin.com/in/jane")

    # The "Meat" of the resume
    st.subheader("📝 Experience & Skills")
    skills = st.text_area("Top Skills (comma separated)", placeholder="Python, Data Analysis, Team Leadership...")
    experience = st.text_area("Work/Project Experience", height=150, 
                              placeholder="Describe your internships, projects, or past jobs loosely here. The AI will polish it.")
    
    # Submission Button
    submitted = st.form_submit_button("✨ Generate Resume")

# --- THE AI BRAIN (GOOGLE GEMINI) ---
if submitted:
    if not api_key:
        st.error("Please enter your Google API Key in the sidebar first!")
    else:
        with st.spinner("AI is writing your resume..."):
            try:
                # 1. Configure Google AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')

                # 2. Craft the Prompt
                prompt = f"""
                You are an expert resume writer. Create a professional resume for:
                Name: {name}
                Contact: {email} | {phone} | {linkedin}
                
                Skills: {skills}
                Experience/Projects: {experience}
                
                STRICT INSTRUCTIONS:
                1. Write a 'Professional Summary' based on the skills.
                2. Improve the experience descriptions to be action-oriented (use words like 'Spearheaded', 'Developed').
                3. Format the output cleanly in Markdown.
                """

                # 3. Call Google Gemini
                response = model.generate_content(prompt)
                resume_content = response.text

                # 4. Display Result
                st.success("Resume Generated!")
                st.markdown("### Preview:")
                st.markdown(resume_content)

                # 5. PDF Generation
                pdf = MarkdownPdf(toc_level=2)
                pdf.add_section(Section(resume_content))
                pdf.meta["title"] = f"Resume - {name}"
                
                pdf_output = pdf.output()

                # 6. Download Button
                st.download_button(
                    label="⬇️ Download PDF Resume",
                    data=pdf_output,
                    file_name=f"{name}_Resume.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")