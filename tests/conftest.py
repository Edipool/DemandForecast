import logging
import sys

import pandas as pd
import pytest

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# Make test data demand orders
@pytest.fixture()
def test_df_demand_orders():
    data = {
        "order_id": ["07f5c674", "de500260", "548d1408", "e924bc98", "abf0324c"],
        "timestamp": [
            "2018-07-01 03:40:50",
            "2018-07-01 17:48:35",
            "2018-07-01 23:45:30",
            "2018-07-02 18:39:46",
            "2018-07-03 01:04:02",
        ],
        "sku_id": ["Router", "Router", "Router", "Router", "Router"],
        "sku": [64, 64, 64, 64, 64],
        "price": [1460, 1460, 1460, 1460, 1460],
        "qty": [3, 5, 4, 4, 6],
    }
    demand_orders = pd.DataFrame(data)
    return demand_orders


# Make test data demand orders status
@pytest.fixture()
def test_df_demand_orders_status():
    data = {
        "order_id": ["e7a5493f", "d6e34aff", "27271224", "e8912be6", "a00b95ff"],
        "status_id": ["1", "1", "1", "1", "1"],
        "status": ["Accepted", "Accepted", "Accepted", "Accepted", "Accepted"],
    }
    demand_orders_status = pd.DataFrame(data)
    return demand_orders_status


# Make test data sales
@pytest.fixture()
def test_df_sales():
    data = {
        "day": ["2018-07-01", "2018-07-02", "2018-07-03", "2018-07-04", "2018-07-05"],
        "sku_id": [
            0,
        ]
        * 5,
        "sku": ["Router 64"] * 5,
        "price": [1460] * 5,
        "qty": [7, 4, 0, 5, 6],
    }
    sales_df = pd.DataFrame(data)
    return sales_df


# Expected data for def sku_demand_by_day
@pytest.fixture()
def test_df_expected_df_sku_demand_by_day():
    data = {
        "day": [
            "2018-07-01",
            "2018-07-02",
            "2018-07-03",
        ],
        "sku_id": ["Router", "Router", "Router"],
        "sku": [64, 64, 64],
        "price": [1460, 1460, 1460],
        "qty": [0, 0, 0],
    }
    expected_df = pd.DataFrame(data)
    return expected_df


# Expected data for def transformed_data (after transform)
@pytest.fixture()
def test_df_output_expected_df_features_and_targets():
    index = list(range(20, 41))
    data = {
        "day": pd.date_range(start="2018-07-21", periods=21, freq="D"),
        "sku_id": ["Router"] * 21,
        "sku": [64] * 21,
        "price": [1460] * 21,
        "qty": [0] * 21,
        "qty_7d_avg": [0.0] * 21,
        "qty_7d_q10": [0.0] * 21,
        "qty_7d_q50": [0.0] * 21,
        "qty_7d_q90": [0.0] * 21,
        "qty_14d_avg": [0.0] * 21,
        "qty_14d_q10": [0.0] * 21,
        "qty_14d_q50": [0.0] * 21,
        "qty_14d_q90": [0.0] * 21,
        "qty_21d_avg": [0.0] * 21,
        "qty_21d_q10": [0.0] * 21,
        "qty_21d_q50": [0.0] * 21,
        "qty_21d_q90": [0.0] * 21,
        "next_7d": [0.0] * 21,
        "next_14d": [0.0] * 21,
        "next_21d": [0.0] * 21,
    }
    targets_df = pd.DataFrame(data, index=index)
    return targets_df


# Expected data for def transformed_data (before transform)
@pytest.fixture()
def test_inpot_df_expected_df_features_and_targets():
    data = {
        "day": [f"2018-07-{str(i).zfill(2)}" for i in range(1, 32)]
        + [f"2018-08-{str(i).zfill(2)}" for i in range(1, 32)],
        "sku_id": ["Router"] * 62,
        "sku": [64] * 62,
        "price": [1460] * 62,
        "qty": [0] * 62,
    }

    expected_df = pd.DataFrame(data)
    return expected_df
