import pandas as pd

def save_to_csv(df, file_path):
    df.to_csv(file_path, index=False)

def load_from_csv(file_path):
    return pd.read_csv(file_path)