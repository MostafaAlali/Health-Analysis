import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Page configuration
st.set_page_config(
    page_title="Medical Blood Report Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .abnormal-high {
        color: #d32f2f;
        font-weight: bold;
    }
    .abnormal-low {
        color: #f57c00;
        font-weight: bold;
    }
    .normal {
        color: #388e3c;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header">
    <h1>🏥 Medical Blood Report Analyzer</h1>
    <p>AI-Powered Analysis with Diet Recommendations</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Configuration")
    
    upload_method = st.radio(
        "Choose input method:",
        ("Upload File", "Paste Text")
    )
    
    patient_name = st.text_input("Patient Name (optional)")
    show_details = st.checkbox("Show detailed analysis", value=True)

# Main content
st.header("📊 Blood Report Analysis")

# Get blood report content
if upload_method == "Upload File":
    uploaded_file = st.file_uploader("Upload blood report (.txt file)", type="txt")
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
    else:
        content = None
else:
    content = st.text_area("Paste blood report here:", height=200)

if content:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Extract Values", use_container_width=True):
            st.session_state.analyze = True
    
    with col2:
        if st.button("🍽️ Get Diet Plan", use_container_width=True):
            st.session_state.diet = True
    
    with col3:
        if st.button("📄 Full Report", use_container_width=True):
            st.session_state.full_report = True
    
    # STAGE 1: Extract and Classify Values
    if st.session_state.get("analyze"):
        st.divider()
        st.subheader("*** STAGE 1: EXTRACTED VALUES ***")
        
        extraction_prompt = f"""
        You are a medical data extraction assistant.
        
        From the blood report below, extract all test values and classify each one as HIGH, LOW, or NORMAL 
        based on the reference ranges provided in the report.
        
        Format your response as:
        - Test Name: value | Status: HIGH/LOW/NORMAL | Reference: range
        
        Blood Report:
        {content}
        """
        
        with st.spinner("Extracting values..."):
            extraction_response = llm.invoke(extraction_prompt)
            response_text = extraction_response.content
        
        # Display extracted values
        for line in response_text.strip().split('\n'):
            if line.strip():
                # Color code the status
                if "HIGH" in line:
                    st.markdown(f"<p class='metric-box'><span class='abnormal-high'>⚠️ {line.strip()}</span></p>", 
                               unsafe_allow_html=True)
                elif "LOW" in line:
                    st.markdown(f"<p class='metric-box'><span class='abnormal-low'>⚠️ {line.strip()}</span></p>", 
                               unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='metric-box'><span class='normal'>✓ {line.strip()}</span></p>", 
                               unsafe_allow_html=True)
        
        st.success("✅ Extraction complete!")
    
    # STAGE 2: Health Summary
    if st.session_state.get("analyze") or st.session_state.get("full_report"):
        st.divider()
        st.subheader("*** STAGE 2: HEALTH SUMMARY ***")
        
        summary_prompt = f"""
        You are a clinical health advisor.
        
        Based on the blood report below, provide:
        1. A brief health summary (3-4 lines) explaining the patient's condition in simple language
        2. Key areas of concern (if any)
        3. Positive findings
        
        Blood Report:
        {content}
        """
        
        with st.spinner("Generating health summary..."):
            summary_response = llm.invoke(summary_prompt)
            summary_text = summary_response.content
        
        st.info(summary_text)
    
    # STAGE 3: Diet Recommendations
    if st.session_state.get("diet") or st.session_state.get("full_report"):
        st.divider()
        st.subheader("*** STAGE 3: PERSONALIZED DIET PLAN ***")
        
        diet_prompt = f"""
        You are a clinical nutritionist specializing in Indian dietary habits.
        
        Based on the blood work analysis below, write:
        1. A short health summary (3-4 lines) explaining the patient's condition in simple language
        2. A short, practical Indian diet plan having three sections:
           - Foods to AVOID
           - Foods to EAT MORE OF
           - Healthy drinks to consume every morning
        
        Do not include any other sections in the diet plan.
        
        Blood Report:
        {content}
        """
        
        with st.spinner("Generating diet plan..."):
            diet_response = llm.invoke(diet_prompt)
            diet_text = diet_response.content
        
        st.success(diet_text)
        
        # Download option
        st.download_button(
            label="📥 Download Diet Plan",
            data=diet_text,
            file_name=f"diet_plan_{patient_name or 'patient'}.txt",
            mime="text/plain"
        )
    
    # STAGE 4: Full Comprehensive Report
    if st.session_state.get("full_report"):
        st.divider()
        st.subheader("*** STAGE 4: COMPREHENSIVE MEDICAL REPORT ***")
        
        full_prompt = f"""
        You are a medical analyst. Create a comprehensive report including:
        1. Patient Profile Summary
        2. Test Results Analysis
        3. Risk Assessment
        4. Recommendations
        5. Follow-up Tests Suggested
        
        Blood Report:
        {content}
        """
        
        with st.spinner("Generating comprehensive report..."):
            full_response = llm.invoke(full_prompt)
            full_text = full_response.content
        
        st.markdown(full_text)
        
        # Download comprehensive report
        st.download_button(
            label="📥 Download Full Report",
            data=full_text,
            file_name=f"medical_report_{patient_name or 'patient'}.txt",
            mime="text/plain"
        )

else:
    st.info("👆 Please upload or paste a blood report to begin analysis")

# Footer
st.divider()
st.markdown("""
    <center>
    <p style='color: gray; font-size: 12px;'>
    ⚕️ <b>Medical Disclaimer:</b> This app provides analytical support only. 
    Always consult with a qualified healthcare professional for medical advice.
    </p>
    </center>
""", unsafe_allow_html=True)
