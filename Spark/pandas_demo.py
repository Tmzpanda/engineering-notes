import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('filename.csv')

# Trim the spaces from the column names
df.columns = df.columns.str.strip()

# Trim the spaces from the column values
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Find the highest salary for each department
highest_salaries = df.groupby('department')['salary'].max()

# Print the results
print(highest_salaries)
