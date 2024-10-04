import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error, r2_score
from .training_model import encode_dates
import numpy as np
from make_dataset_model import  split_item_id,split_store_id,find_outliers
def load_models(model_filepath, ohe_filepath,scaler_filepath):
    """
    Load the trained model and OneHotEncoder from disk.

    Args:
        model_filepath (str): Path to the saved model file.
        ohe_filepath (str): Path to the saved OneHotEncoder file.
        scaler_filepath (str): Path to the saved OneHotEncoder file.

    Returns:
        model: Loaded model.
        ohe: Loaded OneHotEncoder.
        scaler: Loaded Robust Scaler
    """
    with open(model_filepath, 'rb') as f:
        model = pickle.load(f)
    with open(ohe_filepath, 'rb') as f:
        ohe = pickle.load(f)
    with open(scaler_filepath, 'rb') as f:
        scaler = pickle.load(f)
    return model, ohe, scaler

def predict(test_df, model, ohe,scaler):
    """
    Make predictions using the trained model and preprocessed test data.

    Args:
        test_df (DataFrame): DataFrame containing the test data.
        model: Trained model for prediction.
        ohe: Fitted OneHotEncoder instance.

    Returns:
        None
    """
    test_df=find_outliers(test_df)
    test_df=split_store_id(test_df)
    test_df=split_item_id(test_df)
    x_test = test_df.drop(columns=['revenue'])  # All columns except 'revenue'
    y_test = test_df['revenue']  # Specify 'revenue' as the target variable

    # Apply one-hot encoding to categorical columns
    x_test = ohe.transform(x_test[["depart_id", "state"]])
    x_test = pd.DataFrame(x_test, columns=ohe.get_feature_names_out(), index=test_df.index)
    x_test = pd.concat([test_df.drop(columns=["depart_id", "state", "revenue"]), x_test], axis=1)

    # Encode dates
    x_test = encode_dates(x_test, "date")

    # Scale features using the loaded scaler
    x_test_scaled = scaler.transform(x_test)

    # Calculate performance metrics for test set
    y_pred_test = model.predict(x_test_scaled)
    mse_test = mean_squared_error(y_test, y_pred_test)
    rmse_test = np.sqrt(mse_test)
    r2_test = r2_score(y_test, y_pred_test)

    # Print the metrics
    print("\nTesting Performance:")
    print(f"MSE: {mse_test:.4f}")
    print(f"RMSE: {rmse_test:.4f}")
    print(f"R-squared: {r2_test:.4f}")
