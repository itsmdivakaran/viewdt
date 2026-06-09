from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional


@dataclass
class ViewdtOptions:
    theme: Literal["auto", "light", "dark"] = "auto"
    show_labels: bool = True
    histograms: bool = True
    missing_bars: bool = True
    type_badges: bool = True
    insights: bool = True
    query_builder: bool = True
    column_picker: bool = True
    code_export: bool = True
    global_search: bool = True
    na_string: str = "NA"
    hidden_columns: Optional[List[str]] = None
    page_size: int = 200
    hist_bins: int = 20
    top_n: int = 10
    max_cells: int = 5_000_000

    def to_dict(self) -> dict:
        return {
            "theme": self.theme,
            "show_labels": self.show_labels,
            "histograms": self.histograms,
            "missing_bars": self.missing_bars,
            "type_badges": self.type_badges,
            "insights": self.insights,
            "query_builder": self.query_builder,
            "column_picker": self.column_picker,
            "code_export": self.code_export,
            "global_search": self.global_search,
            "na_string": self.na_string,
            "hidden_columns": list(self.hidden_columns or []),
            "page_size": self.page_size,
        }


def viewdt_options(
    theme: Literal["auto", "light", "dark"] = "auto",
    show_labels: bool = True,
    histograms: bool = True,
    missing_bars: bool = True,
    type_badges: bool = True,
    insights: bool = True,
    query_builder: bool = True,
    column_picker: bool = True,
    code_export: bool = True,
    global_search: bool = True,
    na_string: str = "NA",
    hidden_columns: Optional[List[str]] = None,
    page_size: int = 200,
    hist_bins: int = 20,
    top_n: int = 10,
    max_cells: int = 5_000_000,
) -> ViewdtOptions:
    """Configure the viewdt data explorer widget.

    Parameters
    ----------
    theme:
        UI appearance: "auto" (follows system), "light", or "dark".
    show_labels:
        Display variable-label attributes (from ``pd.Series.attrs["label"]``) in column headers.
    histograms:
        Render mini spark-histograms / category bars in column headers.
    missing_bars:
        Show data-completeness bar at the bottom of each column header.
    type_badges:
        Display data-type badges (#, A, T/F, date) in column headers.
    insights:
        Enable the Data Insights drawer (click any column header to open).
    query_builder:
        Enable the visual query builder with multi-condition AND/OR logic.
    column_picker:
        Enable the column-visibility picker.
    code_export:
        Enable the reproducible code generator (pandas / Python / SQL).
    global_search:
        Enable the global search box.
    na_string:
        Placeholder text shown for missing values.
    hidden_columns:
        Column names hidden on initial render.
    page_size:
        Rows kept in the virtualised DOM buffer (controls memory use).
    hist_bins:
        Number of bins for numeric histograms.
    top_n:
        Number of categories profiled for character columns.
    max_cells:
        Soft safeguard: warn when ``nrow * ncol`` exceeds this threshold.
    """
    return ViewdtOptions(
        theme=theme,
        show_labels=show_labels,
        histograms=histograms,
        missing_bars=missing_bars,
        type_badges=type_badges,
        insights=insights,
        query_builder=query_builder,
        column_picker=column_picker,
        code_export=code_export,
        global_search=global_search,
        na_string=na_string,
        hidden_columns=hidden_columns,
        page_size=page_size,
        hist_bins=hist_bins,
        top_n=top_n,
        max_cells=max_cells,
    )
