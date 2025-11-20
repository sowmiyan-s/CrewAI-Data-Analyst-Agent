import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Assuming we have a DataFrame named 'df'
# Replace missing values in the 'age' column with the mean age
df['age'] = df['age'].fillna(df['age'].mean())

# Normalize the 'income' column by scaling it between 0 and 1
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['income'] = scaler.fit_transform(df[['income']])

# Remove duplicate rows based on all columns
df = df.drop_duplicates()

# One-hot encode the 'gender' and 'occupation' columns
df = pd.get_dummies(df, columns=['gender', 'occupation'])

# Remove rows with outlier values in the 'income' column using the IQR method
Q1 = df['income'].quantile(0.25)
Q3 = df['income'].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df['income'] < (Q1 - 1.5 * IQR)) | (df['income'] > (Q3 + 1.5 * IQR)))]

# Create a scatter plot
plt.figure(figsize=(10,6))
sns.scatterplot(x='age', y='income', data=df)
plt.title('Scatter plot of age vs income')
plt.xlabel('Age')
plt.ylabel('Income')
plt.show()