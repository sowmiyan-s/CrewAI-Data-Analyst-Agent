import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Sample dataset
np.random.seed(0)
df = pd.DataFrame({
    'Age': np.random.randint(20, 60, 100),
    'Salary': np.random.randint(50000, 150000, 100),
    'Experience': np.random.randint(1, 10, 100),
    'Department': np.random.choice(['Sales', 'Marketing', 'IT'], 100)
})

# Replace missing values in the 'Age' column with the mean age
df['Age'].fillna(df['Age'].mean(), inplace=True)

# Scale the 'Salary' column using Min-Max Scaler
scaler = MinMaxScaler()
df['Salary'] = scaler.fit_transform(df[['Salary']])

# Drop duplicate rows based on all columns
df.drop_duplicates(inplace=True)

# One-hot encode the 'Department' column
pd.get_dummies(df, columns=['Department'], drop_first=True, inplace=True)

# Remove rows with outliers in the 'Experience' column using IQR method
Q1 = df['Experience'].quantile(0.25)
Q3 = df['Experience'].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df['Experience'] < (Q1 - 1.5 * IQR)) | (df['Experience'] > (Q3 + 1.5 * IQR)))]

# Plotting
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.scatterplot(x='Age', y='Salary', data=df)
plt.title('Age vs Salary')

plt.subplot(1, 3, 2)
sns.scatterplot(x='Age', y='Experience', data=df)
plt.title('Age vs Experience')

plt.subplot(1, 3, 3)
sns.scatterplot(x='Salary', y='Experience', data=df)
plt.title('Salary vs Experience')

plt.tight_layout()
plt.show()