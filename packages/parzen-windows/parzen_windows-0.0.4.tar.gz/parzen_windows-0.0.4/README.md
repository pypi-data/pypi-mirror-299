## parzen-windows

Description: A Python module that will take input (training data) and estimate the underlying probability density function with Parzen Windows





To build run 
`python3 -m build` 
while in the `parzen_windows` directory
then navigate to `./dist` directory


Then run 

`twine upload dist/*`
or 
`twine upload --skip-existing dist/*`


#### Quick Start

```
from parzenwindow.pdf_estimate import ParzenWindow
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Generate 1,000,000 random values for X
X = np.random.uniform(-10, 10, size=1_000_000)

# Generate Y based on a quadratic function of X, with some added noise
noise = np.random.normal(0, 2, size=1_000_000)
Y = 0.5 * X**2 - 3 * X + 5 + noise

# Create a Pandas DataFrame
df = pd.DataFrame({'X': X, 'Y': Y})


# Instantiate ParzenWindow class
pw = ParzenWindow(training_data_df = df)

#Pick a test point to find pdf of
test_point = df.iloc[0,:].to_numpy()
print(f"Getting the pdf value of {test_point}")
print(pw.pdf(new_datapoint=test_point, hypercube_length = 0.01))

```