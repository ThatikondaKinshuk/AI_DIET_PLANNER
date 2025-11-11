import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# --- Configuration ---
PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODELS = ["gemini-1.5-flash"]

def initialize_gemini_client():
    """Initializes the Gemini client."""
    if not API_KEY:
        st.error("Gemini API Key not found. Please set GEMINI_API_KEY in your .env file.")
        return None
    try:
        return genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Error initializing Gemini client: {e}")
        return None

def generate_diet_plan(user_data: dict, client: genai.Client):
    """Generates the diet plan using a structured LLM prompt."""
    
    # 1. Define the LLM Persona and Instructions (The "System Prompt")
    system_instruction = f"""
    You are 'NutriGenie', a licensed, professional nutritionist specializing in creating hyper-personalized, practical, and nutritionally sound 7-day meal plans.

    ### Core Task
    Generate a highly detailed 7-day meal plan and a corresponding consolidated grocery list based *only* on the user's provided health data, goals, and constraints.

    ### Strict Constraints
    1.  **Safety First:** Absolutely avoid suggesting foods the user is allergic to or has listed as 'disliked'.
    2.  **Format:** Output the entire response in a single, clean **Markdown** block. Do not use JSON or any other format.
    3.  **Accuracy:** Calculate and display the approximate **Total Daily Calories** and **Macronutrient Split (Protein/Carbs/Fat)** for each day. Ensure the plan aligns with the user's goals (e.g., a weight loss plan must be in a caloric deficit).
    4.  **Practicality:** Meals should be simple and realistic for the user's stated Cooking Skill Level.

    ### User Profile
    {user_data}
    """

    # 2. Structure the Request
    prompt = f"""
    Please generate the 7-day meal plan and grocery list for the following individual.

    **Structure the output like this:**

    ## 🍎 Personalized 7-Day Meal Plan
    ### Day 1: [Theme, e.g., High-Protein Kickstart]
    * **Breakfast:** [Meal name] (Calories: X kcal | Macros: P:Xg, C:Xg, F:Xg)
    * **Lunch:** [Meal name] (Calories: X kcal | Macros: P:Xg, C:Xg, F:Xg)
    * **Dinner:** [Meal name] (Calories: X kcal | Macros: P:Xg, C:Xg, F:Xg)
    * **Daily Total:** Calories: Y kcal | Macros: P:Yg, C:Yg, F:Yg
    ... (Continue for Day 2 through Day 7)

    ---

    ## 🛒 Consolidated Grocery List
    * **Produce:** * 2 large heads of Broccoli
        * 1 lb Chicken Breast
    * **Dairy/Refrigerated:** * ...
    * **Pantry/Dry Goods:** * ...
    """
    
    # 3. Call the Gemini API with retry logic and graceful fallbacks
    max_retries = 3
    retry_delay = 2  # seconds
    models_to_try = [PRIMARY_MODEL] + FALLBACK_MODELS
    last_error = None

    for model in models_to_try:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=[prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7 # Add creativity
                    )
                )
                return response.text, model
            except Exception as e:
                error_message = str(e)
                last_error = e

                # Check if it's a 503 overload error
                if "503" in error_message or "overloaded" in error_message.lower():
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)  # Exponential backoff per attempt
                        st.warning(
                            f"{model} is overloaded. Retrying in {wait_time} seconds... "
                            f"(Attempt {attempt + 1}/{max_retries})"
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        if model != models_to_try[-1]:
                            st.warning(
                                f"{model} is overloaded after {max_retries} attempts. "
                                "Switching to fallback model."
                            )
                        else:
                            st.error(
                                f"❌ All available models are overloaded after {max_retries} attempts each. "
                                "Please try again in a few minutes."
                            )
                            st.info(
                                "💡 **Tip:** The free Gemini API has usage limits. Try again later or consider using a different model."
                            )
                        break
                else:
                    # For other errors, fail immediately
                    st.error(f"An error occurred during API call with {model}: {e}")
                    return None, None
        else:
            # Only executed if the inner loop didn't break, but we always break/return, so keep for clarity
            continue

    return None, None

# --- Streamlit UI Setup ---
st.set_page_config(page_title="NutriGenie: AI Diet Planner", layout="wide")
st.title("✨ NutriGenie: Hyper-Personalized AI Diet Planner")
st.markdown("A simple, ingredient-aware diet planning tool powered by Google's Gemini AI.")

client = initialize_gemini_client()

# --- Sidebar for User Input ---
with st.sidebar:
    st.header("👤 Your Health Profile")
    
    with st.form("profile_form"):
        # Biometrics
        st.subheader("Metrics & Goals")
        name = st.text_input("Name (for personalization)", "Trailblazer")
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        weight = st.number_input("Weight (kg)", min_value=40, value=75)
        height = st.number_input("Height (cm)", min_value=120, value=175)
        
        goal = st.selectbox("Primary Health Goal", 
            ["Weight Loss", "Muscle Gain", "Maintenance", "Manage Diabetes", "Boost Energy"])
        activity = st.selectbox("Activity Level", 
            ["Sedentary (desk job)", "Lightly Active (1-3x/week)", "Moderately Active (3-5x/week)", "Very Active (daily intense)"])

        st.subheader("Dietary Constraints")
        diet_type = st.selectbox("Diet Type/Preference", 
            ["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo", "Gluten-Free"])
        allergies = st.text_input("Allergies (comma-separated)", "None")
        dislikes = st.text_input("Disliked Foods (comma-separated)", "Broccoli, Cilantro")
        
        st.subheader("Practicality & Uniqueness")
        cooking_skill = st.select_slider("Your Cooking Skill Level", options=['Novice', 'Intermediate', 'Chef'])
        # Unique Feature: Ingredient-First Planning
        available_ingredients = st.text_area("Ingredients You Have/Prefer (Optional - comma-separated for a customized plan)", 
                                             placeholder="e.g., Chicken Breast, Spinach, Rice, Canned Tuna")

        submit_button = st.form_submit_button("🔥 Generate My Plan")

# --- Main Content Area ---
if submit_button and client:
    # Compile user data into a dictionary for the LLM prompt
    user_data = {
        "Name": name,
        "Age": age,
        "Weight (kg)": weight,
        "Height (cm)": height,
        "Goal": goal,
        "Activity Level": activity,
        "Diet Type": diet_type,
        "Allergies": allergies if allergies else "None",
        "Disliked Foods": dislikes if dislikes else "None",
        "Cooking Skill Level": cooking_skill,
        "Available/Preferred Ingredients": available_ingredients if available_ingredients else "None provided - use common ingredients."
    }
    
    with st.spinner("🧠 NutriGenie is crunching the data and synthesizing your personalized 7-Day Plan..."):
        plan_output, model_used = generate_diet_plan(user_data, client)

    if plan_output:
        st.session_state['plan'] = plan_output
        st.session_state['model_used'] = model_used
        st.success("✅ Plan Generated! See below.")
    else:
        st.session_state.pop('model_used', None)

# Display the generated plan if it exists
if 'plan' in st.session_state:
    if st.session_state.get('model_used'):
        st.caption(f"Plan generated using: {st.session_state['model_used']}")
    st.markdown(st.session_state['plan'])
    
    st.markdown("---")
    
    # Unique Feature: Conversational Coach for Refinement
    st.subheader("💬 AI Coach Refinement (Conversational LLM)")
    refinement_prompt = st.text_area(
        "Ask the AI Coach for a change or advice (e.g., 'Make Tuesday's dinner low-carb' or 'Suggest a better snack for Day 4').", 
        key="refinement_input"
    )
    
    if st.button("🔄 Refine Plan") and refinement_prompt:
        st.warning("Feature coming soon! For now, please run the main generator again with the refined input.")
        
        # --- Future conversational logic would go here ---
        # The prompt would include the current plan AND the refinement request.
        # st.session_state['plan'] = refine_plan_with_llm(st.session_state['plan'], refinement_prompt, client)
        # st.experimental_rerun()