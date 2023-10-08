from dataclasses import dataclass


@dataclass
class SplitParams:
    """
    Class for split parameters.
    """

    test_days: int
