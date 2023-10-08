from typing import Tuple

import pandas as pd


def split_train_test(
    df: pd.DataFrame,
    test_days: int = 30,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split the data into train and test sets.
    The last `test_days` days are held out for testing.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the data.
        test_days (int): The number of days to include in the test set (default: 30).
            use ">=" sign for df_test

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
        A tuple containing the train and test DataFrames.
    """
    # Drop rows with NaN values
    df = df.dropna()
    # Convert day column to datetime
    df["day"] = pd.to_datetime(df["day"], dayfirst=True)
    # Get the maximum date in the day column and subtract the number of days in the test set.
    threshold_date = df["day"].max() - pd.Timedelta(days=test_days)
    # For df_train you take all the rows where the date is less than this threshold date.
    # Take all dates that are less than threshold_date
    df_train = df[df["day"] < threshold_date]
    # For df_test you take all the rows where the date is greater than or equal to this threshold date.
    # Take all dates that are greater than or equal to threshold_date
    df_test = df[df["day"] >= threshold_date]
    return df_train, df_test
