import pandas as pd

def find_s(data):
    hypothesis = None

    for i in range(len(data)):
        if data.iloc[i, -1] == "Yes":   # positive example
            if hypothesis is None:
                hypothesis = data.iloc[i, :-1].tolist()
            else:
                for j in range(len(hypothesis)):
                    if hypothesis[j] != data.iloc[i, j]:
                        hypothesis[j] = "?"

    return hypothesis


# Load dataset
data = pd.read_csv("training_data.csv")

# Run Find-S
result = find_s(data)

print("Final Hypothesis:", result)