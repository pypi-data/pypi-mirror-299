import unittest
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Ensure the package is found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_analysis_package.data_visualization import plot_histogram

class TestDataVisualization(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'A': [1, 2, 2, 3, 4, 4, 4, 5, 6],
            'B': [5, 6, 7, 8, 9, 10, 11, 12, 13]
        })

    def test_plot_histogram(self):
        try:
            plot_histogram(self.df, 'A')
            plt.close()  # Close the plot after testing
        except Exception as e:
            self.fail(f"plot_histogram raised {type(e).__name__} unexpectedly: {e}")

    def test_invalid_column(self):
        with self.assertRaises(ValueError):
            plot_histogram(self.df, 'C')  # 'C' does not exist in df

if __name__ == '__main__':
    unittest.main()
