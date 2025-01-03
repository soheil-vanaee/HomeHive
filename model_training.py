import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib

data = pd.read_csv('housing_dataset.csv')
X = data[['house_meter', 'rooms', 'latitude', 'longitude', 'floor']]
y = data['price']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(random_state=42, n_estimators=200, max_depth=10)
xgb_model = XGBRegressor(random_state=42, n_estimators=100, learning_rate=0.1, max_depth=5)

ensemble_model = VotingRegressor(estimators=[
    ('random_forest', rf_model),
    ('xgboost', xgb_model)
])

ensemble_model.fit(X_train, y_train)

y_pred = ensemble_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae}")
print(f"RMSE: {rmse}")
print(f"R²: {r2}")

joblib.dump(ensemble_model, 'house_price_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
