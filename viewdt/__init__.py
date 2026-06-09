"""viewdt — Advanced interactive data table widget for pandas DataFrames.

Python port of the R ViewR ``viewdt()`` function.

Quick-start
-----------
>>> import pandas as pd
>>> from viewdt import viewdt, viewdt_options
>>>
>>> df = pd.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]})
>>> viewdt(df)                                      # Jupyter: renders inline
>>> viewdt(df).show()                               # browser
>>> viewdt(df).save("explorer.html")                # standalone file
>>>
>>> viewdt(df, options=viewdt_options(theme="dark", histograms=False))
"""

from .core import save_viewdt, viewdt
from .options import ViewdtOptions, viewdt_options
from .widget import ViewdtWidget

__all__ = [
    "viewdt",
    "save_viewdt",
    "viewdt_options",
    "ViewdtOptions",
    "ViewdtWidget",
]
__version__ = "1.0.0"
