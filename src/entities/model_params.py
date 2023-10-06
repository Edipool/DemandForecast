from dataclasses import dataclass
from typing import List


@dataclass
class ModelParams:
    features: List[str]
    horizons: List[int]
    quantiles: List[float]
