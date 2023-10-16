import logging
import sys
from typing import List

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import QuantileRegressor
from tqdm import tqdm

from src_demand_forecast.data.split_dataset import split_train_test
from src_demand_forecast.entities.train_pipeline_params import read_training_pipeline_params

PATH = "configs/train_config.yaml"
params = read_training_pipeline_params(PATH)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class MultiTargetModel:
    def __init__(
        self,
        features: List[str],
        horizons: List[int] = [7, 14, 21],
        quantiles: List[float] = [0.1, 0.5, 0.9],
    ) -> None:
        """
        Parameters
        ----------
        features : List[str]
            List of features columns.
        horizons : List[int]
            List of horizons.
        quantiles : List[float]
            List of quantiles.

        Attributes
        ----------
        fitted_models_ : dict
            Dictionary with fitted models for each sku_id.
            Example:
            {
                sku_id_1: {
                    (quantile_1, horizon_1): model_1,
                    (quantile_1, horizon_2): model_2,
                    ...
                },
                sku_id_2: {
                    (quantile_1, horizon_1): model_3,
                    (quantile_1, horizon_2): model_4,
                    ...
                },
                ...
            }

        """
        self.quantiles = quantiles
        self.horizons = horizons
        self.sku_col = "sku_id"
        self.date_col = "day"
        self.features = features
        self.targets = [f"next_{horizon}d" for horizon in self.horizons]

        self.fitted_models_ = {}

    def fit(self, data: pd.DataFrame, verbose: bool = False) -> None:
        """Fit model on data.

        Parameters
        ----------
        data : pd.DataFrame
            Data to fit on.
        verbose : bool, optional
            Whether to show progress bar, by default False
            Optional to implement, not used in grading.
        """

        # For each sku_id
        for sku_id in tqdm(data[self.sku_col].unique()):
            # Make a dictionary for this sku_id
            self.fitted_models_[sku_id] = {}
            # For each horizon (7, 14, 21 days):
            for horizon in self.horizons:
                # For each quantile (0.1, 0.5, 0.9):
                for quantile in self.quantiles:
                    # Fit a model for this sku_id, horizon and quantile
                    model = QuantileRegressor(quantile=quantile, solver="highs")
                    model.fit(
                        data[data[self.sku_col] == sku_id][self.features],
                        data[data[self.sku_col] == sku_id][f"next_{horizon}d"],
                    )
                    # Save the model to the dictionary
                    self.fitted_models_[sku_id][(quantile, horizon)] = model

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """Predict on data.
        Predict 0 values for a new sku_id.
        Parameters
        ----------
        data : pd.DataFrame
            Data to predict on.
        Returns
        -------
        pd.DataFrame
            Predictions.
        """

        predictions_list = []

        # Each sku_id
        for sku_id in tqdm(data[self.sku_col].unique()):
            sku_predictions = pd.DataFrame()
            sku_predictions["sku_id"] = [sku_id] * len(
                data[data[self.sku_col] == sku_id]
            )
            sku_predictions["day"] = data[data[self.sku_col] == sku_id][
                self.date_col
            ].values

            # For each horizon (7, 14, 21 days):
            if sku_id not in self.fitted_models_:
                # If there is no model for this sku_id, predict 0
                for horizon in self.horizons:
                    for quantile in self.quantiles:
                        sku_predictions[f"pred_{horizon}d_q{int(quantile * 100)}"] = 0
            else:
                # If there is a model for this sku_id, predict
                for horizon in self.horizons:
                    for quantile in self.quantiles:
                        # Get model from dictionary
                        model = self.fitted_models_[sku_id][(quantile, horizon)]
                        # Get predictions
                        pred_values = model.predict(
                            data[data[self.sku_col] == sku_id][self.features]
                        )
                        sku_predictions[
                            f"pred_{horizon}d_q{int(quantile * 100)}"
                        ] = pred_values

            # Append predictions for this sku_id to the list
            sku_predictions.reset_index(drop=True, inplace=True)
            predictions_list.append(sku_predictions)

        predictions_df = pd.concat(predictions_list, ignore_index=True)
        # Sort by sku_id and day
        predictions_df = predictions_df.sort_values(by="day", ascending=False)
        return predictions_df


def quantile_loss(y_true: np.ndarray, y_pred: np.ndarray, quantile: float) -> float:
    """
    Calculate the quantile loss between the true and predicted values.

    The quantile loss measures the deviation between the true
        and predicted values at a specific quantile.

    Parameters
    ----------
    y_true : np.ndarray
        The true values.
    y_pred : np.ndarray
        The predicted values.
    quantile : float
        The quantile to calculate the loss for.

    Returns
    -------
    float
        The quantile loss.
    """
    errors = y_true - y_pred
    loss = np.mean(
        quantile * np.maximum(errors, 0) + (1 - quantile) * np.maximum(-errors, 0)
    )
    return loss


def evaluate_model(
    df_true: pd.DataFrame,
    df_pred: pd.DataFrame,
    quantiles: List[float] = [0.1, 0.5, 0.9],
    horizons: List[int] = [7, 14, 21],
) -> pd.DataFrame:
    """Evaluate model on data.

    Parameters
    ----------
    df_true : pd.DataFrame
        True values.
    df_pred : pd.DataFrame
        Predicted values.
    quantiles : List[float], optional
        Quantiles to evaluate on, by default [0.1, 0.5, 0.9].
    horizons : List[int], optional
        Horizons to evaluate on, by default [7, 14, 21].

    Returns
    -------
    pd.DataFrame
        Evaluation results.
    """
    losses = {}

    for quantile in quantiles:
        for horizon in horizons:
            true = df_true[f"next_{horizon}d"].values
            pred = df_pred[f"pred_{horizon}d_q{int(quantile*100)}"].values
            loss = quantile_loss(true, pred, quantile)

            losses[(quantile, horizon)] = loss

    # Make dictionary with losses
    losses = {
        "quantile": [item[0] for item in losses.keys()],
        "horizon": [item[1] for item in losses.keys()],
        "avg_quantile_loss": [item for item in losses.values()],
    }

    return losses


def serialize_model(model, output: str) -> None:
    """Serialize model to pickle file.

    Parameters
    ----------
    model : object
        Model to serialize.
    output : str
        Path to output file.
    """
    with open(output, "wb") as file:
        joblib.dump(model, file)
    return output


if __name__ == "__main__":
    logger.info("Start training model")
    # Read data
    logger.info("Read data")
    data = pd.read_csv(params.output_features_and_targets)
    # Split data
    logger.info("Split data")
    train_data, test_data = split_train_test(data)
    # Make model
    logger.info("Make model")
    model = MultiTargetModel(features=params.model_params.features)
    # Fit model
    logger.info("Fit model")
    model.fit(train_data)
    # Predict
    logger.info("Predict")
    predictions = model.predict(test_data)
    # Calculate loss
    logger.info("Calculate loss")
    losses = evaluate_model(test_data, predictions)
    print(losses)
    logger.info("Finish training model")
