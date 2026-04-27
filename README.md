# 📊 Sales Prediction using Machine Learning
  
LIVE LINK:s
https://codealphasales-prediction-jlm6itpedbhurajfsz5od2.streamlit.app/

## 🚀 Overview

This project predicts **future sales** based on advertising spend across different channels such as **TV, Radio, and Newspaper**.
It uses machine learning models to analyze how marketing investments impact sales performance.

---

## 🎯 Objectives

* Predict sales based on advertising budget
* Analyze impact of different advertising channels
* Build an interactive dashboard for real-time prediction
* Provide actionable business insights

---

## 🧠 Technologies Used

* Python
* Pandas, NumPy
* Scikit-learn
* Matplotlib
* Streamlit
* Joblib

---

## 📁 Project Structure

```
sales-prediction/
│
├── data/
│   └── sales_data.csv
│
├── model/
│   ├── train.py
│   └── model.pkl
├── app.py
├── predict.py
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

The dataset contains advertising spend across multiple channels:

| Feature   | Description                  |
| --------- | ---------------------------- |
| TV        | TV advertising budget        |
| Radio     | Radio advertising budget     |
| Newspaper | Newspaper advertising budget |
| Sales     | Sales generated              |

---

## ⚙️ How It Works

1. Data is cleaned and preprocessed
2. Features (TV, Radio, Newspaper) are used to train a model
3. A machine learning model predicts sales
4. Results are displayed via CLI and web app

---

## 🏋️ Model Used

* Random Forest Regressor
* Pipeline with preprocessing

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 2️⃣ Train the model

```
python model/train.py
```

---

### 3️⃣ Run prediction (CLI)

```
python predict.py
```

---

### 4️⃣ Run web app

```
streamlit run app.py
```

---

## 📈 Features

* Real-time sales prediction
* Interactive dashboard
* Visualization of ad spend
* Feature importance analysis
* Business insights

---

## 💡 Key Insights

* Sales are highly influenced by advertising spend
* TV advertising often has the highest impact
* Multi-channel strategy improves prediction accuracy

---

## 📌 Future Improvements

* Add more features (region, seasonality)
* Use advanced models (XGBoost)
* Deploy the app online
* Add user-uploaded datasets

---

## 🤝 Contribution

Feel free to fork this repository and improve it.

---

## 📬 Contact
Email:smartanilmali234@gmail.com
github:smartanilmali234-art

---

## ⭐ Acknowledgment

This project is created as part of a machine learning internship task.

---
# CodeAlpha_Sales-Prediction
