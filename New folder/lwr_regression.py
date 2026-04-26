import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate dataset
np.random.seed(0)
X = np.linspace(-3, 3, 100)
y = np.sin(X) + np.random.normal(scale=0.3, size=X.shape)

# Step 2: Add bias (intercept term)
X_train = np.c_[np.ones(len(X)), X]

# Step 3: Define LWR function
def lwr_predict(X_train, y_train, x_query, tau):
    m = X_train.shape[0]
    W = np.eye(m)

    # Compute weights
    for i in range(m):
        diff = x_query - X_train[i]
        W[i, i] = np.exp(-np.dot(diff, diff) / (2 * tau**2))

    # Compute theta
    XTWX = X_train.T @ W @ X_train
    
    # To avoid singular matrix error
    theta = np.linalg.pinv(XTWX) @ X_train.T @ W @ y_train

    # Prediction
    return x_query @ theta

# Step 4: Predict values
tau = 0.5
y_pred = []

for i in range(len(X)):
    y_pred.append(lwr_predict(X_train, y, X_train[i], tau))

y_pred = np.array(y_pred)

# Step 5: Plot graph
plt.scatter(X, y, label="Data Points")
plt.plot(X, y_pred, label="LWR Curve")
plt.title("Locally Weighted Regression")
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.show()