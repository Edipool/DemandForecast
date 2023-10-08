from dataclasses import dataclass
from typing import List


@dataclass
class ModelParams:
    """
    Class for model parameters.
    """

    features: List[str]
    horizons: List[int]
    quantiles: List[float]
