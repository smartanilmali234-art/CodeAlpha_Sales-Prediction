import joblib
import pandas as pd

# -------------------------------
# Load Model
# -------------------------------
model = joblib.load("model/model.pkl")

# -------------------------------
# Take User Input
# -------------------------------
try:
    tv = float(input("Enter TV Advertising Budget: "))
    radio = float(input("Enter Radio Advertising Budget: "))
    newspaper = float(input("Enter Newspaper Advertising Budget: "))
except:
    print("❌ Please enter valid numeric values!")
    exit()

# -------------------------------
# Create Input DataFrame
# -------------------------------
input_data = pd.DataFrame({
    "TV": [tv],
    "Radio": [radio],
    "Newspaper": [newspaper]
})

# -------------------------------
# Predict
# -------------------------------
prediction = model.predict(input_data)[0]

# -------------------------------
# Output Result
# -------------------------------
print("\n📊 Predicted Sales:", round(prediction, 2))

# -------------------------------
# Simple Insight
# -------------------------------
if tv > radio and tv > newspaper:
    print("💡 Insight: TV advertising contributes the most.")

elif radio > tv:
    print("💡 Insight: Radio advertising is performing strongly.")

else:
    print("💡 Insight: Newspaper ads are influencing sales.")