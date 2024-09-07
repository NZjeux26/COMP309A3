# ovo_classifier.py

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report

def main():
    # Load labeled training data from CSV
    df_train = pd.read_csv('../data/train_data.csv')

    # Separate features and target variable
    X_train = df_train.drop('genre', axis=1)  # Replace 'target' with your actual target column name
    y_train = df_train['genre']  # Replace 'target' with your actual target column name

    # Define which columns are categorical and which are numerical
    categorical_features = ['artist_name', 'track_name', 'mode', 'key']  # Replace with your actual categorical columns
    numerical_features = [col for col in X_train.columns if col not in categorical_features]

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

    # Define the model
    svc = SVC()

    # Create a pipeline that first preprocesses the data and then fits the model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', OneVsOneClassifier(svc))
    ])

    # Define the parameter grid for GridSearchCV
    param_grid = {
        'classifier__estimator__C': [0.1, 1, 10, 100],
        'classifier__estimator__kernel': ['linear', 'rbf'],
        'classifier__estimator__gamma': ['scale', 'auto']
    }

    # Use GridSearchCV to search for the best parameters
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, scoring='accuracy')

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, random_state=42,shuffle=True)

    # Fit the GridSearchCV to the training data
    grid_search.fit(X_train, y_train)

    # Print the best parameters found by GridSearchCV
    print("Best parameters found by GridSearchCV:")
    print(grid_search.best_params_)

    # Predict on the validation set using the best model
    y_pred = grid_search.best_estimator_.predict(X_val)

    # Evaluate the classifier
    print("Validation Results:")
    print(classification_report(y_val, y_pred))

    # Optionally, if you want to save the best model for later use:
    # from joblib import dump
    # dump(grid_search.best_estimator_, 'best_ovo_model.joblib')

if __name__ == '__main__':
    main()
