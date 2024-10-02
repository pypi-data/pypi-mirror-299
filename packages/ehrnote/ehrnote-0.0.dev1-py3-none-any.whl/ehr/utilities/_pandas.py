# Created by san at 2/4/24
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

__all__ = [
    "clean_numeric_array",
]


def clean_numeric_array(s: pd.Series):
    # start with a copy
    s = s.copy()

    # remove inf
    if max(s) == np.inf or min(s) == -np.inf:
        mask = (s == np.inf) | (s == -np.inf)
        s = s[~mask]
        logger.info(f"Removed {mask.sum()} records with infinite values")

    # remove NA
    if s.isna().sum() > 0:
        mask = s.isna()
        s = s[~mask]
        logger.info(f"Removed {mask.sum()} records with NA values")

    return s
