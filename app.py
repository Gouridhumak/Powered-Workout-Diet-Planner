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
    .main-header { font-size: 3rem; color: #2E7D32; text-align: center; font-weight: 800; margin-bottom: 1rem; }
    .sub-header { font-size: 1.2rem; color: #555; text-align: center; margin-bottom: 2rem; }
    .stButton>button { width: 100%; background-color: #4CAF50; color: white; font-weight: bold; border-radius: 10px; height: 50px; }
    .stTextArea textarea { background-color: #E8F5E9 !important; color: #000000 !important; border: 1px solid #2E7D32 !important; }
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
    def get_valid_model():
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    return m.name
            return "models/gemini-1.5-flash" 
        except Exception as e:
            return "models/gemini-pro"

    model_name = get_valid_model()
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
st.markdown(f'<div class="sub-header">Customized routines. Running on: {model_name}</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("👤 Your Profile")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", 10, 100, 20)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    st.header("🎯 Goals")
    goal = st.selectbox("Goal", ["Weight Loss", "Muscle Gain", "Fitness"])
    st.header("🥗 Details")
    diet = st.selectbox("Diet", ["Veg", "Non-Veg", "Vegan"])
    equip = st.selectbox("Equipment", ["None", "Dumbbells", "Gym"])

tab1, tab2 = st.tabs(["🏋️ Workout", "🥗 Diet"])

with tab1:
    if st.button("Generate Workout"):
        prompt = f"Create a workout plan for {age}yo {gender}, {weight}kg. Goal: {goal}. Equipment: {equip}."
        st.markdown(get_gemini_response(prompt))

with tab2:
    if st.button("Generate Diet"):
        prompt = f"Create a meal plan ({diet}) for {age}yo {gender}, {weight}kg. Goal: {goal}."
        st.markdown(get_gemini_response(prompt))
