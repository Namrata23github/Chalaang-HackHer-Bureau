import numpy as np
from sklearn.neighbors import LocalOutlierFactor
import scipy.sparse
def predict(data, num_neighbors = 20):
    # Handle case when dataset is too small
    print(len(data))
    # Fit the model
    clf = LocalOutlierFactor(n_neighbors=num_neighbors)
    y_pred = clf.fit_predict(data)

    # Negative LOF scores are outliers, positive scores are inliers
    outlier_indices = np.where(y_pred == -1)[0]
    inlier_indices = np.where(y_pred == 1)[0]

    return y_pred


