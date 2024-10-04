import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from scipy import stats
from .ultils import seasonal_decompose


def Multivariate_Density(data, features=None, n_features=5):    
    """
    Create a Pair plot with Multivariate Density plot for some selected features.

    Parameters:
        data: pandas DataFrame. Input dataset used to create the Pair plot.
        features: str, optional. List of features to generate the Pair plot. If None, features will be selected randomly.
        n_features: int, optional. Number of random features. Default is 5.

    Returns:
        Draws the pairplot.
    """

    # If no features are provided, select them randomly
    if features is None:
        features = np.random.choice(data.columns, size=min(len(data.columns),n_features), replace=False).tolist()
    # Select the chosen features into a DataFrame
    selected_data = data[features]
    # Create a Pair plot with the selected features
    sns.pairplot(selected_data, diag_kind='kde', kind='reg', plot_kws={'line_kws':{'color':'red'}})

    plt.suptitle('Multivariate Density Plots', y=1.02)
    plt.show()


def Isolation_Forest(data, contamination=0.003, random_state=42, figure_size=(10, 8)):
    
    """
    Use Isolation Forest to find outliers in the data.

    Parameters:
        data: pandas Series or array, shape (n_samples). Time-series data.
        contamination: float, optional (default=0.003). The proportion of outliers in the dataset.
        random_state: int or RandomState, optional (default=42). Controls the random seed for reproducibility.
        figure_size: tuple, optional (default=(10, 8)). Size of the plot.

    Return:
        A plot representing the outliers in the data.
    """

    # Initialize the IsolationForest model
    clf = IsolationForest(contamination=contamination, random_state=random_state)
    # Fit the model and predict outliers
    outliers = clf.fit_predict(data)
    # Extract the outlier values from the scaled data
    outliers_data = data[outliers == -1]
    outlier_indices = np.where(outliers == -1)[0]

    # Create figure and axis objects
    fig, ax = plt.subplots(figsize=figure_size)

    # Plot the original data
    ax.plot(data.index, data, c='blue', label='Time Series Data')
    ax.scatter(data.index[outlier_indices], outliers_data, c='red', label='Outlier')
    ax.set_title('Isolation Forest Outlier Detection')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.legend()

    return fig, ax


def IQR(data, threshold=1.5, figure_size=(10, 8)):
    
    """
    Use IQR to detect outliers in the data.

    Parameters:
        data: pandas Series, shape (n_samples). Input data, e.g., closing prices or returns.
        threshold: float, optional (default=1.5). Threshold for deciding whether a value is an outlier. 
                   Values outside the range (Q1 - threshold * IQR, Q3 + threshold * IQR) are considered outliers.
        figure_size: tuple, optional (default=(10, 8)). Size of the plot.

    Returns:
        A plot representing the outliers in the data.
    """

    # Calculate the first and third quantile
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    # Calculate the IQR
    iqr = q3 - q1

    # Calculate the lower and upper bounds to detect outliers
    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr

    # Find the outliers
    outliers = data[(data < lower_bound) | (data > upper_bound)]

    # Plot the original data along with the detected outliers
    fig, ax = plt.subplots(figsize=figure_size)

    ax.plot(data.index, data, c='blue', label='Normal')
    ax.scatter(outliers.index, outliers, c='red', label='Outliers')
    ax.set_title('IQR Outlier Detection')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.legend()

    return fig, ax


def MAD(data, threshold=3.5, figsize=(10, 8)):
    
    """
    Use MAD (Median Absolute Deviation) to detect outliers in the data.

    Parameters:
        data: pandas Series, shape (n_samples,). Input data, e.g., closing prices or returns.
        threshold: float, optional (default=3.5). Threshold for outlier detection. Values with absolute deviation 
                   from the median greater than threshold * MAD are considered outliers.
        figsize: tuple, optional (default=(10, 8)). Size of the plot.

    Returns:
        A plot representing the outliers in the data.
    """

    # Calculate the median
    median = np.median(data)

    # Calculate MAD
    mad = stats.median_abs_deviation(data)

    # Calculate the threshold value
    threshold_value = threshold * mad

    # Detect the outliers
    outliers = []
    outliers_idx = []
    for idx, val in enumerate(data):
        if np.abs(val - median) > threshold_value:
            outliers.append(val)
            outliers_idx.append(data.index[idx])

    # Plot the original data along with the detected outliers
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(data.index, data, color='b', label='Original Data')
    ax.scatter(outliers_idx, outliers, color='r', marker='x', label='Outliers')
    ax.set_ylabel('Value')
    ax.set_title('Time Series Data with Outliers Detected (MAD Method)')
    ax.legend()
    ax.grid(True)

    return fig, ax


def Seasonal_Decomposition(data, model={'additive', 'multiplicative'}, figsize=(10, 8), period=12):
    
    """
    Plot seasonal decomposition.

    Parameters:
    data: pandas Series, shape (n_samples). Input data, e.g., closing prices or returns.
    model: {'additive', 'multiplicative'}, optional (default='additive'). Type of seasonal decomposition to use.
    figsize: tuple, optional (default=(10, 8)). Size of the plot.
    period: int, optional. Period of the data, if known.

    Returns:
        A plot showing the components of Seasonal Decomposition.
    """

    # Perform seasonal decomposition
    result = seasonal_decompose(data, model=model, period=period)
    
    # Plot the decomposition components
    plt.subplot(411)
    plt.plot(result.observed, label='Observed')
    plt.legend(loc='best')

    plt.subplot(412)
    plt.plot(result.trend, label='Trend')
    plt.legend(loc='best')

    plt.subplot(413)
    plt.plot(result.seasonal, label='Seasonal')
    plt.legend(loc='best')

    plt.subplot(414)
    plt.plot(result.resid, label='Residual')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.show()