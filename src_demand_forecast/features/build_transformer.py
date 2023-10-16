import logging
import sys

import pandas as pd
from sklearn.pipeline import Pipeline

from src_demand_forecast.entities.train_pipeline_params import read_training_pipeline_params
from src_demand_forecast.features.AddFeatures import AddFeatures
from src_demand_forecast.features.AddTargets import AddTargets

PATH = "configs/train_config.yaml"
params = read_training_pipeline_params(PATH)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def features_and_targets_transformer() -> Pipeline:
    """Builds transformer from config.

    Returns:
        Pipeline: The transformer."""
    transformer = Pipeline(
        [
            (
                "feature_transformer",
                AddFeatures(features=params.feature_params.features),
            ),
            ("target_transformer", AddTargets(targets=params.feature_params.targets)),
        ]
    )
    logger.info("Transformer is built: %s", transformer)
    return transformer


def save_transformed_data(path: str, data: pd.DataFrame):
    data.to_csv(path, index=False, sep=",")
