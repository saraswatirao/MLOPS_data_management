import pandas as pd
import config

df = pd.read_csv(config.CSV_FILE_PATH)

df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
df["created"] = pd.to_datetime(df["created"])

df.to_parquet(config.PARQUET_FILE_PATH)