import streamlit as st
import pandas as pd

st.title("Find-S Algorithm")

st.write("Upload your CSV file")

uploaded_file = st.file_uploader("Choose CSV", type="csv")

def find_s(data):
    hypothesis = None

    for i in range(len(data)):
        if data.iloc[i, -1] == "Yes":
            if hypothesis is None:
                hypothesis = data.iloc[i, :-1].tolist()
            else:
                for j in range(len(hypothesis)):
                    if hypothesis[j] != data.iloc[i, j]:
                        hypothesis[j] = "?"

    return hypothesis

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.write("### Dataset")
    st.dataframe(data)

    result = find_s(data)

    st.write("### Final Hypothesis")
    st.success(result)
else:
    st.warning("Please upload a CSV file")