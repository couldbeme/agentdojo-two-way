"""Load AgentDojo released runs (runs/<pipeline>/<suite>/<user_task>/<attack>/<injection_task>.json)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ATTACK = "important_instructions"


def load_runs(runs_dir, pipelines=None, attack: str = ATTACK) -> pd.DataFrame:
    """One row per cell. Keys are suite-qualified because task ids repeat across suites.
    `security` is AgentDojo's flag for "the injection was executed", i.e. attack success.
    Cells whose JSON has no utility/security value are skipped and counted in
    df.attrs["skipped_missing_outcome"]. Cells with a non-null `error` are kept with the
    outcome the runner recorded."""
    runs_dir = Path(runs_dir)
    names = pipelines or sorted(p.name for p in runs_dir.iterdir() if p.is_dir())
    rows = []
    skipped = {}
    for name in names:
        for f in sorted(runs_dir.glob(f"{name}/*/*/{attack}/*.json")):
            d = json.loads(f.read_text())
            if d.get("utility") is None or d.get("security") is None:
                skipped[name] = skipped.get(name, 0) + 1
                continue
            s = d["suite_name"]
            rows.append({
                "pipeline": name,
                "suite": s,
                "user": f"{s}:{d['user_task_id']}",
                "inj": f"{s}:{d['injection_task_id']}",
                "utility": float(d["utility"]),
                "security": float(d["security"]),
                "error": d.get("error"),
            })
    df = pd.DataFrame(rows)
    df.attrs["skipped_missing_outcome"] = skipped
    return df


def paired_cells(df: pd.DataFrame, a: str, b: str, metric: str) -> pd.DataFrame:
    """Cells present in both pipelines with d = y_a - y_b."""
    key = ["suite", "user", "inj"]
    A = df[df.pipeline == a][key + [metric]]
    Bm = df[df.pipeline == b][key + [metric]]
    m = A.merge(Bm, on=key, suffixes=("_a", "_b"), validate="one_to_one")
    m["d"] = m[f"{metric}_a"] - m[f"{metric}_b"]
    return m[key + ["d"]]
