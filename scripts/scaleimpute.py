import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Load your datasets
train_data = pd.read_csv('../data/mega_full_processed.csv')  # Replace with your training data file path
test_data = pd.read_csv('../data/testing-data/testingFixed.csv')    # Replace with your test data file path

# Specify the target column and columns to exempt from imputation and scaling
target_column = 'genre'  # Replace with your actual target column name
exempt_columns = ['key', 'mode', 'time_signature', 'instance_id', 'track_id']  # Replace with columns to exempt

# Separate features and target from the training data
X_train = train_data.drop(columns=[target_column])
y_train = train_data[target_column]

# Identify numeric columns and categorical columns
numeric_cols = X_train.select_dtypes(include=np.number).columns
categorical_cols = X_train.select_dtypes(include=['object', 'category']).columns

# Ensure exempt columns are preserved in the final output
# Exempted columns must not be included in the imputation and scaling but should be in the final output
numeric_cols = [col for col in numeric_cols if col not in exempt_columns]
all_cols = list(set(numeric_cols + categorical_cols + exempt_columns))

# Initialize the SimpleImputer and StandardScaler
imputer = SimpleImputer(strategy='mean')  # You can also use 'median', 'most_frequent', or a constant value
scaler = StandardScaler()

# Apply imputation and scaling to the numeric columns (excluding exempt columns)
X_train_imputed = X_train.copy()
X_train_imputed[numeric_cols] = imputer.fit_transform(X_train[numeric_cols])
X_train_scaled = X_train_imputed.copy()
X_train_scaled[numeric_cols] = scaler.fit_transform(X_train_imputed[numeric_cols])

# Apply imputation to the test data (excluding exempt columns)
X_test = test_data.copy()
X_test_imputed = X_test.copy()
X_test_imputed[numeric_cols] = imputer.transform(X_test[numeric_cols])
X_test_scaled = X_test_imputed.copy()
X_test_scaled[numeric_cols] = scaler.transform(X_test_imputed[numeric_cols])

# Combine scaled numeric features with categorical features and exempted columns
X_train_final = pd.concat([X_train_scaled[all_cols], y_train.reset_index(drop=True)], axis=1)
X_test_final = X_test_scaled[all_cols]

# Save the scaled datasets
X_train_final.to_csv('megafullProIS.csv', index=False)
X_test_final.to_csv('testProIS.csv', index=False)

print("Training and test data have been imputed, scaled, and saved.")
