import streamlit as st
import pandas as pd
import numpy as np
from huggingface_hub import hf_hub_download
import joblib
import streamlit as st
import base64

# ------------------ Page Configuration ------------------
st.set_page_config(page_title="GenPredict", layout="wide")

# ------------------ Paths ------------------
logo_path = "Logo.png"

# ------------------ Colors ------------------
main_bg_color = "#ECF3F0"

# ------------------ Convert image to Base64 ------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_of_bin_file(logo_path)

# ------------------ CSS ------------------
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {main_bg_color};
    }}

    /* logo*/
    .logo-box {{
        position: fixed;
        top: 20px;
        left: 20px;
        width: 160px;
        height: 160px;
        padding: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }}
    .logo-box img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }}

    /* Project Name*/
    .center-text {{
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        margin-top: 50px;
        color: #064635;
    }}

    /* Text */
    .bottom-text {{
        text-align: center;
        font-size: 24px;
        margin-top: 20px;
        color: #064635;
    }}

    </style>

<!-- Topic -->
<div class="center-text">GenPredict</div>

<!-- Logo -->
<div class="logo-box">
    <img src="data:image/png;base64,{logo_base64}">
</div>

""", unsafe_allow_html=True)

try:
    _ = st.session_state.keep_graphics
except AttributeError:
    st.session_state.keep_graphics = False

REPO_ID = "shahdt/voting_model"
MODEL_FILENAME = "model.pkl"

def fix_monotonic_cst_issue(model):
    if hasattr(model, 'estimators_'):
        for estimator in model.estimators_:
            if hasattr(estimator, 'tree_') and not hasattr(estimator, 'monotonic_cst'):
                estimator.monotonic_cst = None
            if hasattr(estimator, 'estimators_'):
                for sub_estimator in estimator.estimators_:
                    if hasattr(sub_estimator, 'tree_') and not hasattr(sub_estimator, 'monotonic_cst'):
                        sub_estimator.monotonic_cst = None
    return model

@st.cache_resource
def load_model():
    model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=MODEL_FILENAME,
        repo_type="model"
    )
    model = joblib.load(model_path)
    model = fix_monotonic_cst_issue(model)
    return model

@st.cache_resource
def load_preprocessor():
    return joblib.load("preprocessor.pkl")

class_names = [
    "Mitochondrial genetic inheritance disorders",
    "Multifactorial genetic inheritance disorders",
    "Single-gene inheritance diseases"
]

def predict_ensemble_model(model, X_processed_test):
    # تطبيق إصلاح إضافي قبل التنبؤ
    model = fix_monotonic_cst_issue(model)

    y_pred = model.predict(X_processed_test)
    y_pred_labels = np.take(class_names, y_pred.astype(int), mode='raise')

    if hasattr(X_processed_test, 'shape'):
        if len(y_pred_labels) == 1:
            return y_pred_labels[0]
        else:
            return y_pred_labels
    else:
        return y_pred_labels

st.title("Patient Data Form")

with st.form("patient_form"):
    st.subheader("Patient Information")

    patient_age = st.number_input("Patient Age", min_value=0, max_value=120, step=1)
    genes_mother_side = st.selectbox("Genes Mother Side", ["Yes", "No"])
    inherited_from_father = st.selectbox("Inherited from father", ["Yes", "No"])
    maternal_gene = st.selectbox("Maternal gene", ["Yes", "No"])
    paternal_gene = st.selectbox("Paternal gene", ["Yes", "No"])
    blood_cell_count = st.number_input("Blood cell count (mcL)", min_value=0.0)
    mother_age = st.number_input("Mother Age", min_value=0, max_value=120, step=1)
    father_age = st.number_input("Father Age", min_value=0, max_value=120, step=1)
    status = st.selectbox("Status", ["Alive", "Deceased"])
    respiratory_rate = st.selectbox("Respiratory Rate", ["Normal", "Tachypnea"])
    heart_rates = st.selectbox("Heart Rates", ["Normal", "Tachycardia"])
    test_4 = st.checkbox("Test 4 (checked = 1, unchecked = 0)")
    follow_up = st.selectbox("Follow Up", ["Low", "High"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    folic_acid = st.selectbox("Folic Acid", ["Yes", "No"])
    maternal_illness = st.selectbox("Maternal Illness", ["Yes", "No"])
    assisted_conception = st.selectbox("Assisted Conception", ["Yes", "No"])
    history_pregnancies = st.selectbox("History Previous Pregnancies", ["Yes", "No"])
    previous_abortion = st.number_input("Previous Abortion", min_value=0, max_value=4, step=1)
    birth_defects = st.selectbox("Birth Defects", ["Singular", "Multiple"])
    white_blood_cell = st.number_input("White Blood Cell (µL)", min_value=0.0)
    blood_test_result = st.selectbox("Blood Test Result", ["normal", "inconclusive", "slightly abnormal", "abnormal"])

    st.subheader("Symptoms")
    symptom_1 = st.checkbox("Symptom 1")
    symptom_2 = st.checkbox("Symptom 2")
    symptom_3 = st.checkbox("Symptom 3")
    symptom_4 = st.checkbox("Symptom 4")
    symptom_5 = st.checkbox("Symptom 5")

    submitted = st.form_submit_button("Submit")

if submitted:
    data = {
        'Patient_Age': np.int64(patient_age),
        'Genes_Mother_Side': genes_mother_side,
        'Inherited_from_father': inherited_from_father,
        'Maternal_gene': maternal_gene,
        'Paternal_gene': paternal_gene,
        'Blood_cell_count(mcL)': float(blood_cell_count),
        'Mother_Age': mother_age,
        'Father_Age': father_age,
        'Status': status,
        'Respiratory_Rate_Breaths_Min': respiratory_rate,
        'Heart_Rates': heart_rates,
        'Test_4': bool(test_4),
        'Follow_Up': follow_up,
        'Gender': gender,
        'Folic_Acid': folic_acid,
        'Maternal_Illness': maternal_illness,
        'Assisted_Conception': assisted_conception,
        'History_Previous_Pregnancies': history_pregnancies,
        'Previous_Abortion': np.int64(previous_abortion),
        'Birth_Defects': birth_defects,
        'White_Blood_Cell': float(white_blood_cell),
        'Blood_Test_Result': blood_test_result,
        'Symptom_1': bool(symptom_1),
        'Symptom_2': bool(symptom_2),
        'Symptom_3': bool(symptom_3),
        'Symptom_4': bool(symptom_4),
        'Symptom_5': bool(symptom_5)
    }

    df_row = pd.DataFrame([data])
    st.success("Form submitted successfully!")
    st.dataframe(df_row)

    # load preprocessor and model
    pipe = load_preprocessor()
    voting_model = load_model()

    input_transformed = pipe.transform(df_row)

    y_pred_label = predict_ensemble_model(voting_model, input_transformed)

    if y_pred_label == "Mitochondrial genetic inheritance disorders":
        prediction_class = ("Mitochondrial genetic inheritance disorders", "🧪", "#DC2626")
    elif y_pred_label == "Multifactorial genetic inheritance disorders":
        prediction_class = ("Multifactorial genetic inheritance disorders", "🧬🧪", "#16A34A")
    elif y_pred_label == "Single-gene inheritance diseases":
        prediction_class = ("Single-gene inheritance diseases", "🧬", "#2563EB")
    else:
        prediction_class = (y_pred_label, "❓", "#6B7280")

    class_name, emoji, color = prediction_class

    st.markdown(f"""
    <div style="text-align:center; margin-top:40px;">
        <div style="
            display: inline-block;
            padding: 20px;
            border-radius: 12px;
            background-color:#F1F5F9;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
            max-width:500px;
        ">
            <h3>Predicted Diagnosis: <span style="color:{color};">{class_name} {emoji}</span></h3>
            <p style="color:#334155; font-size:16px;">
                This prediction is based on the AI model analysis. Please consult a geneticist for confirmation.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
