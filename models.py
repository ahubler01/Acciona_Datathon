import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from mlxtend.regressor import StackingCVRegressor

# Assuming you have 'merged_df' DataFrame

target_variable = 'INF_Value'

# Define features and target
features = merged_df.drop(target_variable, axis=1)
target = merged_df[target_variable]

# Split the data into training and testing sets
tscv = TimeSeriesSplit(n_splits=5)
for train_index, val_index in tscv.split(features):
    X_train, X_val = features.iloc[train_index], features.iloc[val_index]
    y_train, y_val = target.iloc[train_index], target.iloc[val_index]

    # Models
    rf_model = RandomForestRegressor(random_state=42)
    xgb_model = XGBRegressor(random_state=42)
    catboost_model = CatBoostRegressor(random_state=42, silent=True)

    # Train the models
    rf_model.fit(X_train, y_train)
    xgb_model.fit(X_train, y_train)
    catboost_model.fit(X_train, y_train)

    # Make predictions on the validation set
    rf_val_preds = rf_model.predict(X_val)
    xgb_val_preds = xgb_model.predict(X_val)
    catboost_val_preds = catboost_model.predict(X_val)

    # Create a DataFrame with validation set predictions as features
    meta_features_val = pd.DataFrame({'RF': rf_val_preds, 'XGB': xgb_val_preds, 'CatBoost': catboost_val_preds})

    # Initialize meta-regressor (you may choose a different meta-regressor)
    meta_regressor = CatBoostRegressor(random_state=42, silent=True)

    # Fit the meta-regressor with the predictions
    meta_regressor.fit(meta_features_val, y_val)

# Make predictions on the test set
rf_test_preds = rf_model.predict(X_val)
xgb_test_preds = xgb_model.predict(X_val)
catboost_test_preds = catboost_model.predict(X_val)

# Create a DataFrame with test set predictions as features
meta_features_test = pd.DataFrame({'RF': rf_test_preds, 'XGB': xgb_test_preds, 'CatBoost': catboost_test_preds})

# Make final predictions using the meta-regressor
stacking_preds = meta_regressor.predict(meta_features_test)

# Evaluate the individual models
rf_mae = mean_absolute_error(y_val, rf_test_preds)
rf_rmse = mean_squared_error(y_val, rf_test_preds, squared=False)
rf_mape = mean_absolute_percentage_error(y_val, rf_test_preds)

xgb_mae = mean_absolute_error(y_val, xgb_test_preds)
xgb_rmse = mean_squared_error(y_val, xgb_test_preds, squared=False)
xgb_mape = mean_absolute_percentage_error(y_val, xgb_test_preds)

catboost_mae = mean_absolute_error(y_val, catboost_test_preds)
catboost_rmse = mean_squared_error(y_val, catboost_test_preds, squared=False)
catboost_mape = mean_absolute_percentage_error(y_val, catboost_test_preds)

stacking_mae = mean_absolute_error(y_val, stacking_preds)
stacking_rmse = mean_squared_error(y_val, stacking_preds, squared=False)
stacking_mape = mean_absolute_percentage_error(y_val, stacking_preds)

# Print metrics for individual models
print("Random Forest Test Set MAE:", rf_mae)
print("Random Forest Test Set RMSE:", rf_rmse)
print("Random Forest Test Set MAPE:", rf_mape * 100)

print("XGBoost Test Set MAE:", xgb_mae)
print("XGBoost Test Set RMSE:", xgb_rmse)
print("XGBoost Test Set MAPE:", xgb_mape * 100)

print("CatBoost Test Set MAE:", catboost_mae)
print("CatBoost Test Set RMSE:", catboost_rmse)
print("CatBoost Test Set MAPE:", catboost_mape * 100)

# Print metrics for stacking model
print("Stacking Test Set MAE:", stacking_mae)
print("Stacking Test Set RMSE:", stacking_rmse)
print("Stacking Test Set MAPE:", stacking_mape * 100)
