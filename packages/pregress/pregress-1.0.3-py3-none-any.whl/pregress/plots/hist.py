import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm as normal_dist

def hist(vector, bins=30, color="blue", norm=False, main="Histogram", xlab=None, ylab="Frequency", subplot = None):
    """
    Generates and prints a histogram for a given vector.

    Args:
        vector (array-like): Vector of numeric values.
        bins (int, optional): Number of bins for the histogram.
        color (str, optional): Color of the histogram.
        norm (bool, optional): Whether to include a normal distribution line.
        main (str, optional): Title for the histogram.
        xlab (str, optional): Label for the x-axis.
        ylab (str, optional): Label for the y-axis.

    Returns:
        None. The function creates and shows the histogram.
    """
    # Get the variable name if xlab is not provided
    if xlab is None:
        # If the vector is a Series, use its name
        if isinstance(vector, pd.Series):
            xlab = vector.name
        else:
            # Otherwise, try to get the variable name from the caller's local variables
            callers_local_vars = inspect.currentframe().f_back.f_locals.items()
            xlab = [var_name for var_name, var_val in callers_local_vars if var_val is vector]
            xlab = xlab[0] if xlab else 'Variable'

    # Clear any existing plots
    plt.clf()
    plt.close()

    # Create the histogram
    sns.histplot(vector, bins=bins, kde=False, color=color, edgecolor='black')

    if norm:
        mean = np.mean(vector)
        std = np.std(vector)
        x = np.linspace(min(vector), max(vector), 100)
        p = normal_dist.pdf(x, mean, std)
        bin_width = np.diff(np.histogram(vector, bins=bins)[1])[0]
        plt.plot(x, p * (len(vector) * bin_width), 'k', linewidth=2)

    # Set titles and labels
    plt.title(main)
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    # Show the plot if subplot is not specified or if it is the last subplot
    if subplot is None:
        plt.show()
        plt.clf()
        plt.close()





