# model_comparison.py

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, accuracy_score

def main():
    # Load labeled training data from CSV
    df_train = pd.read_csv('../data/OOfull_processed.csv')

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

    # Define models with a pipeline that first preprocesses the data
    models = {
        'SVM': Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', SVC())]),
        'Logistic Regression': Pipeline(steps=[('preprocessor', preprocessor),
                                               ('classifier', LogisticRegression(max_iter=1000))]),
        'Gradient Boosting': Pipeline(steps=[('preprocessor', preprocessor),
                                             ('classifier', GradientBoostingClassifier())]),
        'Naive Bayes': Pipeline(steps=[('preprocessor', preprocessor),
                                       ('classifier', GaussianNB())])
    }

    # Define parameter grids for each model
    param_grids = {
        'SVM': {
            'classifier__C': [0.1, 1, 10],
            'classifier__kernel': ['linear', 'rbf'],
            'classifier__gamma': ['scale', 'auto']
        },
        'Logistic Regression': {
            'classifier__C': [0.1, 1, 10],
            'classifier__solver': ['lbfgs', 'liblinear']
        },
        'Gradient Boosting': {
            'classifier__n_estimators': [100, 200,],
            'classifier__learning_rate': [0.1, 0.2,0.3],
            'classifier__max_depth': [3, 5, 10]
        },
        'Naive Bayes': {}
    }

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, random_state=42)

    best_models = {}
    for name, model in models.items():
        print(f"Performing GridSearchCV for {name}...")
        grid_search = GridSearchCV(model, param_grids[name], cv=5, n_jobs=-1, scoring='accuracy')
        grid_search.fit(X_train, y_train)
        best_models[name] = grid_search.best_estimator_
        print(f"Best parameters for {name}: {grid_search.best_params_}")

    # Compare models on the validation set
    results = []
    for name, model in best_models.items():
        y_pred = model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)
        results.append((name, accuracy))
        print(f"\n{name} Classification Report:\n")
        print(classification_report(y_val, y_pred))

    # Print summary of results
    print("\nModel Comparison:")
    for name, accuracy in results:
        print(f"{name}: Accuracy = {accuracy:.4f}")

if __name__ == '__main__':
    main()
