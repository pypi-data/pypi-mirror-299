import numpy as np
import pandas as pd
from public import public
import logging
import seaborn as sns
from IPython.display import display
from matplotlib import pyplot as plt

from ehr.utilities import _pandas

logger = logging.getLogger(__name__)


@public
def profile_numeric_series(s: pd.Series, percentiles=None, show_describe=True, show_distribution=True, figsize=None, **histplot_kwargs):
    """Print basic statistic and plot distribution for each consecutive range defined in percentiles for a pandas series

    Args:
        s: pd.Series
        percentiles: list of float between [0, 1], default is [0, 0.01, 0.99, 1]
        show_describe: boolean
        show_distribution: boolean
    """
    percentiles = [0, 0.01, 0.99, 1] if percentiles is None else percentiles
    if any(map(lambda x: isinstance(x, str), s)):
        logger.info("array contains string, skipped.")
        return

    s = _pandas.clean_numeric_array(s)

    if len(s) == 0:
        logger.info(f"There is no numeric value")
        return

    if show_describe:
        # .describe() always print out min and max value, so remove 0 and 1 if exists
        p = [i for i in percentiles if i not in {0, 1}]
        display(s.describe(percentiles=p).to_frame().T)

    if show_distribution:
        qth_percentiles = [*map(lambda x: 100 * x, percentiles)]
        cutoff = np.percentile(s, qth_percentiles)
        # try:
        #     cutoff = np.percentile(s, qth_percentiles)
        # except TypeError as e:
        #     logger.error(f"distribution plot is not proceeded becasue of exception {e}")
        #     return

        fig, ax = plt.subplots(1, len(cutoff) - 1, figsize=figsize)
        for i in range(len(ax)):
            array = s[s.between(cutoff[i], cutoff[i + 1])]
            # sns.distplot(array, kde=False, ax=ax[i], **distplot_kwargs)
            sns.histplot(array, kde=False, ax=ax[i], **histplot_kwargs)
            ax[i].set_title(f"{len(array)} records")
            
            ax[i].set_xlabel(f"({qth_percentiles[i]}, {qth_percentiles[i + 1]})th percentile")
            # ax[i].set_xlabel(f"({qth_percentiles[i]}, {qth_percentiles[i + 1]})th percentile -> ({cutoff[i]:.1f}, {cutoff[i + 1]:.1f})")

        plt.show()
