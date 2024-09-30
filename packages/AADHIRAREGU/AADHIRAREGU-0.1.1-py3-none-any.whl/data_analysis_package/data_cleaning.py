import pandas as pd

def handle_missing_data(df, method="drop", fill_value=None):
    """
    Handle missing data in a pandas DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.
    method (str): How to handle missing data ('drop' or 'fill').
    fill_value: Value to fill missing data if method is 'fill'.

    Returns:
    pd.DataFrame: DataFrame with missing values handled.
    """
    if method == "drop":
        return df.dropna()
    elif method == "fill":
        return df.fillna(fill_value)
    else:
        raise ValueError("Invalid method: choose 'drop' or 'fill'")
