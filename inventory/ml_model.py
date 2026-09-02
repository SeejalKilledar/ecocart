"""
EcoCart Inventory Demand Forecasting
Uses Random Forest Regressor on synthetic historical sales data.
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

PRODUCTS = ['Laptop', 'Headphones', 'Phone Case', 'Charger', 'Keyboard']


# Seasonal multipliers per week (52 weeks)
def _seasonal(week):
    return 1.0 + 0.3 * np.sin(2 * np.pi * week / 52)


def generate_sales_data(product_index=0, weeks=52):
    """Generate synthetic weekly sales data with trend + seasonality + noise."""
    rng = np.random.default_rng(seed=42 + product_index)
    weeks_arr = np.arange(1, weeks + 1)
    trend = 100 + product_index * 15 + weeks_arr * 1.2
    seasonal = _seasonal(weeks_arr)
    noise = rng.normal(0, 10, weeks)
    sales = trend * seasonal + noise
    sales = np.clip(sales, 0, None).astype(int)
    return weeks_arr.tolist(), sales.tolist()


def _build_features(weeks_arr):
    """Build rich feature set: week, trend, and Fourier seasonality features."""
    X = np.array(weeks_arr).reshape(-1, 1)
    X_sq = X ** 2
    X_sin = np.sin(2 * np.pi * X / 52)
    X_cos = np.cos(2 * np.pi * X / 52)
    X_sin2 = np.sin(4 * np.pi * X / 52)
    X_cos2 = np.cos(4 * np.pi * X / 52)
    return np.hstack([X, X_sq, X_sin, X_cos, X_sin2, X_cos2])


def forecast(product_index=0, history_weeks=52, forecast_weeks=8):
    """
    Train a Random Forest model with trend + Fourier features and forecast future demand.

    Random Forest builds multiple decision trees on random subsets of the data
    and features, then averages their predictions to reduce overfitting and
    improve generalisation — more robust than a single regression line.

    Returns:
        historical weeks/sales, predicted weeks/sales, metrics, feature importances.
    """
    weeks, sales = generate_sales_data(product_index, history_weeks)
    y = np.array(sales)

    X_train = _build_features(weeks)

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y)

    y_pred_train = np.clip(model.predict(X_train), 0, None).astype(int).tolist()

    future_weeks = list(range(history_weeks + 1, history_weeks + forecast_weeks + 1))
    X_future = _build_features(future_weeks)
    y_future = np.clip(model.predict(X_future), 0, None).astype(int).tolist()

    mae = round(mean_absolute_error(y, y_pred_train), 2)
    r2 = round(r2_score(y, y_pred_train), 4)

    feature_names = ['Week', 'Week²', 'Sin(annual)', 'Cos(annual)', 'Sin(half-yr)', 'Cos(half-yr)']
    importances = [
        {'feature': name, 'importance': round(float(imp), 4)}
        for name, imp in zip(feature_names, model.feature_importances_)
    ]
    importances.sort(key=lambda x: x['importance'], reverse=True)

    return {
        'product': PRODUCTS[product_index],
        'history': {'weeks': weeks, 'sales': sales, 'predicted': y_pred_train},
        'forecast': {'weeks': future_weeks, 'sales': y_future},
        'metrics': {'mae': mae, 'r2': r2},
        'feature': 'Week number + seasonality features',
        'target': 'Units sold',
        'model_info': {
            'algorithm': 'Random Forest Regressor',
            'n_estimators': 200,
            'max_depth': 8,
        },
        'feature_importances': importances,
    }
