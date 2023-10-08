import logging
import sys

import pandas as pd

from src.features.build_sku_by_day import sku_demand_by_day
from src.features.build_transformer import (features_and_targets_transformer,
                                            save_transformed_data)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# Test sales.csv
def test_equals_sku_demand_by_day(
    test_df_demand_orders: pd.DataFrame,
    test_df_demand_orders_status: pd.DataFrame,
    test_df_expected_df_sku_demand_by_day: pd.DataFrame,
) -> None:
    """
    Test sku_demand_by_day function. This function
    checks the correctness of the sku_demand_by_day.

    Parameters
    ----------
    test_df_demand_orders : pd.DataFrame
        Test demand orders
    test_df_demand_orders_status : pd.DataFrame
        Test demand orders status
    test_df_expected_df_sku_demand_by_day : pd.DataFrame
        Test expected sku demand by day

    Returns
    -------
    None
    """
    # Call the function to test sku_demand_by_day
    actual_df = sku_demand_by_day(test_df_demand_orders, test_df_demand_orders_status)
    assert actual_df.equals(
        test_df_expected_df_sku_demand_by_day
    ), f"Expected {test_df_expected_df_sku_demand_by_day}, but got {actual_df}"


def test_features_and_targets_transformer(
    test_inpot_df_expected_df_features_and_targets: pd.DataFrame,
    test_df_output_expected_df_features_and_targets: pd.DataFrame,
) -> None:
    """
    Test features_and_targets_transformer function. This function
    checks the correctness of the transformer.

    Parameters
    ----------
    test_inpot_df_expected_df_features_and_targets : pd.DataFrame
        Test input data
    test_df_output_expected_df_features_and_targets : pd.DataFrame
        Test expected output data

    Returns
    -------
    None
    """
    # Call the function to test features_and_targets_transformer
    transformer = features_and_targets_transformer()
    actual_df = transformer.fit_transform(
        test_inpot_df_expected_df_features_and_targets
    )
    actual_df["day"] = pd.to_datetime(actual_df["day"])
    assert actual_df.equals(
        test_df_output_expected_df_features_and_targets
    ), f"Expected {test_df_output_expected_df_features_and_targets}, but got {actual_df}"
