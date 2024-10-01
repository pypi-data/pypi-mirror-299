import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def prepare_data(filepath, target_column=None, numerical_columns=None, categorical_columns=None,
                 test_size=0.2, random_state=42, binary_threshold=2, low_cardinality_threshold=10):
    """
    Prepares the dataset for training by handling missing values, encoding categorical variables, and splitting the data.

    Args:
        data (str or pandas.DataFrame): The input dataset, either as a file path (e.g., 'data.csv') or a pandas DataFrame.
        target_column (str, optional): The name of the target column. If not provided, the last column is assumed as the target. Defaults to None.
        task (str, optional): The type of task ('classification', 'regression'). Defaults to 'classification'.

    Returns:
        tuple: A tuple of (X, y) where X is the feature matrix and y is the target vector.

    Usage:
        >>> from mkyz import data_processing as dp
        >>> data = dp.prepare_data('winequality-red.csv', target_column='quality')
    """

    # Load the dataset
    df = pd.read_csv(filepath)

    # If target_column is not specified, use the last column
    if target_column is None:
        target_column = df.columns[-1]
        print(f"No target column specified. Using the last column '{target_column}' as the target.")

    # Ensure the target column exists in the dataframe
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in the dataframe.")

    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Initialize lists if not provided
    if numerical_columns is None:
        numerical_columns = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if categorical_columns is None:
        categorical_columns = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # Automatically detect additional categorical columns based on heuristics
    potential_categorical = []
    for col in numerical_columns.copy():  # Iterate over a copy since we might modify the list
        unique_values = X[col].nunique()
        if unique_values <= binary_threshold:
            print(f"Column '{col}' has {unique_values} unique values. Treating as binary categorical.")
            potential_categorical.append(col)
        elif unique_values <= low_cardinality_threshold:
            print(f"Column '{col}' has {unique_values} unique values. Treating as low cardinality categorical.")
            potential_categorical.append(col)

    # Move identified categorical columns from numerical_columns to categorical_columns
    for col in potential_categorical:
        numerical_columns.remove(col)
        categorical_columns.append(col)

    # Display the final lists of numerical and categorical columns
    print(f"Numerical columns: {numerical_columns}")
    print(f"Categorical columns: {categorical_columns}")

    # Define preprocessing pipelines
    numerical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Combine preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(transformers=[
        ('num', numerical_pipeline, numerical_columns),
        ('cat', categorical_pipeline, categorical_columns)
    ])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Fit and transform the training data, transform the testing data
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    return X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns
