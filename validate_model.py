from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor


DATA_PATH = Path(__file__).parent / "data" / "co2_clean_1000.csv"
FEATURES = ("population", "gdp", "energy_per_capita", "methane")
TARGET = "co2"
RANDOM_STATE = 42


def load_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    features: list[list[float]] = []
    targets: list[float] = []
    countries: list[str] = []

    with DATA_PATH.open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            try:
                values = [float(row[name]) for name in FEATURES]
                target = float(row[TARGET])
            except (KeyError, TypeError, ValueError):
                continue
            if not np.isfinite(values).all() or not np.isfinite(target):
                continue
            features.append(values)
            targets.append(target)
            countries.append(row["country"])

    if len(set(countries)) < 6:
        raise ValueError("At least six countries are required for grouped validation.")
    return np.asarray(features), np.asarray(targets), np.asarray(countries)


def split_by_country(groups: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    all_indices = np.arange(len(groups))
    outer = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=RANDOM_STATE)
    development, test = next(outer.split(all_indices, groups=groups))

    inner = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=RANDOM_STATE)
    train_local, validation_local = next(inner.split(development, groups=groups[development]))
    return development[train_local], development[validation_local], test


def candidates() -> dict[str, object]:
    return {
        "linear": Pipeline([
            ("scale", StandardScaler()),
            ("model", LinearRegression()),
        ]),
        **{
            f"tree-depth-{depth}": DecisionTreeRegressor(
                max_depth=depth,
                min_samples_leaf=10,
                random_state=RANDOM_STATE,
            )
            for depth in (2, 4, 6)
        },
    }


def metrics(expected: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    return {
        "MAE": mean_absolute_error(expected, predicted),
        "RMSE": mean_squared_error(expected, predicted) ** 0.5,
        "R2": r2_score(expected, predicted),
    }


def main() -> None:
    x, y, countries = load_data()
    train, validation, test = split_by_country(countries)
    models = candidates()

    validation_scores: dict[str, float] = {}
    for name, model in models.items():
        model.fit(x[train], y[train])
        score = mean_absolute_error(y[validation], model.predict(x[validation]))
        validation_scores[name] = score
        print(f"validation {name:>12}: MAE={score:.3f}")

    selected_name = min(validation_scores, key=validation_scores.get)
    selected = models[selected_name]
    development = np.concatenate((train, validation))
    selected.fit(x[development], y[development])
    final_metrics = metrics(y[test], selected.predict(x[test]))

    print(f"\nselected model: {selected_name}")
    print(f"held-out countries: {', '.join(sorted(set(countries[test])))}")
    for name, value in final_metrics.items():
        print(f"test {name}: {value:.3f}")


if __name__ == "__main__":
    main()
