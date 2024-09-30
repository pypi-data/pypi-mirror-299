import unittest
import sys
import os

# Ensure the package is found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from data_analysis_package.statistical_analysis import perform_t_test

class TestStatisticalAnalysis(unittest.TestCase):

    def test_perform_t_test(self):
        sample1 = [1, 2, 3, 4, 5]
        sample2 = [2, 3, 4, 5, 6]
        
        t_stat, p_value = perform_t_test(sample1, sample2)
        
        # Check if the returned values are of correct type
        self.assertIsInstance(t_stat, float)
        self.assertIsInstance(p_value, float)

if __name__ == '__main__':
    unittest.main()
