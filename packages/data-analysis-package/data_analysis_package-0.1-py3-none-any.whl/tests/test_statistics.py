# tests/test_statistics.py

import pandas as pd
import pytest
from data_analysis.statistics import correlation, t_test

def test_correlation():
    df = pd.DataFrame({'A': [5, 8, 3], 'B': [4, 9, 6]})
    # Calculate the expected correlation manually or using Pandas
    expected_corr = df['A'].corr(df['B'])
    assert correlation(df, 'A', 'B') == pytest.approx(expected_corr, rel=1e-2)

def test_t_test():
    sample1 = [1, 2, 3]
    sample2 = [4, 5, 6]
    t_stat, p_value = t_test(sample1, sample2)
    assert t_stat is not None
    assert p_value is not None
