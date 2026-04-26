🚗 Car Price Prediction using Machine Learning

A complete Machine Learning web application that predicts the selling price of a car based on features like year, showroom price, kilometers driven, fuel type, transmission, and ownership.

Built using Python, Scikit-learn, Pandas, and Streamlit with a clean interactive UI.

🚀 Live Demo

https://codealphacar-price-prediction-gzyratlyfmhhyvgdvh6kyx.streamlit.app/

📌 Project Overview

This project predicts used car prices using a trained Machine Learning model.

It helps users:

Estimate car resale value instantly
Understand price factors
Visualize dataset insights
Experience a real-world ML product
✨ Features

✔ 🔍 Auto searchable car selection
✔ 💰 Real-time price prediction
✔ 📊 Dataset insights dashboard
✔ 🚗 Car image display
✔ 📈 Price trend visualization
✔ 🧠 Machine Learning regression model
✔ 🎨 Clean and modern Streamlit UI
✔ ⚡ Instant predictions

🛠️ Tech Stack
Python 🐍
Pandas 📊
NumPy 🔢
Scikit-learn 🤖
Matplotlib 📈
Streamlit 🌐
Joblib 💾

📁 Project Structure
car-price-prediction/
│── app.py
│── train.py
│── requirements.txt
│── README.md
│
├── data/
│   ├── car_data.csv
│
├── model/
│   ├── model.pkl
│   ├── columns.pkl
│
├── assets/
│   ├── car_images/
│       ├── swift.jpg
│       ├── fortuner.jpg
│       ├── innova.jpg

📊 Dataset Features
Feature	Description
Car Name	Brand & model name
Year	Manufacturing year
Present Price	Showroom price (Lakhs)
Driven Kms	Distance driven
Fuel Type	Petrol / Diesel / CNG
Seller Type	Dealer / Individual
Transmission	Manual / Automatic
Owner	Number of previous owners
Selling Price	Target variable

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/car-price-prediction.git
cd car-price-prediction
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Train Model
python train.py
5️⃣ Run Application
streamlit run app.py

🤖 Machine Learning Model
Algorithm: Random Forest Regressor
Handles:
Non-linear relationships
Feature importance
High accuracy predictions

📈 Model Workflow
Load dataset
Data preprocessing
Feature encoding
Train-test split
Train Random Forest model
Save model using Joblib
Deploy using Streamlit


📊 Visualizations
Price distribution graph
Fuel type comparison
Car popularity insights
Trend analysis chart
🌍 Deployment

You can deploy this project using:

🔹 Streamlit Cloud
Push to GitHub
Connect repo
Deploy in 1 click
🔹 Hugging Face Spaces
Upload files
Select Streamlit app
🔮 Future Improvements

🔥 Add Deep Learning model
🔥 Real-time car image API
🔥 User login system
🔥 Download prediction report (PDF)
🔥 Mobile responsive UI
🔥 Cloud database integration

👨‍💻 Author
Anil Mali
📧 Email: smartanilmali234@gmail.com

🔗 GitHub: https://github.com/smartanilmali234-art

⭐ Support

If you like this project:

⭐ Star the repository
🍴 Fork it
🚀 Share with others
📜 License

This project is licensed under the MIT License.