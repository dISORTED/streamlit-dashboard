import pandas as pd
from io import StringIO

def test_csv_loads_correctly():
    data = "col1,col2\n1,2\n3,4"
    df = pd.read_csv(StringIO(data))
    assert list(df.columns) == ["col1", "col2"]
    assert df.shape == (2, 2)