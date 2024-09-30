import sys
import os
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_analysis_package import handle_missing_data

def test_handle_missing_data():
    df = pd.DataFrame({
        'A': [1, 2, None, 4],
        'B': [5, None, None, 8]
    })

    # Test drop method
    cleaned_df = handle_missing_data(df, method="drop")
    assert cleaned_df.shape == (2, 2), "Drop method failed"
    print("Drop method passed")

    # Test fill method
    filled_df = handle_missing_data(df, method="fill", fill_value=0)
    assert filled_df.isna().sum().sum() == 0, "Fill method failed"
    print("Fill method passed")

# Run the test
if __name__ == "__main__":
    test_handle_missing_data()
    print("All tests passed!")
