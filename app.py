import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(
    page_title="AI Personal Trainer",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main Title Color - Fitness Green */
    .main-header { 
        font-size: 3rem; 
        color: #2E7D32; /* Dark Green */
        text-align: center; 
        font-weight: 800;
        margin-bottom: 1rem; 
    }
    
    /* Subtitle Color */
    .sub-header { 
        font-size: 1.2rem; 
        color: #555; 
        text-align: center; 
        margin-bottom: 2rem; 
    }
    
    /* Button Style - Vibrant Green */
    .stButton>button { 
        width: 100%; 
        background-color: #4CAF50; 
        color: white; 
        font-weight: bold; 
        border-radius: 10px;
        height: 50px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    
    /* TEXT BOX COLOR CHANGE (Black text on Light Green background) */
    .stTextArea textarea {
        background-color: #E8F5E9 !important; /* Light Green */
        color: #000000 !important; /* Black Text */
        border: 1px solid #2E7D32 !important;
    }
    
    /* Focus state */
    .stTextArea textarea:focus {
        background-color: #FFFFFF !important;
        border: 2px solid #2E7D32 !important;
    }
</style>
""", unsafe_allow_html=True)

try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("⚠️ API Key missing! Please set GOOGLE_API_KEY in st.secrets.")
        st.stop()
        
    genai.configure(api_key=api_key)

    @st.cache_resource
    def get_working_model():
        try:
            priority_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            available_models = [m.name.replace('models/', '') for m in genai.list_models()]
            
            for model in priority_models:
                if model in available_models:
                    return model
            return "gemini-1.5-flash" 
        except Exception:
            return "gemini-1.5-flash"

    model_name = get_working_model()
    model = genai.GenerativeModel(model_name)
    
except Exception as e:
    st.error(f"⚠️ Error configuring API: {e}")
    st.stop()

def get_gemini_response(prompt_text):
    try:
        with st.spinner(f"💪 Generating Plan (Using {model_name})..."):
            response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

st.markdown('<div class="main-header">💪 AI Fitness & Diet Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Customized routines and meal plans based on your biology and budget.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("👤 Your Profile")
    
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=10, max_value=100, value=20)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
    
    st.header("🎯 Goals")
    goal = st.selectbox("Primary Goal", [
        "Weight Loss (Fat Burn)", 
        "Muscle Gain (Hypertrophy)", 
        "General Fitness & Stamina", 
        "Athletic Performance"
    ])
    activity_level = st.select_slider("Activity Level", options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    
    st.header("🥗 Diet & Equipment")
    diet_pref = st.selectbox("Dietary Preference", [
        "Vegetarian", 
        "Non-Vegetarian", 
        "Vegan", 
        "Eggetarian", 
        "Keto",
        "Indian Standard (Roti/Rice based)"
    ])
    equipment = st.selectbox("Available Equipment", [
        "No Equipment (Home Workout)", 
        "Dumbbells Only", 
        "Full Gym Access"
    ])

tab1, tab2, tab3 = st.tabs(["🏋️ Workout Plan", "🥗 Meal Plan", "💡 Budget Tips"])

with tab1:
    st.subheader("Weekly Workout Routine")
    if st.button("Generate Workout Plan"):
        prompt = f"""
        Act as a professional fitness trainer. Create a 7-day workout plan for a {age}-year-old {gender} 
        weighing {weight}kg with the goal of {goal}.
        
        Constraints:
        - Equipment: {equipment}
        - Activity Level: {activity_level}
        
        Format the output as a clear schedule (Monday to Sunday). 
        Include sets and reps for each exercise.
        """
        st.markdown(get_gemini_response(prompt))

with tab2:
    st.subheader("Weekly Meal Plan")
    if st.button("Generate Diet Plan"):
        prompt = f"""
        Act as a nutritionist. Create a 7-day meal plan for a {age}-year-old {gender} 
        weighing {weight}kg with the goal of {goal}.
        
        Constraints:
        - Diet Type: {diet_pref}
        - Cultural Preference: Include local accessible foods.
        
        Format:
        Provide a daily breakdown for Breakfast, Lunch, Snack, and Dinner.
        Include approximate calorie and protein counts for the day.
        """
        st.markdown(get_gemini_response(prompt))

with tab3:
    st.subheader("Shopping List & Tips")
    if st.button("Get Shopping List"):
        prompt = f"""
        Based on a {diet_pref} diet for {goal}, provide:
        1. A student-friendly grocery shopping list (Budget-friendly).
        2. 3 Tips to save money on food while hitting protein goals.
        3. 3 Tips for consistency in training.
        """
        st.markdown(get_gemini_response(prompt))