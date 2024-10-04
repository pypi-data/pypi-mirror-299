from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import  mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import pickle

def ohe_encoding(x_train: pd.DataFrame, x_val: pd.DataFrame, cols: list):
    """
    Application of One Hot Encoding on training and validation sets.

    Parameters:
    - x_train: DataFrame containing training data
    - x_val: DataFrame containing validation data
    - cols: List of columns to apply One Hot Encoding to

    Returns:
    - x_train, x_val: DataFrames with One Hot Encoded columns added
    - ohe: Fitted OneHotEncoder instance
    """
    
    # Initialize the OneHotEncoder
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

    # Fit and Transform on Training Set
    ohe_train = ohe.fit_transform(x_train[cols])
    
    # Transform the Validation Set
    ohe_val = ohe.transform(x_val[cols])

    # Extracting feature names
    names = ohe.get_feature_names_out(cols)

    # Creating One Hot Encoded DataFrames
    ohe_train_df = pd.DataFrame(ohe_train, columns=names, index=x_train.index)
    ohe_val_df = pd.DataFrame(ohe_val, columns=names, index=x_val.index)

    # Concatenating the One Hot Encoded DataFrames with the original DataFrames
    x_train = pd.concat([x_train.drop(columns=cols), ohe_train_df], axis=1)
    x_val = pd.concat([x_val.drop(columns=cols), ohe_val_df], axis=1)

    return x_train, x_val, ohe

def encode_dates(df, date_col):

  df[date_col] = pd.to_datetime(df[date_col])
  df['year'] = df[date_col].dt.year
  df['month'] = df[date_col].dt.month
  df['day'] = df[date_col].dt.day
  df['weekday'] = df[date_col].dt.weekday  # Monday=0, Sunday=6
  df=df.drop(columns=date_col)
  return df

def train_model(train_df, model, model_name, target_col, param_grid=None):
    """
    Train a specified machine learning model.
    Hyperparameter tuning can be performed if a param_grid is provided.

    Args:
        train_df (pd.DataFrame): Input DataFrame containing training data.
        model: A machine learning model to be trained (e.g., Logistic Regression, Xboost,Gradient Boosting).
        model_name (str): The name of the model (used for saving the model,ohe,scaler).
        target_col (str): The name of the target column in the dataset.
        param_grid (dict): Hyperparameter grid for tuning using RandomizedSearchCV.

    Returns:
        model: Trained machine learning model (after tuning if param_grid is provided).
        ohe: One Hot Encoded Model.
        scaler: Robust Scaler
    """
    # Separate features and target
    x = train_df.drop(target_col, axis=1)
    y = train_df[target_col]
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)
    print("Splitting into training and validation done")
    
    # Apply one-hot encoding to categorical columns
    x_train, x_val, ohe = ohe_encoding(x_train, x_val, ["depart_id", "state"])
    print("One Hot encoding for training and validation done")

    # Encode dates
    x_train = encode_dates(x_train, "date")
    x_val = encode_dates(x_val, "date")
    print("Encoding Dates for training and validation done")
    
    # Scale features
    scaler = RobustScaler()
    scaler.fit(x_train)
    x_train_scaled = scaler.transform(x_train)
    x_val_scaled = scaler.transform(x_val)
    print("Robust Scaling for training and validation done")

    # Save the OneHotEncoder
    file_ohe = f'ohe_{model_name}.pkl'
    with open(file_ohe, 'wb') as f:
        pickle.dump(ohe, f)
    print("Pickle File for OHE done")
    # Save the Scaler
    file_scaler = f'scaler.pkl'
    with open(file_scaler, 'wb') as f:
        pickle.dump(scaler, f)
    print("Pickle File for Scaler done")

    # If param_grid is provided, perform hyperparameter tuning
    if param_grid is None:
        model.fit(x_train_scaled, y_train)
    else:
        reg = RandomizedSearchCV(
            estimator=model,
            param_distributions=param_grid,
            n_iter=10,
            scoring='neg_mean_squared_error',
            cv=3,
            verbose=1,
            random_state=42,
            n_jobs=-1
        )
        reg.fit(x_train_scaled, y_train)
        model = reg  # Use the best model found
    print("Model Training Stage done")

    # Predictions
    y_pred_train = model.predict(x_train_scaled)
    y_pred_val = model.predict(x_val_scaled)
    print("\nPrediction Stage done")

    # Performance metrics: Training Set
    mse_train = mean_squared_error(y_train, y_pred_train)
    rmse_train = np.sqrt(mse_train)
    r2_train = r2_score(y_train, y_pred_train)

    # Performance metrics: Validation Set
    mse_val = mean_squared_error(y_val, y_pred_val)
    rmse_val = np.sqrt(mse_val)
    r2_val = r2_score(y_val, y_pred_val)

    # Print the metrics
    print("Training Performance:")
    print(f"RMSE: {rmse_train:.4f}")
    print(f"R-squared: {r2_train:.4f}")

    print("\nValidation Performance:")
    print(f"RMSE: {rmse_val:.4f}")
    print(f"R-squared: {r2_val:.4f}")

    # Save the trained model
    model_filepath = f'{model_name}_model.pkl'
    with open(model_filepath, 'wb') as f:
        pickle.dump(model, f)

    # Return the model, OHE,scaler
    return model, ohe,scaler