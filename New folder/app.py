import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Locally Weighted Regression (LWR)")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# If no file → use default dataset
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Dataset Preview:")
    st.write(data.head())

    X = data.iloc[:, 0].values
    y = data.iloc[:, 1].values
else:
    st.write("Using default dataset")
    np.random.seed(0)
    X = np.linspace(-3, 3, 100)
    y = np.sin(X) + np.random.normal(scale=0.3, size=X.shape)

# Add bias
X_train = np.c_[np.ones(len(X)), X]

# Tau slider
tau = st.slider("Select Tau (τ)", 0.1, 2.0, 0.5)

# LWR function
def lwr_predict(X_train, y_train, x_query, tau):
    m = X_train.shape[0]
    W = np.eye(m)

    for i in range(m):
        diff = x_query - X_train[i]
        W[i, i] = np.exp(-np.dot(diff, diff) / (2 * tau**2))

    theta = np.linalg.pinv(X_train.T @ W @ X_train) @ X_train.T @ W @ y_train
    return x_query @ theta

# Predictions
y_pred = np.array([lwr_predict(X_train, y, X_train[i], tau) for i in range(len(X))])

# Plot
fig, ax = plt.subplots()
ax.scatter(X, y, label="Data Points")
ax.plot(X, y_pred, label="LWR Curve")
ax.set_title("Locally Weighted Regression")
ax.legend()

st.pyplot(fig)