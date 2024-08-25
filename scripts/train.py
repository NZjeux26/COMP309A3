import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import FastICA
import joblib

def preprocess_data(df, target_column):
    """
    Preprocess the data by handling missing values, encoding categorical features,
    and separating features from the target.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - target_column (str): The column name of the target variable.

    Returns:
    - X (pd.DataFrame): The features.
    - y (pd.Series): The target labels.
    - categorical_features (list): List of categorical feature names.
    - numeric_features (list): List of numeric feature names.
    - label_encoder (LabelEncoder): The label encoder for the target.
    """
    # Drop rows with missing target values
    df = df.dropna(subset=[target_column])

    # Handle missing values in the features (e.g., fill with median for numeric)
    df = df.fillna(df.median(numeric_only=True))  # filling numeric columns
    df = df.fillna('unknown')  # filling categorical columns with 'unknown'

    # Separate features (X) and target (y)
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Identify categorical and numeric features
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    numeric_features = X.select_dtypes(exclude=['object']).columns.tolist()

    # Encode the target labels (if they are categorical)
    label_encoder = None
    if y.dtype == 'object':
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)

    return X, y, categorical_features, numeric_features, label_encoder

def create_pipeline(categorical_features, numeric_features, n_components=10):
    """
    Create a pipeline for preprocessing and modeling, including ICA.

    Parameters:
    - categorical_features (list): List of categorical feature names.
    - numeric_features (list): List of numeric feature names.
    - n_components (int): Number of components for ICA (default: 10).

    Returns:
    - pipeline (Pipeline): A pipeline that preprocesses the data and trains the model.
    """
    # Preprocessing for numeric features
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('ica', FastICA(n_components=n_components, random_state=42))
    ])

    # Preprocessing for categorical features
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Create the pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    return pipeline

def grid_search_tuning(pipeline, X_train, y_train):
    """
    Perform Grid Search to tune hyperparameters of the Random Forest model.

    Parameters:
    - pipeline (Pipeline): The pipeline containing preprocessing and the model.
    - X_train (pd.DataFrame): The training features.
    - y_train (pd.Series): The training target labels.

    Returns:
    - best_model (Pipeline): The pipeline with the best found parameters.
    """
    param_grid = {
        'preprocessor__num__ica__n_components': [5, 10],  # Added ICA components tuning
        'classifier__n_estimators': [100, 200, 300],
        'classifier__max_depth': [None, 10, 20, 30],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4],
    }

    grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)

    print(f"Best parameters found: {grid_search.best_params_}")
    return grid_search.best_estimator_

def evaluate_model(model, X, y, label_encoder=None):
    """
    Evaluate the model on a given dataset and print the classification report.

    Parameters:
    - model (Pipeline): The trained model pipeline.
    - X (pd.DataFrame): The features to evaluate on.
    - y (pd.Series): The true labels.
    - label_encoder (LabelEncoder): The encoder used for the target labels (if any).

    Returns:
    - None
    """
    y_pred = model.predict(X)

    if label_encoder:
        y = label_encoder.inverse_transform(y)
        y_pred = label_encoder.inverse_transform(y_pred)

    print("Model Evaluation:")
    print(classification_report(y, y_pred))
    print(f"Accuracy: {accuracy_score(y, y_pred):.4f}")

def save_model(model, output_file):
    """
    Save the trained model to a file.

    Parameters:
    - model (Pipeline): The trained model pipeline.
    - output_file (str): The file path to save the model.

    Returns:
    - None
    """
    joblib.dump(model, output_file)
    print(f"Model saved to {output_file}")

# Example usage:
train_file = '../data/train_data.csv'
val_file = '../data/val_data.csv'
test_file = '../data/test_data.csv'
model_file = '../models/random_forest_genre_model_pipeline_with_ica.pkl'

# Load the datasets
df_train = pd.read_csv(train_file)
df_val = pd.read_csv(val_file)
df_test = pd.read_csv(test_file)

# Preprocess the data
target_column = 'genre'  # Replace 'genre' with the actual name of your genre column
X_train, y_train, categorical_features, numeric_features, label_encoder = preprocess_data(df_train, target_column)
X_val, y_val, _, _, _ = preprocess_data(df_val, target_column)
X_test, y_test, _, _, _ = preprocess_data(df_test, target_column)

# Create the pipeline with ICA
pipeline = create_pipeline(categorical_features, numeric_features)

# Perform hyperparameter tuning using the training set
best_model = grid_search_tuning(pipeline, X_train, y_train)

# Evaluate the tuned model on the validation set
print("\nValidation Set Evaluation:")
evaluate_model(best_model, X_val, y_val, label_encoder)

# After tuning, perform the final evaluation on the test set
print("\nTest Set Evaluation:")
evaluate_model(best_model, X_test, y_test, label_encoder)

# Save the trained model
save_model(best_model, model_file)