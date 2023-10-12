import logging
import sys
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class AddFeatures(BaseEstimator, TransformerMixin):
    """
    The class adds features to the DataFrame.

    Attributes:
        features (Dict[str, Tuple[str, int, str, Optional[int]]]): The dictionary with the features.

    """

    def __init__(self, features: Dict[str, Tuple[str, int, str, Optional[int]]]):
        self.features = features

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """
        Add features to the DataFrame.

        Parameters:
            X (pd.DataFrame): The input DataFrame.
            y: The target values.

        Returns:
            pd.DataFrame: The DataFrame with the added features.
        """
        X_copy = X.copy()
        self._add_features(X_copy, self.features)
        return X_copy.dropna()

    def _add_features(
        self, df: pd.DataFrame, features: Dict[str, Tuple[str, int, str, Optional[int]]]
    ) -> None:
        """
        This method adds attributes to the DataFrame by applying the specified aggregation functions to the windows defined
        by the 'days' parameters. First, the DataFrame is grouped by 'sku_id', after which aggregation is applied
        to the specified 'aeg_col' column within each group.

        Parameters:
            df (pd.DataFrame): The input DataFrame.
            features (Dict[str, Tuple[str, int, str, Optional[int]]]):
            The dictionary with the features:
                agg_col (str): The name of the column to aggregate.
                days (int): The number of days to aggregate.
                agg_func (str): The name of the aggregation function.
                quantile (Optional[int]): The quantile to compute (default: None).

        Returns:
            None
        """
        for feature_name, (agg_col, days, agg_func, quantile) in features.items():
            if agg_func == "quantile":
                df[feature_name] = (
                    df.groupby("sku_id")[agg_col]
                    .rolling(window=days)
                    .quantile(quantile / 100)
                    .reset_index(level=0, drop=True)
                )

            elif agg_func == "avg":
                df[feature_name] = (
                    df.groupby("sku_id")[agg_col]
                    .rolling(window=days)
                    .mean()
                    .reset_index(level=0, drop=True)
                )

            else:
                raise ValueError(f"Unknown aggregation function: {agg_func}")

            columns_to_set = [
                col
                for col in df.columns
                if "next" in col and col.endswith("d") and not col[-2:].isdigit()
            ]
            max_date = df["day"].max()
            df.loc[df["day"] == max_date, columns_to_set] = np.nan
