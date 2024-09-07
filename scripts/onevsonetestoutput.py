# ovo_classifier.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
# Custom transformer to drop columns

class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.drop(columns=self.columns)
    
def main():
    # Load labeled training data from CSV
    # Replace 'train_data.csv' with your actual labeled training CSV file path
    df_train = pd.read_csv('../data/OOfull_processed.csv')

    # Separate features and target variable
    X_train = df_train.drop('genre', axis=1)  # Replace 'target' with your actual target column name
    y_train = df_train['genre']  # Replace 'target' with your actual target column name

    # Drop 'instance_id' before preprocessing
    X_train = X_train.drop(columns=['instance_id'])
    
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


    # Create a pipeline that first preprocesses the data and then fits the model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', OneVsOneClassifier(SVC(C=1,kernel='linear', gamma='scale',probability=True)))
    ])

    # Split the data into training and test sets
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, random_state=42)

    # Train the classifier
    pipeline.fit(X_train, y_train)

    # Predict on the validation set
    y_pred = pipeline.predict(X_val)

    # Evaluate the classifier
    print("Validation Results:")
    print(classification_report(y_val, y_pred))

    # Load unlabeled test data from CSV
    # Replace 'test_data.csv' with your actual unlabeled test CSV file path
    df_test = pd.read_csv('../data/testing-data/OvOTest_data.csv')
    
    # Predict on the unlabeled test set
    test_predictions = pipeline.predict(df_test)

    # Save predictions along with instance_id to a CSV file
    output = pd.DataFrame({'instance_id': df_test['instance_id'], 'Prediction': test_predictions})
    output.to_csv('../data/outputs/test_predictions4.csv', index=False)
    print("Test predictions saved to 'test_predictions4.csv'")

if __name__ == '__main__':
    main()
