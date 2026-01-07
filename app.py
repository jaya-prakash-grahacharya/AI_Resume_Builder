import streamlit as st
import google.generativeai as genai
from markdown_pdf import MarkdownPdf, Section

# --- CONFIGURATION ---
st.set_page_config(page_title="AI Resume Builder", page_icon="📄")

# --- SIDEBAR: API KEY ---
st.sidebar.header("🔐 Setup")
st.sidebar.markdown("Get your free key [here](https://aistudio.google.com/app/apikey)")
api_key_input = st.sidebar.text_input("Enter your Google API Key", type="password")
api_key = api_key_input.strip() if api_key_input else None

# --- MAIN PAGE: USER INPUTS ---
st.title("🚀 AI Resume & Portfolio Builder")
st.markdown("Enter your details below. **Experience is optional** for freshers!")

with st.form("resume_form"):
    # Personal Info
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="Jane Doe")
        email = st.text_input("Email", placeholder="jane@example.com")
    with col2:
        phone = st.text_input("Phone", placeholder="+1 234 567 890")
        linkedin = st.text_input("LinkedIn/Portfolio URL", placeholder="linkedin.com/in/jane")

    # Education (Critical for Freshers)
    st.subheader("🎓 Education")
    education = st.text_area("University, Degree, Year, GPA", 
                             placeholder="Example: B.Tech in Computer Science, Mumbai University, 2024. CGPA: 9.0")

    # The "Meat" of the resume
    st.subheader("📝 Experience & Skills")
    skills = st.text_area("Top Skills (comma separated)", placeholder="Python, Data Analysis, Team Leadership...")
    
    # Experience is now clearly marked as optional
    experience = st.text_area("Work/Project Experience (Optional for Freshers)", height=150, 
                              placeholder="If you have no jobs, describe college projects or leave blank!")
    
    # Submission Button
    submitted = st.form_submit_button("✨ Generate Resume")

# --- THE AI BRAIN ---
if submitted:
    # 1. SAFETY CHECK: Name, Skills and Education are mandatory. Experience is NOT.
    if not api_key:
        st.error("❌ Please enter your Google API Key in the sidebar!")
    elif not name or not skills or not education:
        st.warning("⚠️ Please fill in your Name, Education, and Skills. Experience is optional.")
    else:
        with st.spinner("AI is writing your resume..."):
            try:
                # 2. Configure Google AI
                genai.configure(api_key=api_key)
                
                # Use the stable model
                model = genai.GenerativeModel('gemini-flash-latest')

                # 3. Craft the Prompt (Updated for Freshers)
                prompt = f"""
                You are an expert resume writer. Create a professional resume for:
                Name: {name}
                Contact: {email} | {phone} | {linkedin}
                
                EDUCATION: {education}
                SKILLS: {skills}
                EXPERIENCE: {experience if experience else "NO EXPERIENCE - User is a fresher"}
                
                STRICT INSTRUCTIONS:
                1. Write a 'Professional Summary' based on the skills and education.
                2. IMPORTANT: If 'EXPERIENCE' is empty or says 'NO EXPERIENCE', focus heavily on the Education and Skills section. Highlight academic achievements.
                3. If experience IS provided, rewrite it to be action-oriented.
                4. Format the output cleanly in Markdown (Use ## for headers).
                """

                # 4. Call Google Gemini
                response = model.generate_content(prompt)
                resume_content = response.text

                # 5. Display Result
                st.success("Resume Generated!")
                st.markdown("### Preview:")
                st.markdown(resume_content)

                # 6. PDF Generation
                pdf = MarkdownPdf(toc_level=2)
                pdf.add_section(Section(resume_content))
                pdf.meta["title"] = f"Resume - {name}"
                
                pdf_filename = "resume.pdf"
                pdf.save(pdf_filename)

                with open(pdf_filename, "rb") as f:
                    pdf_data = f.read()

                # 7. Download Button
                st.download_button(
                    label="⬇️ Download PDF Resume",
                    data=pdf_data,
                    file_name=f"{name}_Resume.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
