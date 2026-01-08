# 🚀 AI Resume & Portfolio Builder

A full-stack AI application that generates professional, ATS-friendly resumes in seconds. Built with **Python**, **Streamlit**, and **Google Gemini AI**.

🔗 **Live Demo:** [Click here to use the App](https://huggingface.co/spaces/JayaPrakash4065/AI_Resume_Builder)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini-4285F4)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)

---

## 📖 About The Project

Writing a resume from scratch is difficult, especially for freshers. This tool uses **Generative AI** to take raw user details (education, skills, rough experience) and transforms them into a professional, polished resume.

**Key Features:**
* ✨ **AI-Powered Writing:** Uses Google's Gemini Pro model to write professional summaries and bullet points.
* 🎓 **Fresher Friendly:** Automatically detects if a user has no experience and highlights Education/Projects instead.
* 📄 **PDF Export:** Generates a clean, downloadable PDF resume instantly.
* 🔒 **Secure:** API keys are handled safely via Environment Variables or Streamlit Secrets.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **LLM (Brain):** Google Gemini API (`gemini-flash-latest`)
* **PDF Generation:** `markdown-pdf`
* **Deployment:** Docker & Hugging Face Spaces

---

## 💻 How to Run Locally

Follow these steps to run the project on your own computer.

### 1. Clone the Repository
```bash
git clone [https://github.com/jaya-prakash-grahacharya/AI_Resume.git](https://github.com/jaya-prakash-grahacharya/AI_Resume.git)
cd AI_Resume
