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

Built-in datasets
-----------------
>>> from viewdt.datasets import load_iris, load_mtcars, load_penguins
>>> from viewdt.datasets import load_tips, load_gapminder, load_titanic
>>> from viewdt.datasets import load_stocks, list_datasets
>>>
>>> viewdt(load_iris())
>>> viewdt(load_mtcars())
>>> list_datasets()          # summary table of all available datasets
"""

from .core import save_viewdt, viewdt
from .datasets import (
    list_datasets,
    load_gapminder,
    load_iris,
    load_mtcars,
    load_penguins,
    load_stocks,
    load_tips,
    load_titanic,
)
from .options import ViewdtOptions, viewdt_options
from .widget import ViewdtWidget

__all__ = [
    # Core API
    "viewdt",
    "save_viewdt",
    "viewdt_options",
    "ViewdtOptions",
    "ViewdtWidget",
    # Datasets
    "load_iris",
    "load_mtcars",
    "load_penguins",
    "load_tips",
    "load_gapminder",
    "load_titanic",
    "load_stocks",
    "list_datasets",
]
__version__ = "1.0.0"
