# ovo_classifier.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report

def main():
    # Load data from CSV
    # Replace 'your_data.csv' with your actual CSV file path
    df = pd.read_csv('../data/OOfull_processed.csv')

    # Separate features and target variable
    X = df.drop('genre', axis=1)  # Replace 'target' with your actual target column name
    y = df['genre']  # Replace 'target' with your actual target column name

    # Define which columns are categorical and which are numerical
    categorical_features = ['artist_name', 'track_name', 'mode', 'key']  # Replace with your actual categorical columns
    numerical_features = [col for col in X.columns if col not in categorical_features]

    # Create transformers for categorical and numerical features
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values with the mean
        ('scaler', StandardScaler())  # Standardize numerical features
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute missing values with the most frequent value
        ('onehot', OneHotEncoder(handle_unknown='ignore'))  # One-hot encode categorical features
    ])

    # Combine transformers into a preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Create a pipeline that first preprocesses the data and then fits the model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', OneVsOneClassifier(SVC(C=1,kernel='linear', gamma='scale',probability=True)))
    ])

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42,shuffle=True)

    # Train the classifier
    pipeline.fit(X_train, y_train)

    # Predict on the test set
    y_pred = pipeline.predict(X_test)

    # Evaluate the classifier
    print(classification_report(y_test, y_pred))

if __name__ == '__main__':
    main()