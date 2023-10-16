import argparse
import json
import logging
import sys

import pandas as pd

from src_demand_forecast.data.split_dataset import split_train_test
from src_demand_forecast.entities.train_pipeline_params import read_training_pipeline_params
from src_demand_forecast.features.build_sku_by_day import save_sku_demand_by_day, sku_demand_by_day
from src_demand_forecast.features.build_transformer import (
    features_and_targets_transformer,
    save_transformed_data,
)
from src_demand_forecast.models.train_model import MultiTargetModel, evaluate_model, serialize_model

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def train_pipeline(config_path: str):
    """Train pipeline for sku demand prediction."""
    params = read_training_pipeline_params(config_path)
    demand_orders = pd.read_csv(params.input_demand_orders)
    demand_orders_status = pd.read_csv(params.input_demand_orders_status)
    # Make sku_demand_by_day
    logger.info("Start training...")
    logger.info("Make sku demand day...")
    sku_demand_day = sku_demand_by_day(demand_orders, demand_orders_status)
    # Save sku_demand_by_day
    logger.info("Saving sku demand day...")
    save_sku_demand_by_day(params.output_sku_demand_day, sku_demand_day)
    logger.info("Sku demand day received successfully!")

    # Make features and targets transformer
    logger.info("Make transformer...")
    transformer = features_and_targets_transformer()
    # Transform data
    logger.info("Transforming data...")
    transformed_data = transformer.fit_transform(sku_demand_day)
    logger.info("Complete!")
    # Save transformed data
    logger.info("Saving transformed data...")
    save_transformed_data(params.output_features_and_targets, transformed_data)
    # Split data
    logger.info("Splitting data...")
    train, test = split_train_test(transformed_data, params.split_params.test_days)
    print(f"Train dataset\n {train.head()}")
    print(f"Test dataset\n {test.head()}")
    # Train model
    logger.info("Training model...")
    model = MultiTargetModel(params.model_params.features)
    model.fit(train)
    # Make predictions
    logger.info("Making predictions...")
    predictions = model.predict(test)
    logger.info(f"Predictions is\n {predictions}")
    # Save predictions to .csv
    logger.info("Saving predictions...")
    predictions.to_csv(params.output_predictions, index=False)
    # Evaluate model
    logger.info("Evaluating model...")
    losses = evaluate_model(test, predictions)
    logger.info(f"Losses is {losses}")
    logger.info("Finish training model")
    # Save losses in dump .json
    with open(params.output_losses, "w") as file:
        json.dump(losses, file)
    # Serialize model
    logger.info("Saving model...")
    serialize_model(model, params.output_model)
    logger.info("Model saved successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/train_config.yaml")
    args = parser.parse_args()
    train_pipeline(args.config)
