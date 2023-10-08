from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class AddTargets(BaseEstimator, TransformerMixin):
    """
    The class adds targets to the DataFrame.

    Attributes:
        targets (Dict[str, Tuple[str, int]]): The dictionary with the targets.

    """

    def __init__(self, targets: Dict[str, Tuple[str, int]]):
        self.targets = targets

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """
        Add targets to the DataFrame.

        Parameters:
            X (pd.DataFrame): The input DataFrame.
            y: The target values.
        """
        X_copy = X.copy()
        self._add_targets(X_copy, self.targets)
        return X_copy.dropna()

    def _add_targets(
        self, df: pd.DataFrame, targets: Dict[str, Tuple[str, int]]
    ) -> None:
        """
        This method is designed to add target variables (targets) to the source DataFrame (df).
        Each target variable is calculated by summing the values of the specified column (vag_com)
        in the window of the specified width (days), and this result is shifted back by days.

        Parameters:
            df (pd.DataFrame): The input DataFrame.
            targets (Dict[str, Tuple[str, int]]):
            The dictionary with the targets:
                agg_col (str): The name of the column to aggregate.
                days (int): The number of days to aggregate.

        Returns:
            None
        """
        for target_name, (agg_col, days) in targets.items():
            # Sum of sales for the next n-days and shift by n-days
            df[target_name] = (
                df.groupby("sku_id")[agg_col]
                .rolling(window=days)
                .sum()
                .reset_index(level=0, drop=True)
            ).shift(-days)

            columns_to_set = [
                col
                for col in df.columns
                if "next" in col and col.endswith("d") and not col[-2:].isdigit()
            ]
            max_date = df["day"].max()
            df.loc[df["day"] == max_date, columns_to_set] = np.nan
