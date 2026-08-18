import streamlit as st
import os
from dotenv import load_dotenv
from utils.extractor import extract_text_from_pdf
from utils.analyzer import analyze_resume

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .score-box {
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
    }
    .score-high   { background: #d4edda; color: #155724; }
    .score-medium { background: #fff3cd; color: #856404; }
    .score-low    { background: #f8d7da; color: #721c24; }
    .section-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    .keyword-chip {
        display: inline-block;
        background: #fee2e2;
        color: #991b1b;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .strength-chip {
        display: inline-block;
        background: #d1fae5;
        color: #065f46;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .bullet-original {
        background: #fff1f1;
        border-left: 3px solid #ef4444;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 6px;
        font-size: 0.9rem;
    }
    .bullet-improved {
        background: #f0fdf4;
        border-left: 3px solid #22c55e;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.9rem;
    }
    .divider { margin: 2rem 0; border-top: 1px solid #e5e7eb; }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 10px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🎯 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Google Gemini · Paste a job description, upload your resume, get instant ATS feedback</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Configuration")

try:
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
except Exception:
    api_key = os.getenv("GEMINI_API_KEY", None)

if not api_key:
    api_key = st.sidebar.text_input(
        "Google Gemini API Key",
        type="password",
        help="Get your FREE key at aistudio.google.com",
        placeholder="AIza..."
    )

st.sidebar.markdown("🔑 **Get free API key:** [aistudio.google.com](https://aistudio.google.com/app/apikey)")

selected_model = st.sidebar.selectbox(
    "🤖 Model",
    options=[
        "gemini-3.6-flash",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
    ],
    index=0,
    help="gemini-3.6-flash is the latest free and fast model."
)
st.sidebar.caption("✅ gemini-3.6-flash: FREE · Latest model")

if not api_key:
    st.info("👈 Enter your Gemini API key in the sidebar. It's completely free at [aistudio.google.com](https://aistudio.google.com/app/apikey)")

# ── Input Section ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume as PDF",
        type=["pdf"],
        help="Only PDF format is supported"
    )
    if uploaded_file:
        st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")

with col2:
    st.subheader("💼 Job Description")
    job_description = st.text_area(
        "Paste the full job description here",
        height=200,
        placeholder="Paste the job posting here — include required skills, responsibilities, and qualifications..."
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Analyze Button ─────────────────────────────────────────────────────────────
analyze_clicked = st.button("🚀 Analyze My Resume", use_container_width=True)

# ── Analysis Logic ─────────────────────────────────────────────────────────────
if analyze_clicked:
    if not api_key:
        st.error("❌ Please provide your Gemini API key in the sidebar.")
    elif not uploaded_file:
        st.error("❌ Please upload your resume PDF.")
    elif not job_description.strip():
        st.error("❌ Please paste the job description.")
    else:
        with st.spinner("🔍 Extracting resume text..."):
            try:
                resume_text = extract_text_from_pdf(uploaded_file)
                if not resume_text:
                    st.error("❌ Could not extract text from your PDF. Make sure it's not a scanned image.")
                    st.stop()
            except Exception as e:
                st.error(f"❌ Error reading PDF: {e}")
                st.stop()

        with st.spinner(f"🤖 Analyzing with {selected_model}... (usually takes 5-10 seconds)"):
            try:
                result = analyze_resume(resume_text, job_description, api_key, model=selected_model)
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                st.stop()

        # ── Results ───────────────────────────────────────────────────────────
        st.markdown("## 📊 Analysis Results")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        score = result.get("match_score", 0)
        score_class = "score-high" if score >= 70 else ("score-medium" if score >= 45 else "score-low")
        score_emoji = "🟢" if score >= 70 else ("🟡" if score >= 45 else "🔴")

        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.markdown(
                f'<div class="score-box {score_class}">{score_emoji} {score}/100<br>'
                f'<span style="font-size:1rem;font-weight:400">{result.get("score_reason","")}</span></div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        left, right = st.columns(2, gap="large")

        with left:
            st.markdown("### ✅ Strengths")
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            for s in result.get("strengths", []):
                st.markdown(f'<span class="strength-chip">✓ {s}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown("### 🚨 Missing Keywords")
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            for kw in result.get("missing_keywords", []):
                st.markdown(f'<span class="keyword-chip">✗ {kw}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown("### ⚠️ Areas to Improve")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        for w in result.get("weak_areas", []):
            st.markdown(f"• {w}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown("### ✍️ Rewritten Bullet Points")
        st.caption("Your original bullets → AI-improved versions with stronger action verbs and measurable impact")
        for i, bullet in enumerate(result.get("rewritten_bullets", []), 1):
            with st.expander(f"Bullet #{i} — click to expand", expanded=True):
                st.markdown(f'<div class="bullet-original">🔴 <strong>Original:</strong> {bullet.get("original","")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="bullet-improved">🟢 <strong>Improved:</strong> {bullet.get("improved","")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown("### 💡 Overall Advice")
        st.info(result.get("overall_advice", ""))

        # ── Download Report ────────────────────────────────────────────────────
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📥 Download Your Report")

        report_lines = [
            "AI RESUME ANALYSIS REPORT",
            "=" * 50,
            f"Match Score: {score}/100",
            f"Score Reason: {result.get('score_reason','')}",
            "", "STRENGTHS", "-" * 30,
        ]
        for s in result.get("strengths", []):
            report_lines.append(f"  • {s}")
        report_lines += ["", "MISSING KEYWORDS", "-" * 30]
        for kw in result.get("missing_keywords", []):
            report_lines.append(f"  • {kw}")
        report_lines += ["", "AREAS TO IMPROVE", "-" * 30]
        for w in result.get("weak_areas", []):
            report_lines.append(f"  • {w}")
        report_lines += ["", "REWRITTEN BULLETS", "-" * 30]
        for b in result.get("rewritten_bullets", []):
            report_lines.append(f"  Original:  {b.get('original','')}")
            report_lines.append(f"  Improved:  {b.get('improved','')}")
            report_lines.append("")
        report_lines += ["OVERALL ADVICE", "-" * 30, result.get("overall_advice", "")]
        report_text = "\n".join(report_lines)

        st.download_button(
            label="⬇️ Download Report as .txt",
            data=report_text,
            file_name="resume_analysis_report.txt",
            mime="text/plain",
        )