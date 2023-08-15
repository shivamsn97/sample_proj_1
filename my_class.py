# Create a class that can be called to fix the formatting of the csv in this dir (sample.csv) and return it as a df. 
# BONUS: Return the data grouped in the best manner you see fit.

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class CSVFormatter:
    def __init__(self, filename):
        self.filename = filename
        self.df = None

    def clean_data(self):
        if self.df:
            return self.df
        try:
            df = pd.read_csv(self.filename, thousands=',', na_values='', keep_default_na=False)
            
            df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
            
            columns2clean = ['Revenue', 'Profit', 'Cost', 'Expense', 'Income', 'Price', 'Salary', 'Investment']
            fcols = ['Revenue', 'Profit', 'Cost']

            for col in columns2clean:
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)
            
            # Clean rows with only one missing value
            for index, row in df.iterrows():
                num_missing = row[fcols].isnull().sum()
                if num_missing == 1:
                    missing_col = row[fcols].isnull().idxmax()
                    non_missing_cols = row[fcols].dropna().index.tolist()
                    if missing_col == 'Income':
                        df.at[index, missing_col] = sum(row[col] for col in non_missing_cols) - row['Expense'] - row['Profit']
                    elif missing_col == 'Revenue':
                        df.at[index, missing_col] = row['Profit'] + row['Cost']
                    elif missing_col == 'Cost':
                        df.at[index, missing_col] = row['Revenue'] - row['Profit']

            # Perform regression imputation for rows with more than one missing value
            for index, row in df.iterrows():
                num_missing = row[columns2clean].isnull().sum()
                X = np.array([columns2clean.index(col) for col in columns2clean if not np.isnan(row[col])]).reshape(-1, 1)
                y = np.array([row[col] for col in columns2clean if not np.isnan(row[col])])
                
                if len(X) > 0 and len(y) > 0:
                    model = LinearRegression()
                    model.fit(X, y)
                    
                    for col in columns2clean:
                        if np.isnan(row[col]):
                            predicted_value = model.predict([[columns2clean.index(col)]])
                            df.at[index, col] = predicted_value[0]
                            
            df['ID'] = range(1, len(df) + 1)
            self.df = df
            return df
        except Exception as e:
            raise

    def group_data(self):
        df = self.df
        if df is None:
            raise Exception("Dataframe is not initialized. Please call clean_data() method first.")
        try:
            grouped_df = df.groupby('Master', as_index=False).agg({
                'Revenue': 'sum',
                'Profit': 'sum',
                'Cost': 'sum',
                'Expense': 'sum',
                'Income': 'sum',
                'Price': 'sum',
                'Salary': 'sum',
                'Investment': 'sum'
            })
            return grouped_df
        except Exception as e:
            raise

# Usage
# if __name__ == '__main__':
filename = 'sample.csv'
csv_formatter = CSVFormatter(filename)
cleaned_df = csv_formatter.clean_data()
grouped_df = csv_formatter.group_data()

if grouped_df is not None:
    print(grouped_df)
else:
    print("Error occurred while processing the CSV file.")
