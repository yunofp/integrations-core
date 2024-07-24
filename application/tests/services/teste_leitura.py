import pytest
from unittest.mock import MagicMock
import pandas as pd
import os

def sample_df():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'file.csv')
    df = pd.read_csv(csv_path)
    print(df.iloc[11:13])

sample_df()