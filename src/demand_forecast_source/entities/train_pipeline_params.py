import logging
import sys
from dataclasses import dataclass, field

import yaml
from marshmallow_dataclass import class_schema

from src.entities.feature_params import FeatureParams
from src.entities.model_params import ModelParams
from src.entities.split_params import SplitParams

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

PATH = "configs/train_config.yaml"


@dataclass()
class TrainPipelineParams:
    """
    The class makes it possible to store all the parameters of the training pipeline in one place.

    Attributes:
        feature_params (FeatureParams): The parameters for the features.
        split_params (SplitParams): The parameters for the split.
        model_params (ModelParams): The parameters for the model.
        input_demand_orders (str): The path to the demand_orders csv file.
        input_demand_orders_status (str): The path to the demand_orders_status csv file.
        output_sku_demand_day (str): The path to the sku_demand_day csv file.
        output_features_and_targets (str): The path to the features_and_targets csv file.
        output_losses (str): The path to the losses json file.
        output_model (str): The path to the model pkl file.
        input_sales (str): The path to the sales csv file.
        input_features (str): The path to the features csv file.
        output_predictions (str): The path to the predictions csv file.
    """

    feature_params: FeatureParams
    split_params: SplitParams
    model_params: ModelParams
    input_demand_orders: str = field(default="data/raw/demand_orders_2023_09_22.csv")
    input_demand_orders_status: str = field(
        default="data/raw/demand_orders_status_2023_09_22.csv"
    )
    output_sku_demand_day: str = field(default="data/processed/sales.csv")
    output_features_and_targets: str = field(
        default="data/processed/features_targets.csv"
    )
    output_losses: str = field(default="models/losses.json")
    output_model: str = field(default="models/model.pkl")
    input_sales: str = field(default="data/raw/sales.csv")
    input_features: str = field(default="data/raw/features.csv")
    output_predictions: str = field(default="data/processed/predictions.csv")


TrainingPipelineParamsSchema = class_schema(TrainPipelineParams)


def read_training_pipeline_params(path: str) -> TrainPipelineParams:
    """
    Read the training pipeline parameters from the yaml file.

    Parameters:
        path (str): The path to the yaml file.

    Returns:
        TrainPipelineParams: The parameters for the training pipeline.
    """
    with open(path, "r") as input_stream:
        config_dict = yaml.safe_load(input_stream)
        schema = TrainingPipelineParamsSchema().load(config_dict)
        logger.info("Schema loaded successfully")
        return schema


if __name__ == "__main__":
    read_training_pipeline_params(PATH)
