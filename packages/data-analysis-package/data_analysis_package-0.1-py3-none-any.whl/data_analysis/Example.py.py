# Example of using the modules
import pandas as pd
from data_analysis.cleaning import fill_missing, drop_duplicates
from data_analysis.visualization import plot_histogram, plot_scatter, plot_correlation_matrix
from data_analysis.statistics import calculate_mean, perform_ttest

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
