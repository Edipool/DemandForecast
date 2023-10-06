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
    with open(path, "r") as input_stream:
        config_dict = yaml.safe_load(input_stream)
        schema = TrainingPipelineParamsSchema().load(config_dict)
        logger.info("Schema loaded successfully")
        return schema


if __name__ == "__main__":
    read_training_pipeline_params(PATH)
