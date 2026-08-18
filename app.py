import streamlit as st
import os
from dotenv import load_dotenv
from utils.extractor import extract_text_from_pdf
from utils.analyzer import analyze_resume

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header ── */
    .header-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 18px;
        padding: 2.2rem 0 0.4rem 0;
    }
    .logo-circle {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 4px 18px rgba(102,126,234,0.35);
    }
    .logo-circle svg {
        width: 28px;
        height: 28px;
        stroke: #fff;
        fill: none;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0.3rem 0 1.8rem 0;
        letter-spacing: 0.01em;
    }

    /* ── Divider ── */
    .divider { margin: 1.8rem 0; border-top: 1px solid #e2e8f0; }

    /* ── Section headers ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .section-header svg {
        width: 18px;
        height: 18px;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
        flex-shrink: 0;
    }

    /* ── Score card ── */
    .score-wrap {
        border-radius: 16px;
        padding: 28px 24px 20px 24px;
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid transparent;
    }
    .score-high   { background: #f0fdf4; border-color: #bbf7d0; }
    .score-medium { background: #fffbeb; border-color: #fde68a; }
    .score-low    { background: #fff1f2; border-color: #fecdd3; }

    .score-number {
        font-size: 3.8rem;
        font-weight: 900;
        line-height: 1;
        letter-spacing: -2px;
    }
    .score-high   .score-number { color: #16a34a; }
    .score-medium .score-number { color: #d97706; }
    .score-low    .score-number { color: #dc2626; }

    .score-label {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 8px;
        line-height: 1.5;
    }
    .score-bar-bg {
        background: #e2e8f0;
        border-radius: 999px;
        height: 8px;
        margin: 14px 0 0 0;
        overflow: hidden;
    }
    .score-bar-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.6s ease;
    }
    .score-high   .score-bar-fill { background: #16a34a; }
    .score-medium .score-bar-fill { background: #d97706; }
    .score-low    .score-bar-fill { background: #dc2626; }

    /* ── Section cards ── */
    .card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 1rem;
    }

    /* ── Chips ── */
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        border-radius: 6px;
        padding: 5px 12px;
        margin: 3px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .chip-green { background: #dcfce7; color: #15803d; }
    .chip-red   { background: #fee2e2; color: #b91c1c; }
    .chip-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        display: inline-block;
        flex-shrink: 0;
    }
    .chip-green .chip-dot { background: #16a34a; }
    .chip-red   .chip-dot { background: #dc2626; }

    /* ── Bullet comparison ── */
    .bullet-block { margin-bottom: 14px; }
    .bullet-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }
    .bullet-original-label { color: #dc2626; }
    .bullet-improved-label { color: #16a34a; }
    .bullet-text {
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 0.9rem;
        line-height: 1.55;
        color: #1e293b;
    }
    .bullet-text-original { background: #fff1f2; border-left: 3px solid #fca5a5; }
    .bullet-text-improved { background: #f0fdf4; border-left: 3px solid #86efac; }

    /* ── Weak area list ── */
    .weak-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.9rem;
        color: #334155;
        line-height: 1.5;
    }
    .weak-item:last-child { border-bottom: none; }
    .weak-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #f59e0b;
        flex-shrink: 0;
        margin-top: 6px;
    }

    /* ── Advice card ── */
    .advice-card {
        background: linear-gradient(135deg, #ede9fe 0%, #dbeafe 100%);
        border: 1px solid #c4b5fd;
        border-radius: 12px;
        padding: 18px 20px;
        font-size: 0.93rem;
        color: #1e1b4b;
        line-height: 1.65;
    }

    /* ── Button ── */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        letter-spacing: 0.02em;
        box-shadow: 0 4px 14px rgba(102,126,234,0.3);
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.92; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.5rem 0 1.2rem 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 1.2rem;
    }
    .sidebar-logo-circle {
        width: 34px; height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .sidebar-logo-circle svg {
        width: 16px; height: 16px;
        stroke: #fff; fill: none;
        stroke-width: 2.2;
        stroke-linecap: round; stroke-linejoin: round;
    }
    .sidebar-logo-text {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1.2;
    }
    .sidebar-logo-sub {
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 400;
    }

    /* ── Input labels ── */
    .input-label {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 8px;
    }
    .input-label svg {
        width: 15px; height: 15px;
        stroke: #667eea;
        fill: none;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    /* ── Results header ── */
    .results-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.01em;
        margin-bottom: 0;
    }
    .results-sub {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-top: 2px;
    }

    /* hide streamlit default header branding */
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
  <div class="logo-circle">
    <svg viewBox="0 0 24 24">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14 2 14 8 20 8"/>
      <line x1="16" y1="13" x2="8" y2="13"/>
      <line x1="16" y1="17" x2="8" y2="17"/>
      <polyline points="10 9 9 9 8 9"/>
    </svg>
  </div>
  <h1 class="main-title">AI Resume Analyzer</h1>
</div>
<p class="subtitle">Powered by Google Gemini &nbsp;·&nbsp; ATS scoring, keyword analysis &amp; bullet point rewrites</p>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div class="sidebar-logo">
  <div class="sidebar-logo-circle">
    <svg viewBox="0 0 24 24">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14 2 14 8 20 8"/>
      <line x1="16" y1="13" x2="8" y2="13"/>
    </svg>
  </div>
  <div>
    <div class="sidebar-logo-text">Resume Analyzer</div>
    <div class="sidebar-logo-sub">AI-Powered · Free</div>
  </div>
</div>
""", unsafe_allow_html=True)

try:
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
except Exception:
    api_key = os.getenv("GEMINI_API_KEY", None)

if not api_key:
    st.sidebar.markdown("**Gemini API Key**")
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        help="Get your free key at aistudio.google.com",
        placeholder="AIza...",
        label_visibility="collapsed"
    )
    st.sidebar.caption("Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)")

st.sidebar.markdown("---")
st.sidebar.markdown("**Model**")
selected_model = st.sidebar.selectbox(
    "Model",
    options=[
        "gemini-3.6-flash",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
    ],
    index=0,
    label_visibility="collapsed"
)
st.sidebar.caption("gemini-3.6-flash — free & fast")

if not api_key:
    st.info("Enter your Gemini API key in the sidebar to get started. Free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)")

# ── Input Section ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="input-label">
      <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
      Resume PDF
    </div>""", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"**{uploaded_file.name}** uploaded successfully")

with col2:
    st.markdown("""
    <div class="input-label">
      <svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
      Job Description
    </div>""", unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description",
        height=200,
        placeholder="Paste the full job posting here — required skills, responsibilities, qualifications...",
        label_visibility="collapsed"
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Analyze Button ─────────────────────────────────────────────────────────────
analyze_clicked = st.button("Analyze My Resume", use_container_width=True)

# ── Analysis Logic ─────────────────────────────────────────────────────────────
if analyze_clicked:
    if not api_key:
        st.error("Please provide your Gemini API key in the sidebar.")
    elif not uploaded_file:
        st.error("Please upload your resume PDF.")
    elif not job_description.strip():
        st.error("Please paste the job description.")
    else:
        with st.spinner("Extracting resume text..."):
            try:
                resume_text = extract_text_from_pdf(uploaded_file)
                if not resume_text:
                    st.error("Could not extract text from your PDF. Make sure it is not a scanned image.")
                    st.stop()
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
                st.stop()

        with st.spinner(f"Analyzing with {selected_model}..."):
            try:
                result = analyze_resume(resume_text, job_description, api_key, model=selected_model)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()

        # ── Results Header ─────────────────────────────────────────────────────
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="results-header">Analysis Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="results-sub">Based on your resume vs the provided job description</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Score ──────────────────────────────────────────────────────────────
        score = result.get("match_score", 0)
        score_class = "score-high" if score >= 70 else ("score-medium" if score >= 45 else "score-low")
        score_label = "Strong Match" if score >= 70 else ("Moderate Match" if score >= 45 else "Weak Match")

        c1, c2, c3 = st.columns([1, 1.2, 1])
        with c2:
            st.markdown(f"""
            <div class="score-wrap {score_class}">
              <div class="score-number">{score}<span style="font-size:1.4rem;font-weight:600;color:#94a3b8">/100</span></div>
              <div class="score-label"><strong>{score_label}</strong><br>{result.get("score_reason","")}</div>
              <div class="score-bar-bg">
                <div class="score-bar-fill" style="width:{score}%"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Strengths + Missing Keywords ───────────────────────────────────────
        left, right = st.columns(2, gap="large")

        with left:
            st.markdown("""
            <div class="section-header">
              <svg viewBox="0 0 24 24" stroke="#16a34a" fill="none"><polyline points="20 6 9 17 4 12"/></svg>
              Strengths
            </div>""", unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            chips = "".join([
                f'<span class="chip chip-green"><span class="chip-dot"></span>{s}</span>'
                for s in result.get("strengths", [])
            ])
            st.markdown(chips, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown("""
            <div class="section-header">
              <svg viewBox="0 0 24 24" stroke="#dc2626" fill="none"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              Missing Keywords
            </div>""", unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            chips = "".join([
                f'<span class="chip chip-red"><span class="chip-dot"></span>{kw}</span>'
                for kw in result.get("missing_keywords", [])
            ])
            st.markdown(chips, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Weak Areas ─────────────────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
          <svg viewBox="0 0 24 24" stroke="#d97706" fill="none"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          Areas to Improve
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        items = "".join([
            f'<div class="weak-item"><span class="weak-dot"></span>{w}</div>'
            for w in result.get("weak_areas", [])
        ])
        st.markdown(items, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Rewritten Bullets ──────────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
          <svg viewBox="0 0 24 24" stroke="#667eea" fill="none"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          Rewritten Bullet Points
        </div>""", unsafe_allow_html=True)
        st.caption("Your original bullets improved with stronger action verbs and measurable impact")

        for i, bullet in enumerate(result.get("rewritten_bullets", []), 1):
            with st.expander(f"Bullet {i}", expanded=True):
                st.markdown(f"""
                <div class="bullet-block">
                  <div class="bullet-label bullet-original-label">Original</div>
                  <div class="bullet-text bullet-text-original">{bullet.get("original","")}</div>
                </div>
                <div class="bullet-block">
                  <div class="bullet-label bullet-improved-label">Improved</div>
                  <div class="bullet-text bullet-text-improved">{bullet.get("improved","")}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Overall Advice ─────────────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
          <svg viewBox="0 0 24 24" stroke="#667eea" fill="none"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          Overall Advice
        </div>""", unsafe_allow_html=True)
        st.markdown(f'<div class="advice-card">{result.get("overall_advice","")}</div>', unsafe_allow_html=True)

        # ── Download ───────────────────────────────────────────────────────────
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        report_lines = [
            "AI RESUME ANALYSIS REPORT",
            "=" * 50,
            f"Match Score: {score}/100 — {score_label}",
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
            label="Download Report",
            data=report_text,
            file_name="resume_analysis_report.txt",
            mime="text/plain",
            use_container_width=True,
        )