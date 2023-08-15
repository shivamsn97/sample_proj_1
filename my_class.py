# Create a class that can be called to fix the formatting of the csv in this dir (sample.csv) and return it as a df. 
# BONUS: Return the data grouped in the best manner you see fit.

import pandas as pd
import numpy as np

class CSVFormatter:
    def __init__(self, filename):
        self.filename = filename

    def fix_csv_format(self, missing_default=None):
        try:
            df = pd.read_csv(self.filename, thousands=',', na_values='', keep_default_na=False)
            
            df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
            
            columns2clean = ['Revenue', 'Profit', 'Cost', 'Expense', 'Income', 'Price', 'Salary', 'Investment']

            for col in columns2clean:
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)
                if missing_default is not None:
                    df[col].fillna(missing_default, inplace=True)
                else:
                    df[col].fillna(df[col].mean(), inplace=True)
            
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
if __name__ == '__main__':
    filename = 'sample.csv'
    csv_formatter = CSVFormatter(filename)
    formatted_df = csv_formatter.fix_csv_format(missing_default=None)  # Change missing_default value as needed
    print(formatted_df)
