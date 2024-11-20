import pandas as pd
import feast
from joblib import load
import config


class DriverRankingModel:
    def __init__(self):
        # Load model
        self.model = load("model/driver_model.bin")

        # Set up feature store
        self.fs = feast.FeatureStore(repo_path=config.FEATURE_REPO_PATH)

    def predict(self, driver_ids):
        # Read features from Feast
        driver_features = self.fs.get_online_features(
            entity_rows=[{"driver_id": driver_id} for driver_id in driver_ids],
            features=[
                "driver_hourly_stats:conv_rate",
                "driver_hourly_stats:acc_rate",
                "driver_hourly_stats:avg_daily_trips",
            ],
        )
        
        df = pd.DataFrame.from_dict(driver_features.to_dict())

        # Make prediction
        df["prediction"] = self.model.predict(df[sorted(df)])

        # Choose best driver
        best_driver_id = df["driver_id"].iloc[df["prediction"].argmax()]

        # return best driver
        return best_driver_id


if __name__ == "__main__":
    drivers = [1001, 1002, 1003, 1004]
    model = DriverRankingModel()
    best_driver = model.predict(drivers)
    print("Best Driver: ", best_driver)
