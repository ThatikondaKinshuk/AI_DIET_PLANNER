# 🥗 NutriGenie: Hyper-Personalized AI Diet Planner

NutriGenie replaces static meal plans with an adaptive AI nutritionist. Powered by Google Gemini and Streamlit, it delivers nutritionally accurate 7-day meal plans tailored to individual goals, dietary constraints, and pantry inventory.

---

## 🚀 Why NutriGenie Stands Out

- **Ingredient-first planning:** Input on-hand ingredients (for example, `"chicken, spinach, rice"`) and receive a plan that minimizes grocery waste.
- **Adaptive AI coaching:** Ask for adjustments like "I had pizza for lunch—make dinner low-carb" or "Suggest a healthy sweet snack." The AI responds conversationally.
- **Strict nutritional guardrails:** Prompt engineering enforces allergy avoidance, caloric targets, and macro balance aligned with each health goal.

---

## 🏗️ Architecture Overview

```text
Browser (Streamlit UI)
    │ sidebar inputs / plan display
    ▼
Streamlit runtime (streamlit_app.py)
    │ constructs NutriGenie persona prompt
    ▼
Google Gemini API (gemini-2.5-flash)
    │ returns markdown meal plan + grocery list
    ▼
Session state cache for plan persistence
```

---

## 🔄 Workflow

1. **Profile capture:** Sidebar form collects biometrics, goals, allergies, dislikes, and favorite ingredients.
2. **Persona prompt creation:** `generate_diet_plan` merges the profile into a structured system prompt with strict output rules.
3. **Model invocation:** `genai.Client` sends the request to Gemini (`gemini-2.5-flash`) and receives a Markdown-formatted response.
4. **Plan presentation:** Streamlit renders the plan, stores it in `st.session_state`, and readies the refinement coach area.
5. **Future iterations:** The AI Coach section is prepared for follow-up prompts once refinement logic is wired in.

---

## ⚙️ Tech Stack

- **Frontend/UI:** Streamlit
- **AI Core:** Google Gemini SDK (`google-genai`)
- **Config Management:** `python-dotenv` for `.env` secrets
- **Language:** Python 3.9+

---

## 🧰 Local Setup

### 1. Prerequisites

- Python 3.9 or later
- Gemini API key

### 2. Environment Setup

```bash
# (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. API Key Configuration

Create a `.env` file in the project root and add:

```env
GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
```

### 4. Run the Application

```bash
streamlit run streamlit_app.py
```

Open the app in your browser at `http://localhost:8501`.

---

## 🛤️ Roadmap

1. **Validated nutrition data (RAG):** Pull caloric and macro data from authoritative sources such as the USDA API.
2. **Conversational memory:** Persist plan history via `st.session_state` or vector storage to reference past coaching sessions.
3. **Multimodal logging:** Add photo-based meal logging using multimodal LLM capabilities.

---

## 🤝 Contributions

Ideas, bugs, and improvements are welcome. Please open an issue or submit a pull request.

---

## ⚖️ Disclaimer

NutriGenie is an AI-powered educational tool and does not replace professional medical advice. Consult a qualified healthcare provider or registered dietitian before making major dietary changes.
