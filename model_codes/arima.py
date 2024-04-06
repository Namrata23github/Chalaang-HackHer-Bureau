from sklearn.neighbors import LocalOutlierFactor
import numpy as np

# Generate sample data
np.random.seed(42)
X = 0.3 * np.random.randn(100, 3)
print("X:", X)
X_outliers = np.random.uniform(low=-4, high=4, size=(20, 3))
print("X Outlier:", X_outliers)
X = np.vstack([X, X_outliers])

# Fit the model
clf = LocalOutlierFactor(n_neighbors=20) # You can adjust the number of neighbors
y_pred = clf.fit_predict(X)
print("y_pred:", y_pred)

# Negative LOF scores are outliers, positive scores are inliers
outlier_indices = np.where(y_pred == -1)[0]
inlier_indices = np.where(y_pred == 1)[0]

print("Outlier indices:", outlier_indices)
print("Inlier indices:", inlier_indices)
