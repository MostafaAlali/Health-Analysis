# 🏥 Medical Blood Report Analyzer

A Streamlit-based AI system that analyzes medical blood reports using Google Gemini 2.5 Flash to extract values, classify results, and generate health insights and diet recommendations.

---

## 🚀 Problem

Reading and interpreting blood test reports requires medical knowledge and time. Patients often struggle to understand medical terminology and reference ranges.

---

## 💡 Solution

This application uses LLM-powered analysis to:

- Extract medical values from raw reports
- Compare against reference ranges
- Classify results (HIGH / LOW / NORMAL)
- Generate health summaries
- Provide diet recommendations
- Produce full clinical-style reports

---

## 🧠 Tech Stack

| Component | Technology | Purpose |
|----------|------------|---------|
| LLM | Google Gemini 2.5 Flash | Medical data extraction and reasoning |
| Framework | Streamlit | Interactive web UI |
| Language | Python 3.8+ | Core runtime |
| LLM Integration | LangChain + Google GenAI | API orchestration |
| Data Processing | Pandas | Structured data handling |
| Styling | HTML / CSS | Clinical UI formatting |
| File Handling | Python Native | Upload / export reports |

---

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- Google API Key (from Google AI Studio)

---

### Setup

```bash
git clone https://github.com/yourusername/medical-blood-report-analyzer.git
cd medical-blood-report-analyzer

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

echo "GOOGLE_API_KEY=your_api_key_here" > .env

streamlit run app.py
