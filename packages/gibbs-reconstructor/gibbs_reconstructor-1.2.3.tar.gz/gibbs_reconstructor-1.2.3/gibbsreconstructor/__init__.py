import numpy as np


class GibbsReconstructor:
    """
    A class to perform Gibbs reconstruction of missing data in a dataset.

    This class uses a regularized approach to estimate the coefficients for reconstructing
    missing values in the input data matrix using Gibbs sampling methods.

    Attributes:
        alpha (float): Regularization parameter for the Ridge regression.

    Methods:
        fit(X): Fits the model to the input data matrix X.
        predict(z): Predicts missing values in the input array z.
    """

    def __init__(self, alpha=0):
        """
        Initializes the GibbsReconstructor with a given regularization parameter.

        Parameters:
            alpha (float): Regularization parameter. Default is 0.
        """
        self.alpha = alpha

    def fit(self, X):
        """
        Fits the GibbsReconstructor model to the input data.

        This method computes the coefficients based on the provided dataset X,
        taking into account the regularization to handle overfitting.

        Parameters:
            X (ndarray): A 2D NumPy array of shape (n_samples, n_features) representing the input data.

        Returns:
            None: The coefficients are stored in the instance variable coef_.
        """
        n, p = X.shape

        X = np.hstack((X, np.ones((n, 1))))

        XtX = X.T @ X
        XtX.flat[:: p + 2] += n * self.alpha

        XtX_inv = np.linalg.inv(XtX)

        np.fill_diagonal(XtX, 0)

        XtX_inv_XtX = XtX_inv @ XtX

        self.coef_ = (
            XtX_inv_XtX
            - XtX_inv * ((np.diag(XtX_inv_XtX) / np.diag(XtX_inv)))[np.newaxis, :]
        )

    def predict(self, z):
        """
        Predicts missing values in the input array z using the fitted model.

        This method reconstructs the data based on the learned coefficients.

        Parameters:
            z (ndarray): A 2D NumPy array containing the data with potential missing values (NaNs).

        Returns:
            ndarray: A reconstructed 2D NumPy array with estimated values for the missing entries.
        """
        p = z.shape[1]
        missing_idxs = np.where(np.isnan(z[0]))

        z[:, missing_idxs] = 0

        A = np.eye(p + 1)
        for k in missing_idxs:
            A[k] = self.coef_[:, k].T @ A
        A = A[:p, :p]
        A[missing_idxs, missing_idxs] -= 1

        return np.linalg.solve(A, z.T).T
