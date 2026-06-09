from __future__ import annotations

import sys
from typing import Optional

import pandas as pd

from .options import ViewdtOptions, viewdt_options
from .widget import ViewdtWidget, generate_html


def viewdt(
    data: pd.DataFrame,
    options: Optional[ViewdtOptions] = None,
    dataset_name: Optional[str] = None,
    *,
    width: Optional[int] = None,
    height: Optional[int] = None,
    elementId: Optional[str] = None,
) -> ViewdtWidget:
    """Create an interactive data-explorer widget from a pandas DataFrame.

    Mirrors the R ViewR ``viewdt()`` function exactly.

    Parameters
    ----------
    data:
        A ``pandas.DataFrame`` to explore.
    options:
        Configuration created via :func:`viewdt_options`.
        Defaults to ``viewdt_options()`` (all features on, auto theme).
    dataset_name:
        Variable name used in generated reproducible code.
        Defaults to the name of the variable passed as *data*
        (inferred from the call site via ``sys._getframe``).
    width, height:
        Ignored (kept for API symmetry with the R htmlwidget signature).
        The widget is fully responsive.
    elementId:
        Ignored (kept for API symmetry).

    Returns
    -------
    ViewdtWidget
        Displays inline in Jupyter notebooks via ``_repr_html_``.
        Call ``.show()`` to open in a browser, or ``.save(path)``
        to export a standalone HTML file.

    Examples
    --------
    >>> import pandas as pd
    >>> from viewdt import viewdt, viewdt_options
    >>> df = pd.read_csv("data.csv")
    >>> viewdt(df)
    >>> viewdt(df, options=viewdt_options(theme="dark", hidden_columns=["id"]))
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"viewdt() expects a pandas DataFrame, got {type(data).__name__}")

    if options is None:
        options = viewdt_options()

    if dataset_name is None:
        try:
            frame = sys._getframe(1)
            # Walk locals of caller to find which variable holds `data`
            for name, val in frame.f_locals.items():
                if val is data:
                    dataset_name = name
                    break
        except Exception:
            pass
        if dataset_name is None:
            dataset_name = "df"

    html = generate_html(data, options, dataset_name)
    return ViewdtWidget(html)


def save_viewdt(
    data: pd.DataFrame,
    path: str,
    options: Optional[ViewdtOptions] = None,
    dataset_name: Optional[str] = None,
) -> None:
    """Export an interactive data-explorer widget to a standalone HTML file.

    Parameters
    ----------
    data:
        A ``pandas.DataFrame`` to explore.
    path:
        Destination file path (e.g. ``"output.html"``).
    options:
        Configuration created via :func:`viewdt_options`.
    dataset_name:
        Variable name used in generated code. Inferred automatically if omitted.
    """
    if dataset_name is None:
        try:
            frame = sys._getframe(1)
            for name, val in frame.f_locals.items():
                if val is data:
                    dataset_name = name
                    break
        except Exception:
            pass
        if dataset_name is None:
            dataset_name = "df"

    widget = viewdt(data, options=options, dataset_name=dataset_name)
    widget.save(path)
