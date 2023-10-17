import logging
import os
from time import time

import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from prometheus_data.app_metrics import (
    how_much_to_order_failed_requests,
    how_much_to_order_request_count,
    how_much_to_order_response_time,
    how_much_to_order_successful_requests,
)
from src_demand_forecast.entities.train_pipeline_params import read_training_pipeline_params
from src_demand_forecast.entities.validation_params import LowStockSKURequest, SKURequest

app = FastAPI()
Instrumentator().instrument(app).expose(app)
params = read_training_pipeline_params("configs/train_config.yaml")

PATH_TO_PREDICTIONS = params.output_predictions
logging.basicConfig(filename="./logs/app.log", level=logging.INFO)


# Load predictions
try:
    predictions = pd.read_csv(PATH_TO_PREDICTIONS)
    logging.info(f"Predictions are loaded from {PATH_TO_PREDICTIONS}")
    assert not predictions.empty, "Predictions are empty!"
except Exception as e:
    logging.error(f"Failed to load predictions from {PATH_TO_PREDICTIONS}. Error: {e}")
    raise RuntimeError(
        f"Failed to load predictions from {PATH_TO_PREDICTIONS}. Error: {e}"
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation error: {exc.errors()}")
    how_much_to_order_failed_requests.inc()
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.post("/api/how_much_to_order")
def how_much_to_order(request_data: SKURequest) -> dict:
    """Predict how much to order
    Calculates how many SKUs need to be purchased to ensure sales
    for the specified forecast horizon and confidence level.
    Recommendation, how many items need to be replenished,
    it is formed taking into account the current stock.

    Parameters
    ----------
    request_data : SKURequest
        Request data

    Returns
    -------
    dict
        Quantity to order
    """
    try:
        start_time = time()
        how_much_to_order_request_count.inc()
        sku_id = request_data.sku.sku_id
        current_stock = request_data.sku.stock
        horizon_days = request_data.horizon_days
        confidence_level = request_data.confidence_level

        assert predictions is not None, "Predictions are not loaded"

        sku_predictions = predictions[predictions["sku_id"] == sku_id]
        last_day = sku_predictions["day"].max()
        last_day_prediction = sku_predictions[sku_predictions["day"] == last_day].iloc[
            0
        ]

        # Choose the right column based on horizon_days and confidence_level
        col_name = f"pred_{horizon_days}d_q{int(confidence_level * 100)}"

        total_demand_forecast = last_day_prediction[col_name]
        recommended = max(int(np.ceil(total_demand_forecast)) - current_stock, 0)

        how_much_to_order_successful_requests.inc()
        logging.info(f"Request from how_much_to_order is successful")
        return {"quantity": recommended}
    except Exception as e:
        how_much_to_order_failed_requests.inc()
        logging(f"Failed request with error: {e}")
        raise HTTPException(status_code=420, detail=str(e))
    finally:
        how_much_to_order_response_time.observe(time() - start_time)


@app.post("/api/stock_level_forecast")
def stock_level_forecast(request_data: SKURequest) -> dict:
    """Predict stock level.
    Returns the predicted inventory level for the specified
     SKU for a given forecast horizon and confidence level.
     Calculates how many SKUs will remain in stock, taking into account
     the sales forecast. If the sales forecast is greater than the current one
     the remainder, should return 0.

    Parameters
    ----------
    request_data : SKURequest
        Request data

    Returns
    -------
    dict
        Stock forecast
    """
    try:
        sku_id = request_data.sku.sku_id
        current_stock = request_data.sku.stock
        horizon_days = request_data.horizon_days
        confidence_level = request_data.confidence_level

        assert predictions is not None, "Predictions are not loaded"

        sku_predictions = predictions[predictions["sku_id"] == sku_id]
        last_day = sku_predictions["day"].max()
        last_day_prediction = sku_predictions[sku_predictions["day"] == last_day].iloc[
            0
        ]

        # Choose the right column based on horizon_days and confidence_level
        col_name = f"pred_{horizon_days}d_q{int(confidence_level * 100)}"

        demand_forecast = last_day_prediction[col_name]
        stock_level = max(current_stock - round(demand_forecast), 0)
        logging.info(f"Request from stock_level_forecast is successful")
        return {"stock_forecast": stock_level}

    except Exception as e:
        logging.debug(f"Failed request with error: {e}")
        logging(f"Failed request with error: {e}")
        raise HTTPException(status_code=420, detail=str(e))


@app.post("/api/low_stock_sku_list")
def low_stock_sku_list(request_data: LowStockSKURequest) -> dict:
    """Return sku list with low stock level
        Returns a list of SKUs that are in the "danger zone"
        for a given forecast horizon and confidence level.
        The product is in a dangerous area if there is not enough stock left in the warehouse,
        to ensure the projected sales volume. For example, the rest of the product is 10 pcs.,
    the projected sales volume is 12 pcs. Such a product is in a dangerous zone.

    Parameters
    ----------
    request_data : LowStockSKURequest
        Request data

    Returns
    -------
    dict
        List of SKUs with low stock level

    """
    try:
        confidence_level = request_data.confidence_level
        horizon_days = request_data.horizon_days
        skus = request_data.sku_stock

        assert predictions is not None, "Predictions are not loaded"

        # Get predictions for all SKUs
        sku_predictions = predictions[
            predictions["sku_id"].isin([sku.sku_id for sku in skus])
        ]
        # Get last day
        last_day = sku_predictions["day"].max()
        # Get last day predictions
        last_day_prediction = sku_predictions[sku_predictions["day"] == last_day]

        # Choose the right column based on horizon_days and confidence_level
        col_name = f"pred_{horizon_days}d_q{int(confidence_level * 100)}"

        low_stock_list = []
        for sku in skus:
            # Get demand forecast for SKU
            demand_forecast = last_day_prediction[
                last_day_prediction["sku_id"] == sku.sku_id
            ][col_name].values[0]
            # Check if stock is less than demand forecast
            if sku.stock < demand_forecast:
                low_stock_list.append(sku.sku_id)
        logging.info(f"Request from low_stock_sku_list is successful")
        return {"sku_list": low_stock_list}

    except Exception as e:
        logging(f"Failed request with error: {e}")
        raise HTTPException(status_code=420, detail=str(e))


# uvicorn app:app --host localhost --port 8000
# http://localhost:8000/docs
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=os.getenv("PORT", 8000))
