"""
This module contains functions for making requests to the FastAPI server.
"""
import logging
import os
from time import sleep
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"  # url for local testing
# BASE_URL = os.getenv("REMOTE_URL")  # url for docker testing


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def check_response(response) -> None:
    """
    Check the response from the FastAPI server.

    Parameters
    ----------
    response : requests.models.Response
        The response from the FastAPI server.

    Returns
    -------
    None
    """
    if response.status_code == 200:
        logger.info(f"Success (Code 200): {response.json()}")
    else:
        logger.error(f"Error (Code {response.status_code}): {response.text}")


def how_much_to_order(
    sku_id: int, stock: int, horizon_days: int, confidence_level: float
) -> None:
    """
    Make a request to the FastAPI server to get the order quantity.

    Parameters
    ----------
    sku_id : int
        The SKU id.
    stock : int
        The current stock level.
    horizon_days : int
        The number of days in the horizon.
    confidence_level : float
        The confidence level.

    Returns
    -------
    None
    """
    url = f"{BASE_URL}/api/how_much_to_order"
    payload = {
        "sku": {"sku_id": sku_id, "stock": stock},
        "horizon_days": horizon_days,
        "confidence_level": confidence_level,
    }
    response = requests.post(url, json=payload)
    check_response(response)


def stock_level_forecast(
    sku_id: int, stock: int, horizon_days: int, confidence_level: float
) -> None:
    """
    Get the stock level forecast.

    Parameters
    ----------
    sku_id : int
        The SKU id.
    stock : int
        The current stock level.
    horizon_days : int
        The number of days in the horizon.
    confidence_level : float
        The confidence level.

    Returns
    -------
    None
    """
    url = f"{BASE_URL}/api/stock_level_forecast"
    payload = {
        "sku": {"sku_id": sku_id, "stock": stock},
        "horizon_days": horizon_days,
        "confidence_level": confidence_level,
    }
    response = requests.post(url, json=payload)
    check_response(response)


def low_stock_sku_list(
    confidence_level: float, horizon_days: int, sku_stock: List[dict]
) -> None:
    """
    Get the list of low stock SKUs.

    Parameters
    ----------
    confidence_level : float
        The confidence level.
    horizon_days : int
        The number of days in the horizon.
    sku_stock : List[dict]
        The list of dictionaries with the SKU id and stock level.

    Returns
    -------
    None
    """
    url = f"{BASE_URL}/api/low_stock_sku_list"
    payload = {
        "confidence_level": confidence_level,
        "horizon_days": horizon_days,
        "sku_stock": sku_stock,
    }
    response = requests.post(url, json=payload)
    check_response(response)


# Make test data
test_data_list = [
    {"sku": {"sku_id": 78, "stock": 10}, "horizon_days": 7, "confidence_level": 0.1},
    {
        "sku": {"sku_id": "fgfg", "stock": 5},
        "horizon_days": 14,
        "confidence_level": 0.9,
    },
    {"sku": {"sku_id": 18, "stock": 15}, "horizon_days": 7, "confidence_level": 0.1},
    {"sku": {"sku_id": 78, "stock": 10}, "horizon_days": 7, "confidence_level": 0.5},
    {
        "sku": {"sku_id": "fgfg", "stock": 5},
        "horizon_days": 14,
        "confidence_level": 0.9,
    },
    {"sku": {"sku_id": 18, "stock": 15}, "horizon_days": 7, "confidence_level": 0.5},
    {"sku": {"sku_id": 78, "stock": 10}, "horizon_days": 7, "confidence_level": 0.9},
    {"sku": {"sku_id": 18, "stock": 15}, "horizon_days": 7, "confidence_level": 0.9},
    {"sku": {"sku_id": 22, "stock": 5}, "horizon_days": 14, "confidence_level": 0.1},
    {"sku": {"sku_id": 54, "stock": 5}, "horizon_days": 14, "confidence_level": 0.5},
    {"sku": {"sku_id": 22, "stock": 5}, "horizon_days": 14, "confidence_level": 0.9},
    {"sku": {"sku_id": 54, "stock": 5}, "horizon_days": 14, "confidence_level": 0.9},
]

if __name__ == "__main__":
    # Run tests
    for test_data in test_data_list:
        how_much_to_order(
            test_data["sku"]["sku_id"],
            test_data["sku"]["stock"],
            test_data["horizon_days"],
            test_data["confidence_level"],
        )
        stock_level_forecast(
            test_data["sku"]["sku_id"],
            test_data["sku"]["stock"],
            test_data["horizon_days"],
            test_data["confidence_level"],
        )
        low_stock_sku_list(
            test_data["confidence_level"],
            test_data["horizon_days"],
            [
                {
                    "sku_id": test_data["sku"]["sku_id"],
                    "stock": test_data["sku"]["stock"],
                }
            ],
        )
        sleep(1)
