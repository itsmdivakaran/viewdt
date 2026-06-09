from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd


def _get_kind(series: pd.Series) -> str:
    dtype = series.dtype
    if pd.api.types.is_bool_dtype(dtype):
        return "logical"
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "datetime"
    if hasattr(dtype, "tz"):
        return "datetime"
    if pd.api.types.is_numeric_dtype(dtype):
        return "numeric"
    return "character"


def _serialize_scalar(val: Any) -> Any:
    """Convert a pandas scalar to a JSON-safe Python type."""
    try:
        if pd.isna(val):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(val, (bool, np.bool_)):
        return bool(val)
    if isinstance(val, np.integer):
        return int(val)
    if isinstance(val, np.floating):
        f = float(val)
        return None if (f != f or abs(f) == float("inf")) else f
    if isinstance(val, pd.Timestamp):
        return val.isoformat()
    return val


def profile_column(series: pd.Series, hist_bins: int = 20, top_n: int = 10) -> Dict[str, Any]:
    n_total = len(series)
    n_missing = int(series.isna().sum())
    completeness = 1.0 - n_missing / n_total if n_total > 0 else 1.0
    kind = _get_kind(series)
    label = series.attrs.get("label", None)

    profile: Dict[str, Any] = {
        "name": str(series.name),
        "label": str(label) if label is not None else None,
        "kind": kind,
        "n_total": n_total,
        "n_missing": n_missing,
        "completeness": completeness,
    }

    non_null = series.dropna()

    if kind == "numeric":
        if len(non_null) > 0:
            profile["min"] = _serialize_scalar(non_null.min())
            profile["max"] = _serialize_scalar(non_null.max())
            profile["mean"] = _serialize_scalar(non_null.mean())
            profile["median"] = _serialize_scalar(non_null.median())
            profile["std"] = _serialize_scalar(non_null.std())
            counts, _ = np.histogram(non_null.dropna().astype(float), bins=hist_bins)
            profile["hist_counts"] = counts.tolist()
        else:
            profile["min"] = profile["max"] = profile["mean"] = profile["median"] = profile["std"] = None
            profile["hist_counts"] = []

    elif kind == "character":
        vc = non_null.astype(str).value_counts().head(top_n)
        profile["top_values"] = [{"value": str(k), "count": int(v)} for k, v in vc.items()]
        profile["n_unique"] = int(series.nunique(dropna=True))

    elif kind == "logical":
        if len(non_null) > 0:
            bool_series = non_null.astype(bool)
            profile["n_true"] = int(bool_series.sum())
            profile["n_false"] = int((~bool_series).sum())
        else:
            profile["n_true"] = 0
            profile["n_false"] = 0

    elif kind == "datetime":
        if len(non_null) > 0:
            profile["min"] = str(non_null.min())
            profile["max"] = str(non_null.max())
            ts = non_null.astype(np.int64)
            counts, _ = np.histogram(ts, bins=hist_bins)
            profile["hist_counts"] = counts.tolist()
        else:
            profile["min"] = profile["max"] = None
            profile["hist_counts"] = []

    return profile


def profile_dataframe(
    df: pd.DataFrame,
    hist_bins: int = 20,
    top_n: int = 10,
) -> List[Dict[str, Any]]:
    return [profile_column(df[col], hist_bins=hist_bins, top_n=top_n) for col in df.columns]


def serialize_rows(df: pd.DataFrame) -> list:
    """Convert DataFrame rows to a list of lists with JSON-safe values."""
    result = []
    for row in df.itertuples(index=False, name=None):
        result.append([_serialize_scalar(v) for v in row])
    return result
