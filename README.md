# viewdt

**Advanced interactive data table widget for pandas DataFrames — Python port of the R [ViewR](https://itsmdivakaran.github.io/viewR/) `viewdt()` function.**

`viewdt()` transforms any pandas DataFrame into a high-performance, fully self-contained HTML explorer with zero browser-side dependencies. Column statistics are profiled in Python before the page renders, so the widget is fast even on large datasets.

---

## Features

| Feature | Details |
|---|---|
| **Type badges** | `#` numeric &nbsp; `A` text &nbsp; `T/F` logical &nbsp; `⏱` datetime |
| **Spark histograms** | Inline SVG mini-charts in every column header |
| **Completeness bars** | Per-column fill-rate indicator (green / amber / red) |
| **Column labels** | Reads `series.attrs["label"]` — compatible with haven / ADaM clinical datasets |
| **Virtualised grid** | Renders only visible rows — handles hundreds of thousands of rows smoothly |
| **Global search** | Live cross-column text filter |
| **Visual query builder** | Multi-condition AND / OR filtering with type-aware operators |
| **Data Insights drawer** | Full histogram, descriptive stats, and category charts — click any column header |
| **Column picker** | Toggle column visibility at runtime |
| **Code export** | Generates **pandas**, **Python**, and **SQL** that reproduce the current filter state |
| **Dark / light / auto theme** | Follows the system preference by default; toggle at runtime |
| **Standalone HTML** | One self-contained file, no CDN or internet connection required |

---

## Installation

```bash
pip install viewdt
```

Python 3.9+ and pandas 1.3+ are required. No JavaScript build step is needed.

---

## Quick start

```python
import pandas as pd
from viewdt import viewdt

df = pd.read_csv("sales.csv")
viewdt(df)               # renders inline in Jupyter
viewdt(df).show()        # opens in the default browser
viewdt(df).save("explorer.html")  # exports a standalone file
```

Or explore one of the built-in sample datasets immediately:

```python
from viewdt import viewdt, load_iris, load_mtcars, load_titanic

viewdt(load_iris())       # 150 rows — flower measurements
viewdt(load_mtcars())     # 32 rows  — 1974 car specs
viewdt(load_titanic())    # 891 rows — survival data with missing values
```

---

## API reference

### `viewdt(data, options=None, dataset_name=None)`

Create an interactive data-explorer widget from a pandas DataFrame.

**Parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `pd.DataFrame` | required | The DataFrame to explore |
| `options` | `ViewdtOptions` | `viewdt_options()` | Configuration object — see `viewdt_options()` below |
| `dataset_name` | `str` | inferred | Variable name substituted in generated code. Auto-detected from the call site if omitted |

**Returns** `ViewdtWidget`

**Widget methods**

| Method | Description |
|---|---|
| `.show()` | Open the widget in the default web browser |
| `.save(path)` | Export to a standalone HTML file |
| `_repr_html_()` | Renders inline in Jupyter / VS Code notebooks automatically |

---

### `viewdt_options(**kwargs) → ViewdtOptions`

Build a configuration object to pass to `viewdt()`.  
All parameters are keyword-only and have sensible defaults — pass only what you want to change.

```python
from viewdt import viewdt, viewdt_options

viewdt(df, options=viewdt_options(
    theme="dark",
    hidden_columns=["internal_id", "created_at"],
    hist_bins=30,
    top_n=15,
))
```

**Options reference**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `theme` | `"auto"` \| `"light"` \| `"dark"` | `"auto"` | UI colour scheme. `"auto"` follows the OS preference |
| `show_labels` | `bool` | `True` | Show variable labels from `series.attrs["label"]` |
| `histograms` | `bool` | `True` | Render spark-histograms / category bars in column headers |
| `missing_bars` | `bool` | `True` | Show the data-completeness bar at the bottom of each header |
| `type_badges` | `bool` | `True` | Show data-type badges in column headers |
| `insights` | `bool` | `True` | Enable the Data Insights drawer (click any column header) |
| `query_builder` | `bool` | `True` | Enable the visual query builder |
| `column_picker` | `bool` | `True` | Enable the column-visibility picker |
| `code_export` | `bool` | `True` | Enable the reproducible code generator |
| `global_search` | `bool` | `True` | Enable the global search box |
| `na_string` | `str` | `"NA"` | Text displayed for missing values |
| `hidden_columns` | `list[str]` \| `None` | `None` | Columns hidden on initial render |
| `page_size` | `int` | `200` | Rows kept in the virtualised DOM buffer |
| `hist_bins` | `int` | `20` | Bin count for numeric / datetime histograms |
| `top_n` | `int` | `10` | Number of categories profiled for text columns |
| `max_cells` | `int` | `5_000_000` | Warn when `nrow × ncol` exceeds this threshold |

---

### `save_viewdt(data, path, options=None, dataset_name=None)`

Convenience wrapper — profiles *data* and writes the widget directly to *path*.

```python
from viewdt import save_viewdt

save_viewdt(df, "report.html")
save_viewdt(df, "report_dark.html", options=viewdt_options(theme="dark"))
```

---

## Built-in datasets

Seven sample datasets are included — no internet connection required.

| Loader | Rows | Columns | Description |
|---|---|---|---|
| `load_iris()` | 150 | 5 | Fisher's Iris flower measurements — setosa, versicolor, virginica |
| `load_mtcars()` | 32 | 12 | Motor Trend Car Road Tests 1974 — mpg, hp, weight, transmission |
| `load_penguins()` | 344 | 8 | Palmer Archipelago penguins — bill & flipper measurements (with NaNs) |
| `load_tips()` | 244 | 7 | Restaurant tips — bill, tip, sex, smoker, day, time, party size |
| `load_gapminder()` | 444 | 6 | Gapminder — country, continent, year, life expectancy, population, GDP |
| `load_titanic()` | 891 | 9 | Titanic passengers — survival, class, sex, age (with NaNs), fare |
| `load_stocks()` | 1260 | 4 | Daily closing prices — AAPL, GOOG, MSFT, AMZN, META (datetime column) |

```python
from viewdt import (
    viewdt, viewdt_options,
    load_iris, load_mtcars, load_penguins,
    load_tips, load_gapminder, load_titanic, load_stocks,
    list_datasets,
)

# See all available datasets
viewdt(list_datasets())

# Iris — type badges, spark histograms, column labels
viewdt(load_iris())

# mtcars — all-numeric, code export
viewdt(load_mtcars(), options=viewdt_options(theme="dark"))

# Penguins — completeness bars (missing values in age, sex)
viewdt(load_penguins())

# Gapminder — try the query builder: continent = "Asia", year >= 1990
viewdt(load_gapminder())

# Titanic — filter survived = 1, pclass = 1 to explore first-class survivors
viewdt(load_titanic(), options=viewdt_options(hidden_columns=["name"]))

# Stocks — datetime column, time-series data
viewdt(load_stocks())
```

---

## Examples

### Dark theme with pre-hidden columns

```python
from viewdt import viewdt, viewdt_options

viewdt(
    df,
    options=viewdt_options(
        theme="dark",
        hidden_columns=["row_id", "updated_at"],
    ),
)
```

### Clinical / labelled data (haven / ADaM)

Column labels stored in `series.attrs["label"]` are shown below the column name in the header — the same behaviour as the R ViewR package with haven-imported datasets.

```python
df["AVAL"].attrs["label"] = "Analysis Value"
df["PARAMCD"].attrs["label"] = "Parameter Code"

viewdt(df)  # labels appear in every column header
```

### Lightweight view — disable heavy features

```python
viewdt(
    df,
    options=viewdt_options(
        histograms=False,
        insights=False,
        query_builder=False,
    ),
)
```

### Large DataFrames

```python
# viewdt warns automatically when nrow × ncol > max_cells (default 5 M).
# Sample before exploring if needed:
viewdt(df.sample(50_000))

# Or raise the threshold:
viewdt(df, options=viewdt_options(max_cells=20_000_000))
```

### Export to HTML for sharing

```python
from viewdt import save_viewdt, viewdt_options

save_viewdt(
    df,
    "team_report.html",
    options=viewdt_options(theme="light", code_export=False),
    dataset_name="sales_q1",
)
```

---

## Query builder operators

The visual query builder exposes type-appropriate operators for each column:

| Column type | Available operators |
|---|---|
| Numeric | `=` `≠` `<` `≤` `>` `≥` `is null` `not null` |
| Text | `=` `≠` `contains` `!contains` `in` `!in` `is null` `not null` |
| Logical | `is true` `is false` `is null` `not null` |
| Datetime | `=` `<` `≤` `>` `≥` `is null` `not null` |

The `in` / `!in` operators accept a comma-separated list of values in the input field.

---

## Code export

The **Code** button generates reproducible code that matches the current filter state and column selection in three dialects:

**pandas**
```python
mask = (
    df['category'].isin(['A', 'B']) &
    (df['price'] > 50)
)
df = df[mask]
df = df[['category', 'price', 'score']]
```

**Python**
```python
import pandas as pd

result = df[
    df['category'].isin(['A', 'B']) &
    (df['price'] > 50)
]
result = result[['category', 'price', 'score']]
```

**SQL**
```sql
SELECT "category", "price", "score"
FROM "df"
WHERE "category" IN ('A', 'B')
  AND "price" > 50;
```

---

## Comparison with R ViewR

| Feature | R `viewdt()` | Python `viewdt()` |
|---|---|---|
| Data input | `data.frame` / `tibble` | `pd.DataFrame` |
| Column profiling | In R, before render | In Python, before render |
| Spark charts | SVG, vanilla JS | SVG, vanilla JS |
| Code export | dplyr / base R / SQL | pandas / Python / SQL |
| Column labels | `label` attribute (haven) | `series.attrs["label"]` |
| Standalone output | `htmlwidget` | `ViewdtWidget` → `.save()` |
| Jupyter support | via `htmlwidgets` | via `_repr_html_()` |
| Dependencies | R packages | pandas, numpy |
| JS dependencies | None | None |

---

## Development

```bash
git clone https://github.com/itsmdivakaran/viewdt-python
cd viewdt-python
pip install -e ".[notebook]"
```

Run the smoke test:

```bash
python -c "
import pandas as pd, numpy as np
from viewdt import viewdt
df = pd.DataFrame({'x': np.random.randn(100), 'y': list('ABCD') * 25})
viewdt(df).show()
"
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Mahesh Divakaran**  
Research Scholar, Amity University Uttar Pradesh

- GitHub: [github.com/itsmdivakaran](https://github.com/itsmdivakaran)
- ORCID: [0000-0002-3488-0857](https://orcid.org/0000-0002-3488-0857)
- Email: imaheshdivakaran@gmail.com

---

## Citation

If you use **viewdt** in academic work, please cite the original R package:

> Divakaran M (2026). *ViewR: Interactive Data Viewer, Filter, and Editor.*
> R package version 0.2.0.
> <https://itsmdivakaran.github.io/viewR/>

BibTeX:

```bibtex
@Manual{ViewR,
  title  = {{ViewR}: Interactive Data Viewer, Filter, and Editor},
  author = {Mahesh Divakaran},
  year   = {2026},
  note   = {R package version 0.2.0},
  url    = {https://itsmdivakaran.github.io/viewR/},
}
```

---

## Acknowledgements

Python port of the [ViewR](https://itsmdivakaran.github.io/viewR/) R package
([CRAN](https://cran.r-project.org/web/packages/ViewR/index.html)).
The widget design, feature set, and `viewdt_options()` API are derived directly
from the R implementation by the same author.
