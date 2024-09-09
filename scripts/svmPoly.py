import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import classification_report

def main():
    # Load data from CSV
    df = pd.read_csv('../data/train_data.csv')

    # Separate features and target variable
    X = df.drop(['genre','mode','key','duration_ms'], axis=1)  # Drop the columns you don't need
    
    y = df['genre']  # Target variable

    # Define which columns are categorical and which are numerical
    categorical_features = ['artist_name', 'track_name']  # Replace with your actual categorical columns
    numerical_features = [col for col in X.columns if col not in categorical_features]

    # Create transformers for categorical and numerical features
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values with the mean
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),  # Generate polynomial features of degree 2
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
        ('classifier', SVC(C=1, kernel='rbf', gamma='scale', probability=True))
    ])

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

    # Train the classifier
    pipeline.fit(X_train, y_train)

    # Predict on the test set
    y_pred = pipeline.predict(X_test)

    # Evaluate the classifier
    print(classification_report(y_test, y_pred))

if __name__ == '__main__':
    main()
