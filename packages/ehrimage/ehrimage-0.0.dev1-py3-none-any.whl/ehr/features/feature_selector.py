# Created by san at 2/4/24
import logging
import numpy as np
import pandas as pd
from public import public

from ehr.utilities import _pandas

logger = logging.getLogger(__name__)


@public
def has_std(s: pd.Series, min_std: float = 0, max_std: float = np.inf):
    """Check if a array's std statistic falls in range [min_std, max_std)"""
    # if there is string value in array, will abort immediately
    # didn't explicitly extract numeric values only becasue of performance consideration
    if any(map(lambda x: isinstance(x, str), s)):
        logger.info("array contains string, return False.")
        return False

    s = _pandas.clean_numeric_array(s)
    stats = s.describe()
    std = stats.get("std")

    if std is None:
        # when "std" metric doesn't exist
        return False

    return min_std <= std < max_std
