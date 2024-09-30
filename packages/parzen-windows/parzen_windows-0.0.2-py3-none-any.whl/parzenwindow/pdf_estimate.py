""" 
    Author: Ian Meyer (Contact: imeyer [at symbol] unomaha dot edu)
    Description: The premise is simple: put data in, use Parzen window to get pdf estimate for a new datapoint. 
"""

import numpy as np
import pandas as pd
import scipy
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt





class ParzenWindow:
    def __init__(self, training_data_df:pd.DataFrame):
        """Class involved in deploying Parzen windows on a dataset.
        Upon initialization we require 
        
        `training_data_df` : pd.DataFrame - an array of solely numeric values. Each row is assumed to be a datapoint (vector) in the sample space R^n
        
        """
        self.df = training_data_df
        self.df_numpy = df.to_numpy()
        

    def get_gaussian_kernel_fn(self):
        "Return the Gaussian Multivariate Kernel function with mean 0 and unit covariance."

        #Get mean, assuming each row in df is a datapoint in R^n
        mu = np.zeros(self.df.shape[1])
        covariance_matrix = np.eye(self.df.shape[1])

        #Get multivariate normal distribution
        kernel = multivariate_normal(mean = mu, cov=covariance_matrix, allow_singular=False)

        return kernel.pdf
    
    def get_square_kernel_fn(self):
        """Return the square kernel function is a hypercube of unit length centered at origin. 
        Any vectors that lie outside of hypercube obtain value 0 and inside value 1"""

        def square_kernel_fn(x:np.ndarray) -> list:
            """
            
            -- Parameters --
            `x` : np.ndarray is assumed to be the dataframe of all training datapoints adjusted by the new_input_vector and divided by the hypercube length"""
            center = np.zeros(self.df.shape[1])
            unit_side_len = 1
            # Check if all components in each row have absolute value less than unit_side_len / 2
            condition = np.all(np.abs(x) < unit_side_len / 2, axis=1)
            
            # Return 1 if the condition is True for a row, otherwise 0
            result = np.where(condition, 1, 0)

            return result.tolist()

        return square_kernel_fn




    def pdf(self, new_datapoint:np.ndarray, hypercube_length:float, kernel_selection:str = "gaussian"):
        """Run pdf estimate on new_datapoint. Returns a float
        
        -- Parameters --\n
        `new_datapoint` : np.ndarray to run our estimate on, based off the training data given to `ParzenWindow` at initialization\n
        `hypercube_length` : float. A hyperparameter that determines how wide to make the hypercube\n
        `kernel_selection` : str one of "gaussian" or "square" \n
        
        
        """

        assert kernel_selection in ["gaussian", "square"]

        #Total number of datapoints
        N = self.df_numpy.shape[0]

        #Determine dimension R^?
        dimensions = self.df_numpy.shape[1]

        #Obtain volume of hypercube
        volume = hypercube_length**dimensions

        kernel = self.get_gaussian_kernel_fn() if kernel_selection == "gaussian" else self.get_square_kernel_fn()

        
        adjusted_datapoints = (self.df_numpy - new_datapoint)/hypercube_length
        sum_of_kernels_pdfs = np.array(kernel(x = adjusted_datapoints))

        #Adjust by number of datapoints and volume
        sum_of_kernels_pdfs =  np.divide(sum_of_kernels_pdfs, N)
        sum_of_kernels_pdfs =  np.divide(sum_of_kernels_pdfs, volume)


        return sum_of_kernels_pdfs.sum()




if __name__ == "__main__":
    # Generate 1,000,000 random values for X
    X = np.random.uniform(-10, 10, size=1_000_000)

    # Generate Y based on a quadratic function of X, with some added noise
    noise = np.random.normal(0, 2, size=1_000_000)
    Y = 0.5 * X**2 - 3 * X + 5 + noise

    # Create a Pandas DataFrame
    df = pd.DataFrame({'X': X, 'Y': Y})
    pw = ParzenWindow(df = df)


    test_point = df.iloc[0,:].to_numpy()
    print(f"Getting the pdf value of {test_point}")
    print(pw.pdf(new_datapoint=test_point, hypercube_length= 0.8))

    # Define the range for both x and y axes
    x = np.linspace(-20, 20, 50)  # 100 points from -10 to 10
    y = np.linspace(-20, 20, 50)  # 100 points from -10 to 10

    # Create the meshgrid
    X,Y = np.meshgrid(x, y)
    # Stack the X and Y components into vectors for g
    points = np.column_stack([X.ravel(), Y.ravel()])

    Z = []
    for point in points:
        Z.append(pw.pdf(new_datapoint=point, hypercube_length= 0.8, kernel_selection="square"))
        print(point)

    Z = np.array(Z).reshape((50,50))
    # Plotting the function g as a 3D surface
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    ax.plot_surface(X, Y, Z, cmap='viridis')

    # Add labels
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('g(X, Y)')
    ax.set_title('3D Surface Plot of g(x, y) = sin(sqrt(x^2 + y^2))')

    # Show the plot
    plt.show()