import streamlit as st
import pickle
import numpy as np

# 1. Model Loading with Cache
@st.cache_resource
def load_model():
    # model2.pkl file open karat aahe
    with open('model2.pkl', 'rb') as file:
        return pickle.load(file)

model = load_model()

# 2. Page Configuration & Design
st.set_page_config(page_title="Heart Health Monitor", page_icon="🏥", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #e63946;
        color: white;
        height: 3em;
        font-size: 18px;
    }
    div[data-testid="stForm"] {
        border-radius: 15px;
        background-color: #f8f9fa;
        padding: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. UI Header
st.title("🏥 Patient Risk Analysis System")
st.write("Clinical data bhara ani SVC model dwara analysis paha.")

# 4. Input Form (User Friendly)
with st.form("health_form"):
    st.subheader("📝 Clinical Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Patient Profile**")
        age = st.slider("Age (Vay)", 1, 100, 50)
        sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Male" if x == 1 else "Female")
        smoking = st.selectbox("Smoking?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        diabetes = st.selectbox("Diabetes?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        anaemia = st.selectbox("Anaemia?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        hbp = st.selectbox("High BP?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    with col2:
        st.write("**Lab Metrics**")
        ef = st.number_input("Ejection Fraction (%)", 0, 100, 35)
        sc = st.number_input("Serum Creatinine", 0.1, 15.0, 1.2)
        ss = st.number_input("Serum Sodium", 100, 150, 135)
        cpk = st.number_input("CPK Enzyme", 0, 10000, 500)
        platelets = st.number_input("Platelets", 10000, 1000000, 250000)
        time = st.number_input("Follow-up (Days)", 1, 300, 100)

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("Start Analysis")

# 5. Result Section
if submit:
    # Model features kramat (order) tayar karne
    features = np.array([[age, anaemia, cpk, diabetes, ef, hbp, platelets, sc, ss, sex, smoking, time]])
    
    # Prediction logic
    prediction = model.predict(features)
    
    st.divider()
    st.subheader("🔍 Clinical Outcome")
    
    if prediction[0] == 1:
        st.error("### 🚨 HIGH RISK DETECTED")
        st.write("Patient chya metrics madhe heart failure chi shakyata diste. Tattadine doctor cha salla ghya.")
    else:
        st.success("### ✅ LOW RISK DETECTED")
        st.write("Patient che metrics sadhya surakshit range madhe aahet.")

st.caption("Disclaimer: He ek AI tool aahe. Final diagnosis sathi Doctor cha salla garjecha aahe.")
