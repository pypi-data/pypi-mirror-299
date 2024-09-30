import matplotlib.pyplot as plt
import pandas as pd

def plot_histogram(df, column, bins=10):
    """
    Plot a histogram of a specified column in a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column (str): The column name to plot.
    bins (int): Number of bins for the histogram.

    Returns:
    None
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        
    plt.hist(df[column], bins=bins, edgecolor='black')
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()
