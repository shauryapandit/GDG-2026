# Google Solution Challenge 2026 - Build with AI

Team `Karsus's Codex` :
- Shaurya Pandit
- Debjeet Singha
- Debojit Roy

# 🔍 LLM Bias Detector

A **Streamlit-powered web app** that analyzes any LLM-generated text for hidden biases using the **Google Gemini API**. Paste a response from ChatGPT, Claude, Gemini, or any other LLM — and get an instant, structured bias audit with severity scores, highlighted excerpts, and rewrite suggestions.

---

## ✨ Features

- **10+ Bias Categories** — Gender, Racial/Ethnic, Age, Cultural, Confirmation, Political, Socioeconomic, Religious, Disability, and Geographic bias detection
- **Overall Bias Score** — A 0–100 gauge showing how biased the text is at a glance
- **Severity Breakdown** — Interactive bar chart categorizing each bias as Low, Medium, High, or Critical
- **Detailed Findings** — Each bias includes the exact excerpt, an explanation of why it's biased, and a suggested rewrite
- **Pre-loaded Examples** — Try instantly with a biased job description, a biased news article, or a neutral scientific text
- **Secure API Key Input** — Enter your Gemini API key directly in the sidebar (password-masked, never stored on disk)
- **Dark Mode UI** — A polished, modern interface with gradient accents, smooth animations, and Inter typography

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **[uv](https://docs.astral.sh/uv/)** (recommended) or pip
- **Google Gemini API Key** — Get one free at [Google AI Studio](https://aistudio.google.com/apikey)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/GDG-2026.git
cd GDG-2026

# Install dependencies
uv sync
```

### Run the App

```bash
uv run streamlit run app.py
```

The app will open at **http://localhost:8501**.

> **Note:** Enter your Gemini API key in the sidebar when prompted. Alternatively, you can set the `GEMINI_API_KEY` environment variable before launching.

---

## 🎮 Usage

1. **Enter your API key** — Paste your Gemini API key in the sidebar's password field
2. **Paste text** — Copy any LLM-generated text into the main text area (or click an example in the sidebar)
3. **Click "Analyze for Bias"** — Gemini will analyze the text and return structured results
4. **Review the dashboard** — Explore the bias score gauge, category breakdown, and detailed findings with suggestions

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io/) | Web framework & UI |
| [Google Gemini API](https://ai.google.dev/) | Bias analysis via `gemini-2.5-flash` |
| [google-genai](https://pypi.org/project/google-genai/) | Official Google Gen AI Python SDK |
| [Plotly](https://plotly.com/python/) | Interactive gauge & bar charts |

---

## 📁 Project Structure

```
GDG-2026/
├── .streamlit/
│   └── config.toml        # Streamlit theme (dark mode)
├── app.py                 # Streamlit dashboard — UI, charts, layout
├── bias_analyzer.py       # Gemini API wrapper — sends text, parses JSON
├── prompts.py             # System prompt & analysis template
├── pyproject.toml         # Project metadata & dependencies
└── README.md
```

---

## 🔑 API Key

The app accepts your Gemini API key in **two ways** (in priority order):

1. **Sidebar input** — Enter it directly in the UI (recommended, password-masked)
2. **Environment variable** — Set `GEMINI_API_KEY` before launching:
   ```bash
   # Windows
   set GEMINI_API_KEY=your-key-here

   # Linux / macOS
   export GEMINI_API_KEY=your-key-here
   ```

Your key is only held in memory during the session and is **never written to disk**.

---

## 🧠 How It Works

1. Your text is sent to **Gemini 2.5 Flash** with a carefully engineered system prompt that instructs it to act as an impartial bias auditor
2. The model is configured to return **structured JSON** (`response_mime_type="application/json"`) for reliable parsing
3. The response includes an overall bias score, a list of biases (each with category, severity, excerpt, explanation, and suggestion), and a plain-English summary
4. The Streamlit frontend renders the results as interactive Plotly charts and styled HTML cards

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
