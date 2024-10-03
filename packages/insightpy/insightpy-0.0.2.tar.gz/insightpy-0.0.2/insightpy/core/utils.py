from pandas import DataFrame


def is_numeric(df:DataFrame,column:str) -> bool:
    return df[column].dtype in ['int64', 'float64','bool']