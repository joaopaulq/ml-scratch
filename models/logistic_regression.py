import numpy as np

from models.util import sigmoid, loss


class LogisticRegression:
    """Class for the Logistic Regression model.
    
    Attributes:
        w: The weights. NumPy array.
        b: The intercept term. Float.

    Example of usage:
        > clf = LogisticRegression()
        > clf.fit(X_train, y_train)
        > clf.predict(X_valid)
    """

    def __init__(self):
        self.w, self.b = None, 0


    def fit(self, X, y, max_iter=1000, verbose=False):
        """Run the Newton-Raphson method.
        
        Args:
            X: Training examples of shape (m, n). NumPy array.
            y: Training examples labels of shape (m,). NumPy array.
            max_iter: Maximum number of iterations. Integer.
            verbose: Print loss values during training. Boolean.
        """
        m, n = X.shape
        self.w = np.zeros(n) # Start the weights with the zero vector.
        
        for i in range(max_iter):
            # Make a prediction.
            h_x = self.predict(X)
            
            # Compute the gradient.
            dJw = (X.T @ (y - h_x)) / m # Derivative of loss wrt weights.
            dJb = np.sum(y - h_x) / m # Derivative of loss wrt bias.
            d2Jb = -m # Second derivative of loss wrt bias.
            
            # Compute the hessian and its inverse.
            D = np.diag(h_x * (1 - h_x))
            H = (X.T @ D @ X) / m 
            H_inv = np.linalg.pinv(H)
            
            # Update rule.
            prev_w, prev_b = self.w, self.b
            self.w = self.w - H_inv @ dJw
            self.b = self.b - (dJb / d2Jb)
            
            # Stop if converges.
            if np.allclose(prev_w, self.w) and np.isclose(prev_b, self.b):
                break
            
            if verbose and i % 10 == 0:
                J = loss(y, h_x, measure='cross-entropy')
                print(f"Loss on iteration {i}: {J}")
        

    def predict(self, X):
        """Make a prediction given new inputs.

        Args:
            X: Inputs of shape (m, n). NumPy array.

        Returns:
            h_x: Predictions of shape (m,). NumPy array.
        """
        z = X @ self.w + self.b
        return sigmoid(z) # Apply the sigmoid function.