from scipy import stats

def perform_t_test(sample1, sample2):
    """
    Perform a t-test on two samples.

    Parameters:
    sample1 (list): The first sample.
    sample2 (list): The second sample.

    Returns:
    tuple: t-statistic and p-value.
    """
    t_stat, p_value = stats.ttest_ind(sample1, sample2)
    return t_stat, p_value
