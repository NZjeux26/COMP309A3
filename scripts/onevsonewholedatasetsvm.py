import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import SVC

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
    df_train = pd.read_csv('../data/OOfull_processed.csv')

    # Separate features and target variable
    X_train = df_train.drop('genre', axis=1)  # Replace 'genre' with your actual target column name
    y_train = df_train['genre']  # Replace 'genre' with your actual target column name

    # Drop 'instance_id' before preprocessing
    X_train = X_train.drop(columns=['instance_id'])
    
    # Define which columns are categorical and which are numerical
    categorical_features = ['artist_name', 'track_name', 'mode', 'key']  # Replace with your actual categorical columns
    numerical_features = [col for col in X_train.columns if col not in categorical_features]

    # Create transformers for categorical and numerical features
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())  # Standardize numerical features
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))  # One-hot encode categorical features
    ])

    # Combine transformers into a preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Create the SVM classifier wrapped in OneVsOneClassifier
    svm_clf = OneVsOneClassifier(SVC(C=1, kernel='linear', gamma='scale', probability=True))

    # Create a pipeline that first preprocesses the data and then fits the model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', svm_clf)
    ])

    # Train the SVM model on the entire training set
    pipeline.fit(X_train, y_train)

    # Load unlabeled test data from CSV
    df_test = pd.read_csv('../data/testing-data/OvOTest_data.csv')
    
    # Drop 'instance_id' before preprocessing
    X_test = df_test.drop(columns=['instance_id'])

    # Predict on the unlabeled test set
    test_predictions = pipeline.predict(X_test)

    # Save predictions along with instance_id to a CSV file
    output = pd.DataFrame({'instance_id': df_test['instance_id'], 'genre': test_predictions})
    output.to_csv('../data/outputs/test_predictions_svm.csv', index=False)
    print("Test predictions saved to 'test_predictions_svm.csv'")

if __name__ == '__main__':
    main()
