import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Iris Classifier", layout="wide")

st.title("🌸 Iris Flower Classification System")

# ---------------- CSV UPLOAD ----------------
uploaded_file = st.file_uploader("📂 Upload Iris CSV file", type=["csv"])

if uploaded_file is None:
    st.info("👆 Please upload a CSV file to continue")
    st.stop()

# ---------------- LOAD DATA ----------------
df = pd.read_csv(uploaded_file)

# Clean dataset
if "Id" in df.columns:
    df = df.drop("Id", axis=1)

df.columns = df.columns.str.strip()
df["Species"] = df["Species"].str.strip()

# ---------------- FEATURES & TARGET ----------------
X = df.drop("Species", axis=1)
y = df["Species"]

# ---------------- TRAIN MODELS ----------------
rf = RandomForestClassifier()
svm = SVC(probability=True)
knn = KNeighborsClassifier()

rf.fit(X, y)
svm.fit(X, y)
knn.fit(X, y)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Settings")

model_choice = st.sidebar.selectbox(
    "Choose Model",
    ["Random Forest", "SVM", "KNN"]
)

# Accuracy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
st.sidebar.success(f"✅ Accuracy: {accuracy:.2f}")

# ---------------- INPUT ----------------
st.subheader("📥 Enter Flower Features")

sepal_length = st.slider("Sepal Length", float(X.iloc[:,0].min()), float(X.iloc[:,0].max()), 5.1)
sepal_width = st.slider("Sepal Width", float(X.iloc[:,1].min()), float(X.iloc[:,1].max()), 3.5)
petal_length = st.slider("Petal Length", float(X.iloc[:,2].min()), float(X.iloc[:,2].max()), 1.4)
petal_width = st.slider("Petal Width", float(X.iloc[:,3].min()), float(X.iloc[:,3].max()), 0.2)

input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

# ---------------- VISUALIZATION ----------------
st.subheader("📊 Data Visualization")

fig, ax = plt.subplots()
sns.scatterplot(x=X.columns[0], y=X.columns[1], hue=y, data=df, ax=ax)
st.pyplot(fig)

# ---------------- CONFUSION MATRIX ----------------
st.subheader("📊 Confusion Matrix")

cm = confusion_matrix(y_test, y_pred)

fig_cm, ax_cm = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax_cm)
st.pyplot(fig_cm)

# ---------------- PREDICTION ----------------
if st.button("🚀 Predict"):

    if model_choice == "Random Forest":
        model = rf
    elif model_choice == "SVM":
        model = svm
    else:
        model = knn

    prediction = model.predict(input_data)
    result = prediction[0]

    st.success(f"🌼 Prediction: {result}")

    # ---------------- PROBABILITY ----------------
    try:
        probs = model.predict_proba(input_data)[0]

        prob_df = pd.DataFrame({
            "Species": model.classes_,
            "Probability": probs
        })

        st.subheader("📈 Prediction Probability")
        st.bar_chart(prob_df.set_index("Species"))
    except:
        st.info("Probability not available for this model")

    # ---------------- IMAGE OUTPUT ----------------
    st.subheader("🌼 Flower Image")

    image_urls = {
        "Iris-setosa": "https://upload.wikimedia.org/wikipedia/commons/5/56/Iris_setosa.jpg",
        "Iris-versicolor": "https://upload.wikimedia.org/wikipedia/commons/4/41/Iris_versicolor_3.jpg",
        "Iris-virginica": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Iris_virginica.jpg"
    }

    st.image(image_urls[result], width=300)
    