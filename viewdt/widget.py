from __future__ import annotations

import json
import warnings
from typing import Optional

import numpy as np
import pandas as pd

from .options import ViewdtOptions
from .profiler import profile_dataframe, serialize_rows
from .template import HTML_TEMPLATE


class _Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            f = float(obj)
            return None if (f != f or abs(f) == float("inf")) else f
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        try:
            if hasattr(obj, "item"):
                return obj.item()
        except Exception:
            pass
        return super().default(obj)


class ViewdtWidget:
    """A self-contained interactive data explorer HTML widget."""

    def __init__(self, html: str) -> None:
        self._html = html

    # ── Jupyter display ──────────────────────────────────────────────────────
    def _repr_html_(self) -> str:
        # Wrap in an iframe so the widget's full-page CSS doesn't leak into
        # the notebook.
        import base64
        b64 = base64.b64encode(self._html.encode("utf-8")).decode("ascii")
        return (
            f'<iframe src="data:text/html;base64,{b64}" '
            f'width="100%" height="600" frameborder="0" '
            f'style="border:1px solid #e5e7eb;border-radius:8px"></iframe>'
        )

    # ── File I/O ─────────────────────────────────────────────────────────────
    def save(self, path: str) -> None:
        """Save the widget to a standalone HTML file."""
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(self._html)
        print(f"Saved: {path}")

    def show(self) -> None:
        """Open the widget in the default web browser."""
        import os
        import tempfile
        import webbrowser

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(self._html)
            tmp = fh.name

        webbrowser.open("file://" + os.path.abspath(tmp))

    def __repr__(self) -> str:
        return f"<ViewdtWidget rows={self._html.count('grid-row')}>"


def generate_html(
    df: pd.DataFrame,
    options: ViewdtOptions,
    dataset_name: str,
) -> str:
    """Profile *df* in Python and bake the result into the HTML template."""
    n_cells = len(df) * len(df.columns)
    if n_cells > options.max_cells:
        warnings.warn(
            f"DataFrame has {n_cells:,} cells (> {options.max_cells:,}). "
            "Consider sampling before calling viewdt().",
            stacklevel=4,
        )

    col_profiles = profile_dataframe(df, hist_bins=options.hist_bins, top_n=options.top_n)
    row_data = serialize_rows(df)

    payload = {
        "columns":      col_profiles,
        "rows":         row_data,
        "dataset_name": dataset_name,
        "options":      options.to_dict(),
    }

    json_str = json.dumps(payload, cls=_Encoder, ensure_ascii=False, separators=(",", ":"))
    return HTML_TEMPLATE.replace("<<<DATA>>>", json_str)
