import json
import subprocess
import sys
from pathlib import Path

import pytest

from inferrsi.skill_catalog import get_skill, skill_instructions, skill_records

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "src/inferrsi/data/skill_library"
SKILL_NAME = "ascend-video-diffusion-optimization"
SKILL = SKILL_ROOT / "hardware/ascend" / SKILL_NAME
TEMPLATE = SKILL / "assets/campaign.template.json"
EVALUATOR = SKILL / "scripts/evaluate_target.py"


def test_skill_is_discoverable_and_resources_resolve():
    discovered = {record["name"] for record in skill_records(SKILL_ROOT)}
    assert SKILL_NAME in discovered

    record = get_skill(SKILL_ROOT, SKILL_NAME)

    assert record["name"] == SKILL_NAME
    assert record["status"] == "candidate"
    assert {"ascend", "video-diffusion", "performance"} <= set(record["tags"])
    assert set(record["resources"]) == {
        "assets/campaign.template.json",
        "metadata.json",
        "references/field-notes-video-diffusion.md",
        "scripts/evaluate_target.py",
    }

    description = record["description"]
    assert all(term in description for term in ("latency", "RTF", "throughput", "HBM"))
    assert "Not for text-only LLMs" in description

    instructions = skill_instructions(SKILL_ROOT, SKILL_NAME)
    for relative in (
        "assets/campaign.template.json",
        "references/field-notes-video-diffusion.md",
        "scripts/evaluate_target.py",
    ):
        assert relative in instructions
        assert (SKILL / relative).is_file()
    for relative in (
        "methods/inference-benchmark-design/SKILL.md",
        "workflows/rsi-evidence/SKILL.md",
    ):
        assert relative in instructions
        assert (SKILL_ROOT / relative).is_file()


def campaign(case):
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    if case == "fail":
        data["quality_gates"][0]["value"] = 0.90
    elif case == "inconclusive":
        data["primary_metric"]["candidate"] = [2.0, 3.0, 4.0]
    elif case == "invalid":
        data["primary_metric"]["baseline"] = [4.0, 4.01]
    return data


@pytest.mark.parametrize(
    ("case", "exit_code", "verdict"),
    [
        ("pass", 0, "PASS"),
        ("fail", 1, "FAIL"),
        ("invalid", 2, "INVALID"),
        ("inconclusive", 3, "INCONCLUSIVE"),
    ],
)
def test_evaluator_verdict_and_exit_code(tmp_path, case, exit_code, verdict):
    path = tmp_path / f"{case}.json"
    path.write_text(json.dumps(campaign(case)), encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(EVALUATOR), str(path)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == exit_code
    result = json.loads(completed.stdout)
    assert result["verdict"] == verdict
    assert completed.stderr == ""
    if verdict != "INVALID":
        assert "Local pre-check only" in result["scope_note"]
