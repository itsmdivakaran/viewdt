"""Built-in sample datasets for viewdt demonstrations.

All datasets are either embedded from their canonical public-domain sources
or generated with fixed seeds to be fully reproducible without an internet
connection.

Available datasets
------------------
load_iris()       Fisher's Iris flower measurements              150 × 5
load_mtcars()     Motor Trend Car Road Tests 1974                 32 × 12
load_penguins()   Palmer Archipelago penguin measurements        344 × 8
load_tips()       Restaurant tip data                            244 × 7
load_gapminder()  Gapminder world health & economics             444 × 6
load_titanic()    Titanic passenger survival                     891 × 9
load_stocks()     Daily closing prices — 5 tech tickers         1260 × 4
list_datasets()   Summary table of all available datasets          7 × 5
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ── iris ──────────────────────────────────────────────────────────────────────

def load_iris() -> pd.DataFrame:
    """Fisher's Iris flower measurements (150 rows × 5 columns).

    The classic Edgar Anderson / R.A. Fisher dataset. Generated from the
    known per-species means and standard deviations with a fixed seed so
    the result is stable and representative.

    Columns
    -------
    sepal_length, sepal_width, petal_length, petal_width : float  (cm)
    species : str  — setosa | versicolor | virginica

    Column labels (``series.attrs["label"]``) are set for all numeric columns.
    """
    rng = np.random.default_rng(42)
    n = 50
    # (species, sl_mean, sl_std, sw_mean, sw_std, pl_mean, pl_std, pw_mean, pw_std)
    specs = [
        ("setosa",     5.006, 0.352, 3.428, 0.379, 1.462, 0.174, 0.246, 0.105),
        ("versicolor", 5.936, 0.516, 2.770, 0.314, 4.260, 0.470, 1.326, 0.198),
        ("virginica",  6.588, 0.636, 2.974, 0.322, 5.552, 0.552, 2.026, 0.275),
    ]
    parts = []
    for sp, slm, sls, swm, sws, plm, pls, pwm, pws in specs:
        parts.append(pd.DataFrame({
            "sepal_length": np.round(np.clip(rng.normal(slm, sls, n), 4.0, 8.0), 1),
            "sepal_width":  np.round(np.clip(rng.normal(swm, sws, n), 2.0, 5.0), 1),
            "petal_length": np.round(np.clip(rng.normal(plm, pls, n), 0.5, 7.0), 1),
            "petal_width":  np.round(np.clip(rng.normal(pwm, pws, n), 0.1, 3.0), 1),
            "species": sp,
        }))
    df = pd.concat(parts, ignore_index=True)
    df["sepal_length"].attrs["label"] = "Sepal Length (cm)"
    df["sepal_width"].attrs["label"]  = "Sepal Width (cm)"
    df["petal_length"].attrs["label"] = "Petal Length (cm)"
    df["petal_width"].attrs["label"]  = "Petal Width (cm)"
    return df


# ── mtcars ────────────────────────────────────────────────────────────────────

def load_mtcars() -> pd.DataFrame:
    """Motor Trend Car Road Tests, 1974 (32 rows × 12 columns).

    Extracted from the 1974 Motor Trend US magazine. Public domain.

    Columns
    -------
    car      : str    — vehicle name
    mpg      : float  — miles per US gallon
    cyl      : int    — number of cylinders
    disp     : float  — displacement (cu. in.)
    hp       : int    — gross horsepower
    drat     : float  — rear axle ratio
    wt       : float  — weight (1000 lbs)
    qsec     : float  — 1/4 mile time
    vs       : int    — engine shape (0 = V-shape, 1 = straight)
    am       : int    — transmission (0 = automatic, 1 = manual)
    gear     : int    — number of forward gears
    carb     : int    — number of carburettors
    """
    data = [
        # car,                   mpg,  cyl, disp,   hp, drat,    wt,  qsec, vs, am, gear, carb
        ("Mazda RX4",            21.0,  6, 160.0, 110, 3.90, 2.620, 16.46,  0,  1,  4,  4),
        ("Mazda RX4 Wag",        21.0,  6, 160.0, 110, 3.90, 2.875, 17.02,  0,  1,  4,  4),
        ("Datsun 710",           22.8,  4, 108.0,  93, 3.85, 2.320, 18.61,  1,  1,  4,  1),
        ("Hornet 4 Drive",       21.4,  6, 258.0, 110, 3.08, 3.215, 19.44,  1,  0,  3,  1),
        ("Hornet Sportabout",    18.7,  8, 360.0, 175, 3.15, 3.440, 17.02,  0,  0,  3,  2),
        ("Valiant",              18.1,  6, 225.0, 105, 2.76, 3.460, 20.22,  1,  0,  3,  1),
        ("Duster 360",           14.3,  8, 360.0, 245, 3.21, 3.570, 15.84,  0,  0,  3,  4),
        ("Merc 240D",            24.4,  4, 146.7,  62, 3.69, 3.190, 20.00,  1,  0,  4,  2),
        ("Merc 230",             22.8,  4, 140.8,  95, 3.92, 3.150, 22.90,  1,  0,  4,  2),
        ("Merc 280",             19.2,  6, 167.6, 123, 3.92, 3.440, 18.30,  1,  0,  4,  4),
        ("Merc 280C",            17.8,  6, 167.6, 123, 3.92, 3.440, 18.90,  1,  0,  4,  4),
        ("Merc 450SE",           16.4,  8, 275.8, 180, 3.07, 4.070, 17.40,  0,  0,  3,  3),
        ("Merc 450SL",           17.3,  8, 275.8, 180, 3.07, 3.730, 17.60,  0,  0,  3,  3),
        ("Merc 450SLC",          15.2,  8, 275.8, 180, 3.07, 3.780, 18.00,  0,  0,  3,  3),
        ("Cadillac Fleetwood",   10.4,  8, 472.0, 205, 2.93, 5.250, 17.98,  0,  0,  3,  4),
        ("Lincoln Continental",  10.4,  8, 460.0, 215, 3.00, 5.424, 17.82,  0,  0,  3,  4),
        ("Chrysler Imperial",    14.7,  8, 440.0, 230, 3.23, 5.345, 17.42,  0,  0,  3,  4),
        ("Fiat 128",             32.4,  4,  78.7,  66, 4.08, 2.200, 19.47,  1,  1,  4,  1),
        ("Honda Civic",          30.4,  4,  75.7,  52, 4.93, 1.615, 18.52,  1,  1,  4,  2),
        ("Toyota Corolla",       33.9,  4,  71.1,  65, 4.22, 1.835, 19.90,  1,  1,  4,  1),
        ("Toyota Corona",        21.5,  4, 120.1,  97, 3.70, 2.465, 20.01,  1,  0,  3,  1),
        ("Dodge Challenger",     15.5,  8, 318.0, 150, 2.76, 3.520, 16.87,  0,  0,  3,  2),
        ("AMC Javelin",          15.2,  8, 304.0, 150, 3.15, 3.435, 17.30,  0,  0,  3,  2),
        ("Camaro Z28",           13.3,  8, 350.0, 245, 3.73, 3.840, 15.41,  0,  0,  3,  4),
        ("Pontiac Firebird",     19.2,  8, 400.0, 175, 3.08, 3.845, 17.05,  0,  0,  3,  2),
        ("Fiat X1-9",            27.3,  4,  79.0,  66, 4.08, 1.935, 18.90,  1,  1,  4,  1),
        ("Porsche 914-2",        26.0,  4, 120.3,  91, 4.43, 2.140, 16.70,  0,  1,  5,  2),
        ("Lotus Europa",         30.4,  4,  95.1, 113, 3.77, 1.513, 16.90,  1,  1,  5,  2),
        ("Ford Pantera L",       15.8,  8, 351.0, 264, 4.22, 3.170, 14.50,  0,  1,  5,  4),
        ("Ferrari Dino",         19.7,  6, 145.0, 175, 3.62, 2.770, 15.50,  0,  1,  5,  6),
        ("Maserati Bora",        15.0,  8, 301.0, 335, 3.54, 3.570, 14.60,  0,  1,  5,  8),
        ("Volvo 142E",           21.4,  4, 121.0, 109, 4.11, 2.780, 18.60,  1,  1,  4,  2),
    ]
    cols = ["car", "mpg", "cyl", "disp", "hp", "drat", "wt", "qsec", "vs", "am", "gear", "carb"]
    df = pd.DataFrame(data, columns=cols)
    df["mpg"].attrs["label"]  = "Miles per US Gallon"
    df["disp"].attrs["label"] = "Displacement (cu. in.)"
    df["hp"].attrs["label"]   = "Gross Horsepower"
    df["wt"].attrs["label"]   = "Weight (1000 lbs)"
    df["qsec"].attrs["label"] = "1/4 Mile Time (sec)"
    return df


# ── penguins ──────────────────────────────────────────────────────────────────

def load_penguins() -> pd.DataFrame:
    """Palmer Archipelago penguin measurements (344 rows × 8 columns).

    A modern alternative to the Iris dataset. Includes intentional missing
    values (NaN) to demonstrate the completeness-bar feature.

    Columns
    -------
    species          : str    — Adelie | Chinstrap | Gentoo
    island           : str    — Biscoe | Dream | Torgersen
    bill_length_mm   : float  — culmen length (mm), 2 missing
    bill_depth_mm    : float  — culmen depth (mm), 2 missing
    flipper_length_mm: float  — flipper length (mm), 2 missing
    body_mass_g      : float  — body mass (g), 2 missing
    sex              : str    — male | female, 11 missing
    year             : int    — study year (2007–2009)
    """
    rng = np.random.default_rng(7)
    # (species, island, n, bl_μ, bl_σ, bd_μ, bd_σ, fl_μ, fl_σ, bm_μ, bm_σ)
    specs = [
        ("Adelie",    "Torgersen",  52, 38.8, 2.7, 18.3, 1.2, 190.1,  6.4, 3706,  459),
        ("Adelie",    "Dream",      56, 38.5, 2.5, 18.2, 1.2, 189.7,  6.6, 3688,  455),
        ("Adelie",    "Biscoe",     44, 38.9, 2.9, 18.4, 1.2, 188.8,  5.7, 3710,  488),
        ("Chinstrap", "Dream",      68, 48.8, 3.3, 18.4, 1.1, 195.8,  7.1, 3733,  384),
        ("Gentoo",    "Biscoe",    124, 47.5, 3.1, 15.0, 1.0, 217.2,  6.5, 5076,  504),
    ]
    parts = []
    for sp, isl, n, blm, bls, bdm, bds, flm, fls, bmm, bms in specs:
        parts.append(pd.DataFrame({
            "species":           sp,
            "island":            isl,
            "bill_length_mm":    np.round(np.clip(rng.normal(blm, bls, n), 30.0, 65.0), 1),
            "bill_depth_mm":     np.round(np.clip(rng.normal(bdm, bds, n), 12.0, 22.0), 1),
            "flipper_length_mm": np.round(np.clip(rng.normal(flm, fls, n), 170.0, 235.0), 0).astype(int),
            "body_mass_g":       np.round(np.clip(rng.normal(bmm, bms, n), 2500, 6500), 0).astype(int),
            "sex":               rng.choice(["male", "female"], n),
            "year":              rng.choice([2007, 2008, 2009], n),
        }))

    df = pd.concat(parts, ignore_index=True)

    # Inject realistic missing values
    nan_idx_4 = rng.choice(df.index, 4, replace=False)
    nan_idx_11 = rng.choice(df.index, 11, replace=False)
    df.loc[nan_idx_4[:2],  "bill_length_mm"]    = np.nan
    df.loc[nan_idx_4[2:],  "bill_depth_mm"]     = np.nan
    df.loc[rng.choice(df.index, 2, replace=False), "flipper_length_mm"] = np.nan
    df.loc[rng.choice(df.index, 2, replace=False), "body_mass_g"]       = np.nan
    df.loc[nan_idx_11, "sex"] = np.nan

    df["bill_length_mm"].attrs["label"]    = "Bill Length (mm)"
    df["bill_depth_mm"].attrs["label"]     = "Bill Depth (mm)"
    df["flipper_length_mm"].attrs["label"] = "Flipper Length (mm)"
    df["body_mass_g"].attrs["label"]       = "Body Mass (g)"
    return df


# ── tips ──────────────────────────────────────────────────────────────────────

def load_tips() -> pd.DataFrame:
    """Restaurant tip data (244 rows × 7 columns).

    Records of tips left at a restaurant over several months.

    Columns
    -------
    total_bill : float  — meal cost (USD)
    tip        : float  — tip amount (USD)
    sex        : str    — Male | Female  (who paid)
    smoker     : str    — Yes | No
    day        : str    — Thur | Fri | Sat | Sun
    time       : str    — Lunch | Dinner
    size       : int    — party size (1–6)
    """
    rng = np.random.default_rng(13)
    n = 244
    total_bill = np.round(np.clip(rng.lognormal(2.9, 0.5, n), 3.0, 55.0), 2)
    tip_rate   = np.clip(rng.normal(0.16, 0.06, n), 0.04, 0.40)
    tip        = np.round(total_bill * tip_rate, 2)
    df = pd.DataFrame({
        "total_bill": total_bill,
        "tip":        tip,
        "sex":        rng.choice(["Male", "Female"], n, p=[0.64, 0.36]),
        "smoker":     rng.choice(["No", "Yes"],      n, p=[0.62, 0.38]),
        "day":        rng.choice(["Thur", "Fri", "Sat", "Sun"], n, p=[0.25, 0.08, 0.36, 0.31]),
        "time":       rng.choice(["Dinner", "Lunch"], n, p=[0.72, 0.28]),
        "size":       rng.choice([1, 2, 3, 4, 5, 6],  n, p=[0.04, 0.46, 0.18, 0.19, 0.08, 0.05]),
    })
    df["total_bill"].attrs["label"] = "Total Bill (USD)"
    df["tip"].attrs["label"]        = "Tip Amount (USD)"
    return df


# ── gapminder ─────────────────────────────────────────────────────────────────

def load_gapminder() -> pd.DataFrame:
    """Gapminder world health and economics (444 rows × 6 columns).

    37 countries × 12 time points (1952–2007 in 5-year steps).
    Inspired by the Gapminder Foundation data (CC-BY license).

    Columns
    -------
    country    : str    — country name
    continent  : str    — Africa | Americas | Asia | Europe | Oceania
    year       : int    — 1952, 1957, …, 2007
    life_exp   : float  — life expectancy at birth (years)
    population : int    — total population
    gdp_percap : float  — GDP per capita (USD, inflation-adjusted)
    """
    rng = np.random.default_rng(55)
    years = list(range(1952, 2008, 5))

    # (country, continent, le_1952, le_gain_per5yr, pop_1952M, pop_growth, gdp_1952, gdp_growth)
    countries = [
        # Africa
        ("Nigeria",       "Africa",   36.7, 0.55, 33.0, 0.028, 1077, 0.014),
        ("Ethiopia",      "Africa",   34.1, 0.60, 20.2, 0.027,  469, 0.010),
        ("Egypt",         "Africa",   41.9, 0.65, 22.2, 0.023, 1418, 0.032),
        ("South Africa",  "Africa",   45.0, 0.25, 14.2, 0.021, 4725, 0.015),
        ("Kenya",         "Africa",   42.3, 0.50,  6.1, 0.030,  853, 0.012),
        ("Ghana",         "Africa",   43.1, 0.52,  5.4, 0.026,  911, 0.018),
        ("Tanzania",      "Africa",   41.2, 0.55,  8.3, 0.030,  716, 0.011),
        ("Algeria",       "Africa",   43.1, 0.68, 9.28, 0.025, 2449, 0.025),
        # Americas
        ("United States", "Americas", 68.4, 0.22, 157.6, 0.011, 13990, 0.020),
        ("Brazil",        "Americas", 50.9, 0.58,  56.6, 0.020,  2109, 0.028),
        ("Mexico",        "Americas", 50.8, 0.60,  30.1, 0.021,  3478, 0.022),
        ("Argentina",     "Americas", 62.5, 0.34,  17.1, 0.012,  5911, 0.012),
        ("Canada",        "Americas", 68.8, 0.19,  14.8, 0.010, 11367, 0.021),
        ("Colombia",      "Americas", 50.6, 0.55,  12.3, 0.019,  2144, 0.018),
        ("Chile",         "Americas", 54.7, 0.55,   6.1, 0.014,  3940, 0.025),
        # Asia
        ("China",         "Asia",     44.0, 0.60, 556.3, 0.010,   400, 0.055),
        ("India",         "Asia",     37.4, 0.58, 372.0, 0.017,   547, 0.030),
        ("Japan",         "Asia",     63.0, 0.30,  86.5, 0.006,  3217, 0.038),
        ("Indonesia",     "Asia",     37.5, 0.60,  82.1, 0.019,   750, 0.032),
        ("South Korea",   "Asia",     47.5, 0.65,  20.9, 0.011,  1030, 0.062),
        ("Pakistan",      "Asia",     43.4, 0.55,  41.3, 0.026,   684, 0.020),
        ("Bangladesh",    "Asia",     37.5, 0.55,  46.9, 0.022,   684, 0.018),
        ("Thailand",      "Asia",     50.8, 0.55,  21.3, 0.012,   757, 0.040),
        # Europe
        ("Germany",       "Europe",   67.5, 0.20,  69.1, 0.002, 7144, 0.022),
        ("United Kingdom","Europe",   69.2, 0.17,  50.4, 0.003, 9980, 0.020),
        ("France",        "Europe",   67.4, 0.20,  42.5, 0.004, 7030, 0.022),
        ("Italy",         "Europe",   65.9, 0.22,  47.7, 0.003, 4931, 0.024),
        ("Spain",         "Europe",   64.9, 0.24,  28.5, 0.007, 3834, 0.026),
        ("Poland",        "Europe",   61.3, 0.24,  25.0, 0.004, 4030, 0.018),
        ("Netherlands",   "Europe",   72.1, 0.14,  10.4, 0.005, 8942, 0.020),
        ("Russia",        "Europe",   65.5, 0.08, 109.6, 0.004, 6210, 0.012),
        # Oceania
        ("Australia",     "Oceania",  69.1, 0.20,   8.7, 0.013, 10040, 0.020),
        ("New Zealand",   "Oceania",  69.4, 0.18,   1.9, 0.011,  8438, 0.018),
        # Extra Asia / Americas
        ("Vietnam",       "Asia",     40.4, 0.60,  26.2, 0.018,   605, 0.035),
        ("Philippines",   "Asia",     47.8, 0.52,  22.4, 0.021,  1272, 0.022),
        ("Peru",          "Americas", 43.9, 0.55,   8.0, 0.017,  3759, 0.015),
        ("Venezuela",     "Americas", 55.1, 0.42,   5.4, 0.021,  7690, 0.005),
    ]

    rows = []
    for country, continent, le0, le_g, pop0m, pop_g, gdp0, gdp_g in countries:
        for i, yr in enumerate(years):
            le  = round(min(le0 + le_g * i + rng.normal(0, 0.3), 85.0), 2)
            pop = int(pop0m * 1_000_000 * (1 + pop_g) ** i * rng.uniform(0.99, 1.01))
            gdp = round(gdp0 * (1 + gdp_g) ** i * rng.uniform(0.97, 1.03), 2)
            rows.append((country, continent, yr, le, pop, gdp))

    df = pd.DataFrame(rows, columns=["country", "continent", "year", "life_exp", "population", "gdp_percap"])
    df["life_exp"].attrs["label"]   = "Life Expectancy (years)"
    df["gdp_percap"].attrs["label"] = "GDP per Capita (USD)"
    return df


# ── titanic ───────────────────────────────────────────────────────────────────

def load_titanic() -> pd.DataFrame:
    """Titanic passenger survival data (891 rows × 9 columns).

    Synthetic but statistically representative of the canonical Kaggle /
    Vanderbilt Biostatistics version. Contains intentional NaN values in
    ``age`` (~20 %) and ``embarked`` (~0.2 %) to showcase completeness bars.

    Columns
    -------
    survived  : int    — 0 = No, 1 = Yes
    pclass    : int    — ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)
    name      : str    — passenger name (synthetic)
    sex       : str    — male | female
    age       : float  — age in years, ~177 missing
    sib_sp    : int    — siblings/spouses aboard
    parch     : int    — parents/children aboard
    fare      : float  — ticket fare (GBP)
    embarked  : str    — C = Cherbourg | Q = Queenstown | S = Southampton
    """
    rng = np.random.default_rng(19)
    n = 891

    # Realistic class distribution
    pclass = rng.choice([1, 2, 3], n, p=[0.242, 0.206, 0.552])

    # Sex: overall 64.8 % male
    sex = rng.choice(["male", "female"], n, p=[0.648, 0.352])

    # Survival: depends on class and sex
    survival_p = {(1,"female"):0.968,(1,"male"):0.369,(2,"female"):0.921,
                  (2,"male"):0.157,(3,"female"):0.500,(3,"male"):0.135}
    survived = np.array([
        int(rng.random() < survival_p.get((pclass[i], sex[i]), 0.35))
        for i in range(n)
    ])

    # Age: mean ~29.7, std ~14.5, truncated [0.17, 80]
    age = np.round(np.clip(rng.normal(29.7, 14.5, n), 0.17, 80.0), 1)
    # Inject ~20 % missing
    age[rng.choice(n, 177, replace=False)] = np.nan

    # Fare: correlated with class
    fare_map = {1: (84, 78), 2: (20, 14), 3: (13, 12)}
    fare = np.array([
        round(max(0, rng.normal(*fare_map[pclass[i]])), 2) for i in range(n)
    ])

    # Other columns
    sib_sp   = rng.choice([0, 1, 2, 3, 4, 5, 8], n, p=[0.682, 0.234, 0.031, 0.021, 0.020, 0.005, 0.007])
    parch    = rng.choice([0, 1, 2, 3, 4, 5, 6], n, p=[0.762, 0.132, 0.090, 0.005, 0.004, 0.005, 0.002])
    embarked = rng.choice(["S", "C", "Q"], n, p=[0.722, 0.187, 0.091])
    embarked = embarked.astype(object)
    embarked[rng.choice(n, 2, replace=False)] = np.nan  # 2 missing

    # Synthetic names
    first_names_m = ["John","William","James","Charles","George","Thomas","Henry","Frank","Robert","Edward"]
    first_names_f = ["Mary","Anna","Margaret","Helen","Emma","Ruth","Elizabeth","Florence","Alice","Edith"]
    last_names    = ["Smith","Johnson","Williams","Brown","Jones","Davis","Miller","Wilson","Moore","Taylor",
                     "Anderson","Thomas","Jackson","White","Harris","Martin","Thompson","Garcia","Martinez","Robinson"]
    names = []
    for i in range(n):
        fn = rng.choice(first_names_m if sex[i] == "male" else first_names_f)
        ln = rng.choice(last_names)
        names.append(f"{ln}, {fn}")

    df = pd.DataFrame({
        "survived": survived,
        "pclass":   pclass,
        "name":     names,
        "sex":      sex,
        "age":      age,
        "sib_sp":   sib_sp,
        "parch":    parch,
        "fare":     fare,
        "embarked": embarked,
    })
    df["fare"].attrs["label"] = "Ticket Fare (GBP)"
    df["age"].attrs["label"]  = "Age (years)"
    return df


# ── stocks ────────────────────────────────────────────────────────────────────

def load_stocks() -> pd.DataFrame:
    """Daily closing prices for 5 tech tickers, 2020–2024 (1260 rows × 4 columns).

    Simulated via a log-normal random walk with realistic parameters.
    Demonstrates the datetime column type in viewdt.

    Columns
    -------
    date   : datetime64  — trading date (business days only)
    ticker : str         — AAPL | GOOG | MSFT | AMZN | META
    price  : float       — closing price (USD)
    volume : int         — shares traded (millions)
    """
    rng = np.random.default_rng(77)
    dates = pd.bdate_range("2020-01-01", periods=252, freq="B")   # ~1 year per ticker = 1260 rows

    tickers = {
        "AAPL": (75.0,   0.0003, 0.015, 80),
        "GOOG": (1400.0, 0.0003, 0.016, 25),
        "MSFT": (160.0,  0.0003, 0.014, 35),
        "AMZN": (1900.0, 0.0004, 0.018, 20),
        "META": (210.0,  0.0002, 0.020, 60),
    }
    rows = []
    for ticker, (start, mu, sigma, avg_vol) in tickers.items():
        log_returns = rng.normal(mu, sigma, len(dates))
        prices = start * np.exp(np.cumsum(log_returns))
        volumes = np.round(avg_vol * rng.lognormal(0, 0.4, len(dates))).astype(int)
        for d, p, v in zip(dates, prices, volumes):
            rows.append({"date": d, "ticker": ticker, "price": round(float(p), 2), "volume_M": int(v)})

    df = pd.DataFrame(rows)
    df["price"].attrs["label"]    = "Closing Price (USD)"
    df["volume_M"].attrs["label"] = "Volume (millions)"
    return df


# ── catalogue ─────────────────────────────────────────────────────────────────

def list_datasets() -> pd.DataFrame:
    """Return a summary DataFrame of all available sample datasets.

    Each row describes one dataset: its loader function name, dimensions,
    column types, and a short description.
    """
    return pd.DataFrame([
        {
            "name":        "iris",
            "loader":      "load_iris()",
            "rows":        150,
            "columns":     5,
            "description": "Fisher's Iris flower measurements — setosa, versicolor, virginica",
        },
        {
            "name":        "mtcars",
            "loader":      "load_mtcars()",
            "rows":        32,
            "columns":     12,
            "description": "Motor Trend Car Road Tests 1974 — mpg, hp, weight, transmission…",
        },
        {
            "name":        "penguins",
            "loader":      "load_penguins()",
            "rows":        344,
            "columns":     8,
            "description": "Palmer Archipelago penguins — bill, flipper, body mass (with NaNs)",
        },
        {
            "name":        "tips",
            "loader":      "load_tips()",
            "rows":        244,
            "columns":     7,
            "description": "Restaurant tip data — bill, tip, sex, smoker, day, time, party size",
        },
        {
            "name":        "gapminder",
            "loader":      "load_gapminder()",
            "rows":        444,
            "columns":     6,
            "description": "Gapminder — country, continent, year, life expectancy, pop, GDP",
        },
        {
            "name":        "titanic",
            "loader":      "load_titanic()",
            "rows":        891,
            "columns":     9,
            "description": "Titanic passengers — survival, class, sex, age (with NaNs), fare",
        },
        {
            "name":        "stocks",
            "loader":      "load_stocks()",
            "rows":        1260,
            "columns":     4,
            "description": "Daily closing prices — AAPL, GOOG, MSFT, AMZN, META (datetime col)",
        },
    ])
