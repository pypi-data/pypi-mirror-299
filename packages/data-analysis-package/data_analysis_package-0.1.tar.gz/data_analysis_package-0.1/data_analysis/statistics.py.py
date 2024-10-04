import pandas as pd
from scipy import stats

def correlation(df, col1, col2):
    """Compute correlation between two columns.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    col1 (str): The name of the first column.
    col2 (str): The name of the second column.

    Returns:
    float: The Pearson correlation coefficient between the two columns.
    """
    return df[col1].corr(df[col2])

def t_test(sample1, sample2):
    """Perform independent t-test between two samples.

    Parameters:
    sample1 (list or array): The first sample.
    sample2 (list or array): The second sample.

    Returns:
    tuple: The t-statistic and p-value of the test.
    """
    t_stat, p_value = stats.ttest_ind(sample1, sample2)
    return t_stat, p_value
