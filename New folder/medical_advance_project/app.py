import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from data import generate_patient_data
from model import (
    FEATURE_COLUMNS,
    build_clinical_explanation,
    predict_patient_risk,
    train_risk_model,
)


st.set_page_config(page_title="Medical Advance Project", layout="wide")


@st.cache_data
def load_data():
    return generate_patient_data()


@st.cache_resource
def load_model(dataframe: pd.DataFrame):
    return train_risk_model(dataframe)


data = load_data()
model, metrics, feature_importance = load_model(data)

st.title("Medical Advance Project")
st.caption(
    "Advanced healthcare analytics demo with predictive disease risk scoring."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Patients", len(data))
col2.metric("High-Risk Rate", f"{data['disease_risk'].mean() * 100:.1f}%")
col3.metric("Model Accuracy", f"{metrics['accuracy'] * 100:.1f}%")
col4.metric("ROC AUC", f"{metrics['roc_auc']:.2f}")

tab1, tab2, tab3 = st.tabs(
    ["Patient Risk Predictor", "Population Dashboard", "Model Insights"]
)

with tab1:
    st.subheader("Single-Patient Assessment")

    with st.form("patient_form"):
        c1, c2, c3 = st.columns(3)
        age = c1.slider("Age", 18, 90, 50)
        bmi = c2.slider("BMI", 16.0, 45.0, 27.0)
        systolic_bp = c3.slider("Systolic BP", 90, 210, 128)

        c4, c5, c6 = st.columns(3)
        diastolic_bp = c4.slider("Diastolic BP", 55, 130, 82)
        glucose = c5.slider("Glucose", 65, 260, 110)
        cholesterol = c6.slider("Cholesterol", 110, 360, 190)

        c7, c8, c9 = st.columns(3)
        heart_rate = c7.slider("Heart Rate", 45, 140, 78)
        oxygen_saturation = c8.slider("Oxygen Saturation", 82.0, 100.0, 97.0)
        physical_activity = c9.slider("Physical Activity (days/week)", 0, 7, 3)

        c10, c11, c12 = st.columns(3)
        smoking = c10.selectbox("Smoking", [0, 1], format_func=lambda x: "Yes" if x else "No")
        family_history = c11.selectbox(
            "Family History", [0, 1], format_func=lambda x: "Yes" if x else "No"
        )
        stress_level = c12.slider("Stress Level", 1, 10, 5)

        submitted = st.form_submit_button("Predict Risk")

    if submitted:
        patient_input = pd.DataFrame(
            [
                {
                    "age": age,
                    "bmi": bmi,
                    "systolic_bp": systolic_bp,
                    "diastolic_bp": diastolic_bp,
                    "glucose": glucose,
                    "cholesterol": cholesterol,
                    "heart_rate": heart_rate,
                    "oxygen_saturation": oxygen_saturation,
                    "physical_activity": physical_activity,
                    "smoking": smoking,
                    "family_history": family_history,
                    "stress_level": stress_level,
                }
            ]
        )

        probability, label = predict_patient_risk(model, patient_input)
        explanation = build_clinical_explanation(patient_input)

        st.success(
            f"Predicted risk level: {label} ({probability * 100:.1f}% probability)"
        )
        st.dataframe(patient_input[FEATURE_COLUMNS], use_container_width=True)

        fig, ax = plt.subplots(figsize=(8, 4))
        top_factors = explanation.head(8).sort_values("impact_score")
        ax.barh(top_factors["factor"], top_factors["impact_score"], color="#c2410c")
        ax.set_title("Clinical Factor Contribution")
        ax.set_xlabel("Impact Score")
        st.pyplot(fig)

with tab2:
    st.subheader("Population Health Dashboard")

    dashboard_col1, dashboard_col2 = st.columns(2)

    with dashboard_col1:
        age_bins = pd.cut(
            data["age"], bins=[18, 30, 45, 60, 75, 90], right=False
        ).value_counts().sort_index()
        fig_age, ax_age = plt.subplots(figsize=(7, 4))
        ax_age.bar(age_bins.index.astype(str), age_bins.values, color="#0369a1")
        ax_age.set_title("Patient Age Distribution")
        ax_age.tick_params(axis="x", rotation=20)
        st.pyplot(fig_age)

    with dashboard_col2:
        avg_metrics = data[
            ["bmi", "systolic_bp", "glucose", "cholesterol", "oxygen_saturation"]
        ].mean()
        fig_avg, ax_avg = plt.subplots(figsize=(7, 4))
        ax_avg.bar(avg_metrics.index, avg_metrics.values, color="#059669")
        ax_avg.set_title("Average Clinical Measures")
        ax_avg.tick_params(axis="x", rotation=20)
        st.pyplot(fig_avg)

    high_risk_patients = data[data["disease_risk"] == 1].copy()
    st.write("High-risk patient sample")
    st.dataframe(high_risk_patients.head(20), use_container_width=True)

with tab3:
    st.subheader("Model Performance and Feature Importance")

    metric_cols = st.columns(4)
    metric_cols[0].metric("Accuracy", f"{metrics['accuracy'] * 100:.1f}%")
    metric_cols[1].metric("Precision", f"{metrics['precision'] * 100:.1f}%")
    metric_cols[2].metric("Recall", f"{metrics['recall'] * 100:.1f}%")
    metric_cols[3].metric("ROC AUC", f"{metrics['roc_auc']:.2f}")

    fig_imp, ax_imp = plt.subplots(figsize=(8, 5))
    ax_imp.barh(
        feature_importance["feature"][::-1],
        feature_importance["importance"][::-1],
        color="#7c3aed",
    )
    ax_imp.set_title("Feature Importance")
    ax_imp.set_xlabel("Importance")
    st.pyplot(fig_imp)

    st.write("Generated dataset preview")
    st.dataframe(data.head(25), use_container_width=True)

st.info(
    "Educational prototype only. Use validated clinical data and regulatory review before real-world deployment."
)
