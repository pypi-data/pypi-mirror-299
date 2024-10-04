# Example.py
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .cleaning import fill_missing, drop_duplicates, remove_outliers
from .visualization import plot_histogram, plot_scatter, plot_correlation_matrix
from .statistics import (
    calculate_mean,
    calculate_median,
    perform_ttest,
    calculate_standard_deviation,
    calculate_variance,
)

# Load your data
df = pd.read_csv('your_data.csv')

# Handle missing data
df = fill_missing(df, method='mean')

# Drop duplicates
df = drop_duplicates(df)

# Generate plots
plot_histogram(df, 'your_column')
plot_scatter(df, 'column_x', 'column_y')
plot_correlation_matrix(df)

# Perform statistical tests
mean_value = calculate_mean(df, 'your_column')
t_stat, p_value = perform_ttest(df['group1'], df['group2'])
