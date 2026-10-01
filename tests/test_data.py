import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from agentdojo_two_way.data import load_runs, paired_cells
from agentdojo_two_way.estimators import cluster_var, naive_var

RUNS = Path(__file__).resolve().parents[1] / "data" / "upstream" / "runs"
needs_data = pytest.mark.skipif(not RUNS.exists(), reason="raw runs not fetched")


def test_paired_cells_aligns_on_cell_key():
    df = pd.DataFrame({
        "pipeline": ["A", "A", "A", "B", "B", "B"],
        "suite": ["s"] * 6,
        "user": ["s:u1", "s:u1", "s:u2", "s:u2", "s:u1", "s:u1"],
        "inj": ["s:i1", "s:i2", "s:i1", "s:i1", "s:i2", "s:i1"],
        "utility": [1.0, 0.0, 1.0, 0.0, 1.0, 1.0],
        "security": [0.0] * 6,
    })
    p = paired_cells(df, "A", "B", "utility")
    p = p.sort_values(["user", "inj"]).reset_index(drop=True)
    assert list(p["user"]) == ["s:u1", "s:u1", "s:u2"]
    assert list(p["inj"]) == ["s:i1", "s:i2", "s:i1"]
    assert list(p["d"]) == [0.0, -1.0, 1.0]


@needs_data
def test_claude37_reproduces_issue_2605_one_way_numbers():
    df = load_runs(RUNS, pipelines=["claude-3-7-sonnet-20250219"])
    assert len(df) == 949
    assert df["user"].nunique() == 97 and df["inj"].nunique() == 35
    u, s = df["utility"].to_numpy(), df["security"].to_numpy()
    # inspect_evals issue #2605 table (unstratified, grand-mean centred)
    assert np.sqrt(naive_var(u)) == pytest.approx(0.0125, abs=5e-5)
    assert np.sqrt(cluster_var(u, df["user"])) == pytest.approx(0.0334, abs=5e-5)
    assert np.sqrt(naive_var(s)) == pytest.approx(0.0070, abs=5e-5)
    assert np.sqrt(cluster_var(s, df["inj"])) == pytest.approx(0.0177, abs=5e-5)


def test_load_runs_skips_cells_without_outcome(tmp_path):
    base = tmp_path / "P" / "banking" / "user_task_0" / "important_instructions"
    base.mkdir(parents=True)
    common = {"suite_name": "banking", "user_task_id": "user_task_0",
              "attack_type": "important_instructions", "error": None}
    (base / "injection_task_0.json").write_text(json.dumps(
        {**common, "injection_task_id": "injection_task_0", "utility": True, "security": False}))
    (base / "injection_task_1.json").write_text(json.dumps(
        {**common, "injection_task_id": "injection_task_1"}))
    df = load_runs(tmp_path)
    assert len(df) == 1
    assert df.attrs["skipped_missing_outcome"] == {"P": 1}
