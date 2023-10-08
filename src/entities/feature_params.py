from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class FeatureParams:
    """
    Class for feature parameters.
    """

    sku_demand_day: List[str]
    features: Dict[str, Tuple[str, int, str, Optional[int]]]
    targets: Dict[str, Tuple[str, int]]
