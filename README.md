# 🎯 AI Resume Analyzer

An intelligent resume analysis tool that scores your resume against any job description, identifies missing ATS keywords, highlights weaknesses, and rewrites your bullet points using **Google Gemini AI**.

Built as a portfolio project to demonstrate full-stack AI development skills.

---

## 🚀 Live Demo
👉 **[Try it here](https://your-app-name.streamlit.app)** ← *(update this link after deployment)*

---

## 📸 Preview

> Upload your resume PDF + paste a job description → get instant AI feedback

---

## ✨ Features

- 📄 **PDF Resume Parsing** — extracts text from any PDF resume
- 🎯 **ATS Match Score** — rates your resume 0–100 against the job description
- ✅ **Strengths Detection** — highlights what you're doing right
- 🚨 **Missing Keywords** — shows exactly what keywords ATS systems are looking for
- ⚠️ **Weak Areas** — identifies gaps in your resume
- ✍️ **Bullet Point Rewriter** — rewrites your bullets with stronger action verbs and measurable impact
- 📥 **Downloadable Report** — download your full analysis as a `.txt` file
- 🤖 **Model Selector** — switch between Gemini models from the sidebar

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend + Backend | Python, Streamlit |
| AI / LLM | Google Gemini API (`gemini-3.6-flash`) |
| PDF Parsing | pypdf |
| Deployment | Streamlit Cloud |

---

## ⚙️ Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/MehXarii/resume-analyzer.git
cd resume-analyzer
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your API key**

Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get your free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)

**4. Run the app**
```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## 📁 Project Structure

```
resume-analyzer/
│
├── app.py                  # Main Streamlit application
├── utils/
│   ├── extractor.py        # PDF text extraction
│   └── analyzer.py         # Google Gemini AI logic
├── requirements.txt
├── .env                    # API key (not pushed to GitHub)
└── .gitignore
```

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key (free at aistudio.google.com) |

For Streamlit Cloud deployment, add this under **App Settings → Secrets**.

---

## 👩‍💻 Author

**Mehak Ansari**
- GitHub: [@MehXarii](https://github.com/MehXarii)
- LinkedIn: [linkedin.com/in/mehak-ansari](https://linkedin.com/in/mehak-ansari) ← *(update with your actual LinkedIn URL)*

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
