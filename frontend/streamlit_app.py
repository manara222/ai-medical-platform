import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from PIL import Image
from io import BytesIO

from utils.chatbot_helper import generate_chatbot_response

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="AI Multi-Disease Diagnosis Platform",
    page_icon="🩺",
    layout="wide"
)

# =========================
# Session State
# =========================
if "last_case_info" not in st.session_state:
    st.session_state.last_case_info = None

if "chat_response" not in st.session_state:
    st.session_state.chat_response = ""

# =========================
# Custom CSS
# =========================
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #040b16 0%, #091525 100%);
        color: white;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1420px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-family: 'Segoe UI', sans-serif;
    }

    p, label, div, span, li {
        font-family: 'Segoe UI', sans-serif;
    }

    .hero-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.98), rgba(30,41,59,0.94));
        border: 1px solid rgba(148,163,184,0.16);
        border-radius: 30px;
        padding: 38px;
        box-shadow: 0 18px 42px rgba(0,0,0,0.30);
        margin-bottom: 24px;
    }

    .section-card {
        background: rgba(15, 23, 42, 0.80);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.18);
        margin-bottom: 22px;
    }

    .dashboard-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.96), rgba(15,23,42,0.94));
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(148,163,184,0.14);
        box-shadow: 0 10px 24px rgba(0,0,0,0.16);
        min-height: 150px;
    }

    .impact-card {
        background: linear-gradient(135deg, rgba(2,132,199,0.12), rgba(15,23,42,0.90));
        border-radius: 20px;
        padding: 18px;
        border: 1px solid rgba(56,189,248,0.20);
        box-shadow: 0 10px 24px rgba(0,0,0,0.16);
        min-height: 135px;
    }

    .metric-result-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.94), rgba(15,23,42,0.94));
        border-radius: 18px;
        padding: 18px;
        border: 1px solid rgba(148,163,184,0.14);
        text-align: center;
        min-height: 125px;
    }

    .dashboard-label {
        color: #94a3b8;
        font-size: 0.92rem;
        margin-bottom: 10px;
    }

    .dashboard-value {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.15;
    }

    .dashboard-sub {
        color: #cbd5e1;
        font-size: 0.92rem;
        margin-top: 10px;
    }

    .metric-title {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #f8fafc;
        word-break: break-word;
    }

    .small-badge {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 0.84rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .badge-blue {
        background: rgba(59,130,246,0.14);
        color: #93c5fd;
        border: 1px solid rgba(59,130,246,0.28);
    }

    .badge-green {
        background: rgba(34,197,94,0.14);
        color: #86efac;
        border: 1px solid rgba(34,197,94,0.28);
    }

    .badge-yellow {
        background: rgba(234,179,8,0.14);
        color: #fde68a;
        border: 1px solid rgba(234,179,8,0.28);
    }

    .badge-purple {
        background: rgba(168,85,247,0.14);
        color: #d8b4fe;
        border: 1px solid rgba(168,85,247,0.28);
    }

    .logo-box {
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at top, rgba(14,165,233,0.20), rgba(15,23,42,0.95));
        border: 1px solid rgba(56,189,248,0.18);
        border-radius: 24px;
        min-height: 220px;
        font-size: 4.5rem;
        box-shadow: 0 10px 28px rgba(0,0,0,0.18);
    }

    .info-note {
        background: rgba(14,165,233,0.08);
        border: 1px solid rgba(56,189,248,0.18);
        border-radius: 16px;
        padding: 14px;
        color: #dbeafe;
    }

    .workflow-step {
        background: rgba(2,132,199,0.08);
        border: 1px solid rgba(56,189,248,0.18);
        border-radius: 16px;
        padding: 14px;
        color: #dbeafe;
        margin-bottom: 10px;
    }

    .judge-box {
        background: linear-gradient(135deg, rgba(34,197,94,0.10), rgba(15,23,42,0.90));
        border: 1px solid rgba(34,197,94,0.20);
        border-radius: 18px;
        padding: 18px;
        color: #dcfce7;
    }

    .disease-icon-card {
        background: rgba(15,23,42,0.75);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        min-height: 130px;
    }

    .disease-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }

    .sample-card {
        background: rgba(15,23,42,0.75);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 18px;
        padding: 18px;
        min-height: 150px;
    }

    .reason-box {
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.20);
        border-radius: 16px;
        padding: 16px;
        color: #dcfce7;
        margin-top: 12px;
    }

    .footer-box {
        margin-top: 28px;
        padding: 16px 20px;
        border-radius: 16px;
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(148,163,184,0.14);
        color: #cbd5e1;
        text-align: center;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.12;
        margin-bottom: 12px;
        color: #f8fafc;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        color: #cbd5e1;
        margin-bottom: 16px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 14px;
        padding: 0.82rem 1rem;
        font-weight: 700;
        border: none;
        background: linear-gradient(135deg, #0ea5e9, #2563eb);
        color: white;
        box-shadow: 0 8px 24px rgba(37,99,235,0.35);
    }

    .stDownloadButton>button {
        width: 100%;
        border-radius: 14px;
        padding: 0.82rem 1rem;
        font-weight: 700;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(15,23,42,0.82);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 12px;
        padding: 10px 16px;
        color: #e2e8f0;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("## 🩺 Project Dashboard")
    st.markdown(
        """
        **AI Multi-Disease Diagnosis Platform**  
        Unified medical imaging assistant for:
        - Skin Diseases
        - Eye Diseases
        - COVID-19 Chest X-ray
        - Breast Ultrasound
        """
    )

    st.markdown("---")
    st.markdown("### ✨ Key Features")
    st.markdown(
        """
        - Image Enhancement  
        - Multi-Model Classification  
        - Confidence Scoring  
        - Explainable AI  
        - PDF Medical Report  
        - Medical AI Chatbot
        """
    )

    st.markdown("---")
    st.markdown("### 🧠 AI Modules")
    st.success("Skin Disease")
    st.success("Eye Disease")
    st.success("COVID-19")
    st.success("Breast Cancer")

# =========================
# Hero
# =========================
hero_left, hero_right = st.columns([1.35, 0.65], gap="large")

with hero_left:
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">AI Multi-Disease Diagnosis Platform</div>
        <div class="hero-subtitle">
            A competition-ready medical imaging solution that combines disease classification,
            explainable AI, confidence scoring, downloadable clinical-style reports,
            and an AI medical assistant in one unified platform.
        </div>
        <span class="small-badge badge-blue">Deep Learning</span>
        <span class="small-badge badge-green">Explainable AI</span>
        <span class="small-badge badge-yellow">Clinical Workflow</span>
        <span class="small-badge badge-purple">Competition Ready</span>
    </div>
    """, unsafe_allow_html=True)

with hero_right:
    st.markdown('<div class="logo-box">🩺</div>', unsafe_allow_html=True)

# =========================
# Disease Icons
# =========================
st.markdown("### 🧬 Supported Disease Modules")
g1, g2, g3, g4 = st.columns(4, gap="medium")

with g1:
    st.markdown("""
    <div class="disease-icon-card">
        <div class="disease-icon">🩹</div>
        <div class="dashboard-value" style="font-size:1.2rem;">Skin</div>
        <div class="dashboard-sub">7-class dermoscopic analysis</div>
    </div>
    """, unsafe_allow_html=True)

with g2:
    st.markdown("""
    <div class="disease-icon-card">
        <div class="disease-icon">👁️</div>
        <div class="dashboard-value" style="font-size:1.2rem;">Eye</div>
        <div class="dashboard-sub">Retinal disease detection</div>
    </div>
    """, unsafe_allow_html=True)

with g3:
    st.markdown("""
    <div class="disease-icon-card">
        <div class="disease-icon">🫁</div>
        <div class="dashboard-value" style="font-size:1.2rem;">COVID-19</div>
        <div class="dashboard-sub">Chest X-ray screening support</div>
    </div>
    """, unsafe_allow_html=True)

with g4:
    st.markdown("""
    <div class="disease-icon-card">
        <div class="disease-icon">🎗️</div>
        <div class="dashboard-value" style="font-size:1.2rem;">Breast</div>
        <div class="dashboard-sub">Ultrasound image classification</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# =========================
# Impact Cards
# =========================
st.markdown("### 🌍 Project Impact")
i1, i2, i3, i4 = st.columns(4, gap="medium")

with i1:
    st.markdown("""
    <div class="impact-card">
        <div class="dashboard-label">Accessibility</div>
        <div class="dashboard-value" style="font-size:1.5rem;">Fast Screening</div>
        <div class="dashboard-sub">Quick first-pass AI support for multiple disease types.</div>
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown("""
    <div class="impact-card">
        <div class="dashboard-label">Interpretability</div>
        <div class="dashboard-value" style="font-size:1.5rem;">Explainable AI</div>
        <div class="dashboard-sub">Shows visual evidence of model attention.</div>
    </div>
    """, unsafe_allow_html=True)

with i3:
    st.markdown("""
    <div class="impact-card">
        <div class="dashboard-label">Scalability</div>
        <div class="dashboard-value" style="font-size:1.5rem;">Modular Design</div>
        <div class="dashboard-sub">Easy to extend with more disease models later.</div>
    </div>
    """, unsafe_allow_html=True)

with i4:
    st.markdown("""
    <div class="impact-card">
        <div class="dashboard-label">Deployment Value</div>
        <div class="dashboard-value" style="font-size:1.5rem;">Real Platform</div>
        <div class="dashboard-sub">Frontend, backend, AI, reporting, and chatbot.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# =========================
# Dashboard Cards
# =========================
d1, d2, d3, d4 = st.columns(4, gap="medium")

with d1:
    st.markdown("""
    <div class="dashboard-card">
        <div class="dashboard-label">Disease Groups</div>
        <div class="dashboard-value">4</div>
        <div class="dashboard-sub">Skin, Eye, COVID-19, Breast</div>
    </div>
    """, unsafe_allow_html=True)

with d2:
    st.markdown("""
    <div class="dashboard-card">
        <div class="dashboard-label">Workflow</div>
        <div class="dashboard-value">End-to-End</div>
        <div class="dashboard-sub">Upload → Enhance → Predict → Explain → Report</div>
    </div>
    """, unsafe_allow_html=True)

with d3:
    st.markdown("""
    <div class="dashboard-card">
        <div class="dashboard-label">Explainability</div>
        <div class="dashboard-value">Grad-CAM</div>
        <div class="dashboard-sub">Skin-focused visual explainability support</div>
    </div>
    """, unsafe_allow_html=True)

with d4:
    st.markdown("""
    <div class="dashboard-card">
        <div class="dashboard-label">Assistant</div>
        <div class="dashboard-value">Chatbot</div>
        <div class="dashboard-sub">Diagnosis-aware patient guidance</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Tabs
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Diagnosis",
    "📈 Model Overview",
    "🏗️ Architecture",
    "🎤 Judges Pitch",
    "🧪 Demo Cases"
])

# =========================
# Tab 1 - Diagnosis
# =========================
with tab1:
    left, right = st.columns([1.18, 0.82], gap="large")

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📤 Upload Medical Image")

        image_type = st.selectbox(
            "Select image type",
            ["skin", "eye", "covid", "breast"]
        )

        uploaded_file = st.file_uploader(
            "Upload JPG, JPEG, or PNG image",
            type=["jpg", "jpeg", "png"]
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🧬 Current Module Description")

        disease_notes = {
            "skin": "7-class dermoscopic skin disease classification using HAM10000.",
            "eye": "Retinal disease analysis from fundus images.",
            "covid": "Chest X-ray screening support for COVID-19 related cases.",
            "breast": "Breast ultrasound classification into normal, benign, and malignant."
        }

        st.markdown(
            f'<div class="info-note">{disease_notes.get(image_type, "")}</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.info(
            "This system provides AI-assisted support for educational, demo, and healthcare innovation purposes."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None:
        original_bytes = uploaded_file.getvalue()
        image = Image.open(BytesIO(original_bytes)).convert("RGB")
        normalized_type = image_type.strip().lower()

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🖼️ Image Preview")

        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            st.image(image, caption="Original Image", width="stretch")

        with col2:
            try:
                preprocess_response = requests.post(
                    "http://127.0.0.1:8000/preprocess",
                    files={"file": (uploaded_file.name, original_bytes, uploaded_file.type)}
                )
                if preprocess_response.status_code == 200:
                    processed_image = Image.open(BytesIO(preprocess_response.content)).convert("RGB")
                    st.image(processed_image, caption="Enhanced Image", width="stretch")
                else:
                    st.warning("Could not display enhanced image.")
            except Exception as e:
                st.warning(f"Preprocessing unavailable: {e}")

        with col3:
            if normalized_type == "skin":
                try:
                    gradcam_response = requests.post(
                        "http://127.0.0.1:8000/gradcam",
                        files={"file": (uploaded_file.name, original_bytes, uploaded_file.type)},
                        data={"image_type": normalized_type}
                    )

                    if gradcam_response.status_code == 200:
                        gradcam_image = Image.open(BytesIO(gradcam_response.content)).convert("RGB")
                        st.image(gradcam_image, caption="AI Focus Area", width="stretch")
                        st.success("AI localized the suspicious region using explainable attention mapping.")
                    else:
                        st.info("Explainability module is currently enabled for skin analysis only.")

                except Exception as e:
                    st.warning(f"AI focus area unavailable: {e}")
            else:
                st.info("Explainability module is currently enabled for skin analysis only.")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🔍 Analyze Image"):
            with st.spinner("Running AI diagnosis..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/analyze",
                        files={"file": (uploaded_file.name, original_bytes, uploaded_file.type)},
                        data={"image_type": normalized_type}
                    )

                    if response.status_code == 200:
                        result = response.json()
                        confidence = float(result["confidence"])

                        clinical_note = result.get("clinical_insight", "Clinical review is recommended.")
                        next_step = result.get("next_step", "Consult a medical specialist.")
                        risk_level = result.get("risk_level", "Moderate Risk")
                        urgency = result.get("urgency", "Medical follow-up is recommended.")
                        risk_color = result.get("risk_color", "yellow")

                        case_info = {
                               "disease_type": result["disease_type"],
                               "predicted_class": result["predicted_class"],
                               "clinical_insight": clinical_note,
                               "next_step": next_step,
                               "risk_level": risk_level,
                                "urgency": urgency
                        }
                        st.session_state.last_case_info = case_info
                        st.session_state.chat_response = ""

                        st.markdown('<div class="section-card">', unsafe_allow_html=True)
                        st.subheader("📊 Prediction Result")

                        r1, r2, r3 = st.columns(3, gap="medium")

                        with r1:
                            st.markdown(f"""
                            <div class="metric-result-card">
                                <div class="metric-title">Disease Type</div>
                                <div class="metric-value" style="font-size:1.35rem;">{result["disease_type"]}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        with r2:
                            st.markdown(f"""
                            <div class="metric-result-card">
                                <div class="metric-title">Predicted Class</div>
                                <div class="metric-value" style="font-size:1.65rem;">{result["predicted_class"]}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        with r3:
                            st.markdown(f"""
                            <div class="metric-result-card">
                                <div class="metric-title">Confidence</div>
                                <div class="metric-value">{confidence:.2f}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("### Confidence Score")
                        st.progress(min(max(confidence, 0.0), 1.0))

                        if confidence >= 0.85:
                            st.success("High confidence prediction.")
                        elif confidence >= 0.60:
                            st.warning("Moderate confidence prediction.")
                        else:
                            st.error("Low confidence prediction. The image may need better quality or expert review.")

                        st.info(f"🩺 Clinical Insight: {clinical_note}")
                        st.info(f"📌 {next_step}")
                        st.markdown("### 🚨 Risk Assessment")

                        if risk_color == "red":
                         st.error(f"Risk Level: {risk_level}\n\nUrgency: {urgency}")
                        elif risk_color == "green":
                         st.success(f"Risk Level: {risk_level}\n\nUrgency: {urgency}")
                        else:
                         st.warning(f"Risk Level: {risk_level}\n\nUrgency: {urgency}")

                        st.markdown("### 📌 Confidence Interpretation")
                        if confidence >= 0.85:
                         st.success("The model shows strong confidence in this prediction.")
                        elif confidence >= 0.60:
                         st.warning("The model shows moderate confidence. Clinical review is recommended.")
                        else:
                         st.error("The model confidence is limited. This case should be reviewed carefully by a specialist.")
                        summary_text = f"""
**AI Case Summary**

- **Disease Type:** {result["disease_type"]}
- **Predicted Class:** {result["predicted_class"]}
- **Confidence Score:** {confidence:.2f}
- **Clinical Insight:** {clinical_note}
- **Recommended Next Step:** {next_step}
"""
                        st.markdown("### 📋 Case Summary")
                        st.success(summary_text)

                        st.markdown("### 🧠 Why this prediction?")

                        if normalized_type == "skin":
                            explanation_html = """
                            <div class="reason-box">
                            <b>The prediction was generated based on:</b><br><br>
                            • The enhanced medical image after preprocessing.<br>
                            • The detected visual patterns learned by the deep learning model.<br>
                            • The highlighted AI Focus Area, which shows the image region that most influenced the decision.<br>
                            • The confidence score, which reflects the model’s certainty for the selected class.<br><br>
                            <b>Interpretation:</b> This is an AI-assisted screening result designed to support medical review, not replace it.
                            </div>
                            """
                        else:
                            explanation_html = """
                            <div class="reason-box">
                            <b>The prediction was generated based on:</b><br><br>
                            • The enhanced medical image after preprocessing.<br>
                            • The detected visual patterns learned by the deep learning model.<br>
                            • The confidence score, which reflects the model’s certainty for the selected class.<br><br>
                            <b>Interpretation:</b> This is an AI-assisted screening result designed to support medical review, not replace it.
                            </div>
                            """

                        st.markdown(explanation_html, unsafe_allow_html=True)

                        st.warning(
                            "This result is AI-assisted and not a final medical diagnosis. "
                            "Please consult a qualified medical professional."
                        )

                        report_response = requests.post(
                            "http://127.0.0.1:8000/report",
                            files={"file": (uploaded_file.name, original_bytes, uploaded_file.type)},
                            data={"image_type": normalized_type}
                        )

                        if report_response.status_code == 200:
                            st.download_button(
                                label="📄 Download Medical Report (PDF)",
                                data=report_response.content,
                                file_name="medical_report.pdf",
                                mime="application/pdf"
                            )
                        else:
                            st.error("Could not generate PDF report.")

                        st.markdown("</div>", unsafe_allow_html=True)

                    else:
                        st.error(f"API Error: {response.text}")

                except Exception as e:
                    st.error(f"Connection Error: {e}")

    # =========================
    # Medical Chatbot
    # =========================
    if st.session_state.last_case_info is not None:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("💬 Medical AI Assistant")

        user_question = st.text_input(
            "Ask about the current case",
            placeholder="Example: What does this result mean?"
        )

        if st.button("Send to Assistant"):
            if user_question.strip():
                st.session_state.chat_response = generate_chatbot_response(
                    user_question,
                    st.session_state.last_case_info
                )
            else:
                st.warning("Please type a question first.")

        if st.session_state.chat_response:
            st.markdown("### Assistant Response")
            st.info(st.session_state.chat_response)

        st.markdown("""
        **Suggested questions:**
        - What does this result mean?
        - What should I do next?
        - Is this serious?
        - How confident is the AI?
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Tab 2 - Model Overview
# =========================
with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📈 Model Performance Dashboard")

    o1, o2, o3, o4 = st.columns(4, gap="medium")

    with o1:
        st.markdown("""
        <div class="dashboard-card">
            <div class="dashboard-label">Skin Model</div>
            <div class="dashboard-value">96.2%</div>
<div class="dashboard-sub">Training Accuracy</div>
<div class="dashboard-sub" style="font-size:0.8rem; opacity:0.7;">
testing: 73.17%
</div>
            <div class="dashboard-sub">7-class dermoscopic classification</div>
        </div>
        """, unsafe_allow_html=True)

    with o2:
        st.markdown("""
        <div class="dashboard-card">
            <div class="dashboard-label">Eye Model</div>
            <div class="dashboard-value">88.10%</div>
            <div class="dashboard-sub">Retinal disease classification</div>
        </div>
        """, unsafe_allow_html=True)

    with o3:
        st.markdown("""
        <div class="dashboard-card">
            <div class="dashboard-label">COVID Model</div>
            <div class="dashboard-value">97.22%</div>
            <div class="dashboard-sub">Chest X-ray classification</div>
        </div>
        """, unsafe_allow_html=True)

    with o4:
        st.markdown("""
        <div class="dashboard-card">
            <div class="dashboard-label">Breast Model</div>
            <div class="dashboard-value">94.51%</div>
            <div class="dashboard-sub">Breast ultrasound classification</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    a, b = st.columns(2, gap="large")

    with a:
        st.markdown("### Strengths")
        st.success("Unified multi-disease platform")
        st.success("High-performing COVID and Breast models")
        st.success("Strong eye disease module")
        st.success("Explainable AI + PDF reporting")
        st.success("Diagnosis-aware medical assistant")

    with b:
        st.markdown("### Key Observation")
        st.info("Skin disease classification is the most challenging due to 7 classes and heavy class imbalance.")
        st.info("COVID and Breast models achieved strong validation performance.")
        st.info("The system demonstrates modular AI integration across multiple medical domains.")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Tab 3 - Architecture
# =========================
with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🏗️ System Architecture")

    st.code(
"""User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend
  ├── Image Preprocessing
  ├── Skin Disease Model
  ├── Eye Disease Model
  ├── COVID-19 Model
  ├── Breast Cancer Model
  ├── Explainable AI
  ├── Medical AI Assistant
  └── PDF Report Generator""",
        language="text"
    )

    st.markdown("### Workflow")
    st.markdown("""
    <div class="workflow-step"><b>1. Upload Image:</b> User uploads a supported medical image.</div>
    <div class="workflow-step"><b>2. Image Enhancement:</b> Preprocessing improves image quality.</div>
    <div class="workflow-step"><b>3. AI Diagnosis:</b> The selected disease-specific model performs classification.</div>
    <div class="workflow-step"><b>4. Confidence Score:</b> The system provides prediction confidence.</div>
    <div class="workflow-step"><b>5. Explainable AI:</b> Skin module supports focus-area visualization where localization is clinically meaningful.</div>
    <div class="workflow-step"><b>6. Medical Chatbot:</b> User can ask about the result and next steps.</div>
    <div class="workflow-step"><b>7. PDF Report:</b> A downloadable report is generated instantly.</div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Tab 4 - Judges Pitch
# =========================
with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🎤 Judges Pitch Section")

    j1, j2 = st.columns(2, gap="large")

    with j1:
        st.markdown("""
        <div class="judge-box">
            <h4 style="margin-top:0;">Why This Project Stands Out</h4>
            <ul>
                <li>Supports 4 disease groups in one unified platform</li>
                <li>Combines AI prediction, explainability, PDF reporting, and a chatbot</li>
                <li>Uses real trained deep learning models</li>
                <li>Transforms a demo into a product-like medical solution</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with j2:
        st.markdown("""
        <div class="judge-box">
            <h4 style="margin-top:0;">Suggested Live Demo Flow</h4>
            <ol>
                <li>Open Diagnosis tab</li>
                <li>Select a disease type</li>
                <li>Upload one sample image</li>
                <li>Show enhancement + skin explainability demo where applicable</li>
                <li>Explain prediction confidence</li>
                <li>Ask the chatbot one question</li>
                <li>Download the PDF report</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Problem Statement")
    st.write(
        "Medical image interpretation can be time-consuming and requires expertise. "
        "This platform provides a unified AI-assisted screening experience for multiple disease domains."
    )

    st.markdown("### Innovation Value")
    st.write(
        "Unlike single-disease tools, this project integrates multiple specialized AI models, "
        "explainable AI, reporting, and a diagnosis-aware assistant into one scalable product."
    )

    st.markdown("### Judges One-Line Pitch")
    st.success(
        "We built a unified AI medical imaging platform that can screen multiple diseases, explain its predictions, guide the user, and generate instant clinical-style reports."
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Tab 5 - Demo Cases
# =========================
with tab5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🧪 Demo Cases for Presentation")

    s1, s2, s3, s4 = st.columns(4, gap="medium")

    with s1:
        st.markdown("""
        <div class="sample-card">
            <h4>🩹 Skin Case</h4>
            <p><b>Use:</b> One clear dermoscopic image</p>
            <p><b>Goal:</b> Show 7-class prediction + Grad-CAM + chatbot</p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="sample-card">
            <h4>👁️ Eye Case</h4>
            <p><b>Use:</b> One retinal image</p>
            <p><b>Goal:</b> Show retinal classification + explanation</p>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="sample-card">
            <h4>🫁 COVID Case</h4>
            <p><b>Use:</b> One chest X-ray</p>
            <p><b>Goal:</b> Show strongest-performing model</p>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown("""
        <div class="sample-card">
            <h4>🎗️ Breast Case</h4>
            <p><b>Use:</b> One ultrasound image</p>
            <p><b>Goal:</b> Show malignant / benign / normal classification</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "Before presentation, prepare one strong demo image for each disease category so the live demo runs smoothly."
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("""
<div class="footer-box">
    Built for AI Healthcare Innovation • Multi-Disease Classification • Explainable AI • Medical AI Assistant • Clinical Report Generation
</div>
""", unsafe_allow_html=True)