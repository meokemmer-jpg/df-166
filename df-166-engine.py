"""DF-166 LexVance audit hours tracker engine."""

import re
import os
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime, timezone


DF_DIR = Path(__file__).parent
LOCK_DIR = Path("/tmp/df-166.lock")
DF_ID = "166"
DECISION_KEYWORDS_REGEX = re.compile(
    r"\b(entscheid[a-z]*|empfehl(?:e|en|t|st)|sollt(?:e|en|est)|recommend[a-z]*|decid[a-z]*|advis[a-z]*|propos[a-z]*)\b",
    re.IGNORECASE,
)


@dataclass
class TrackerOutput:
    welle: str = "25"
    df: str = "DF-166"
    iso_timestamp: str = ""
    source: str = "mock"
    audits_open: int = 0
    hours_billed_month: float = 0
    hours_per_audit_avg: float = 0
    top_audit_clients: list = field(default_factory=list)
    deadline_breaches: int = 0


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _file_stable(path, min_age_sec=300) -> bool:
    p = Path(path)
    if not p.exists() or not p.is_file():
        return False
    try:
        age = time.time() - p.stat().st_mtime
    except OSError:
        return False
    return age >= min_age_sec


def acquire_lock_with_identity() -> bool:
    stale_after_sec = 6 * 60 * 60

    try:
        LOCK_DIR.mkdir(mode=0o700)
    except FileExistsError:
        try:
            age = time.time() - LOCK_DIR.stat().st_mtime
            if age > stale_after_sec:
                for child in LOCK_DIR.iterdir():
                    if child.is_file() or child.is_symlink():
                        child.unlink()
                LOCK_DIR.rmdir()
                LOCK_DIR.mkdir(mode=0o700)
            else:
                return False
        except OSError:
            return False

    identity = {
        "df": f"DF-{DF_ID}",
        "pid": os.getpid(),
        "created_at": iso_now(),
        "cwd": os.getcwd(),
    }
    try:
        (LOCK_DIR / "identity.json").write_text(
            json.dumps(identity, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        release_lock()
        return False

    return True


def release_lock() -> None:
    try:
        for child in LOCK_DIR.iterdir():
            if child.is_file() or child.is_symlink():
                child.unlink()
        LOCK_DIR.rmdir()
    except FileNotFoundError:
        return
    except OSError:
        return


def k17_pre_action_verification(anchors) -> dict:
    missing = []
    env_tag = "real" if _is_real_api_enabled() else "mock"

    for anchor in anchors or []:
        token = str(anchor).strip()
        if not token:
            continue
        if token.startswith("env:"):
            name = token[4:]
            if not os.getenv(name):
                missing.append(token)
        else:
            path = Path(token)
            if not path.is_absolute():
                path = DF_DIR / path
            if not _file_stable(path, min_age_sec=0):
                missing.append(token)

    return {
        "ok": len(missing) == 0,
        "missing_anchors": missing,
        "env_tag": env_tag,
    }


def _is_real_api_enabled() -> bool:
    value = os.getenv("DF_166_REAL_API_ENABLED", "false").strip().lower()
    return value in {"1", "true", "yes", "y", "on"}


def scan_output_for_decision_keywords(text) -> list:
    if text is None:
        return []
    return sorted({match.group(0) for match in DECISION_KEYWORDS_REGEX.finditer(str(text))})


def assert_no_decision_keywords(output) -> None:
    hits = scan_output_for_decision_keywords(output)
    if hits:
        raise ValueError("Q_0/K_0 keyword block triggered: " + ", ".join(hits))


def _float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _list_env(name: str, default: list) -> list:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return list(default)
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in raw.split(",") if item.strip()]


def collect_tracker_output() -> TrackerOutput:
    real_enabled = _is_real_api_enabled()

    if real_enabled:
        audits_open = _int_env("DF_166_AUDITS_OPEN", 0)
        hours_billed_month = _float_env("DF_166_HOURS_BILLED_MONTH", 0.0)
        hours_per_audit_avg = _float_env("DF_166_HOURS_PER_AUDIT_AVG", 0.0)
        top_audit_clients = _list_env("DF_166_TOP_AUDIT_CLIENTS", [])
        deadline_breaches = _int_env("DF_166_DEADLINE_BREACHES", 0)
        source = "real"
    else:
        audits_open = 14
        hours_billed_month = 428.5
        hours_per_audit_avg = 30.61
        top_audit_clients = ["Meyer & Co", "NordTax GmbH", "Rhein Ledger AG"]
        deadline_breaches = 1
        source = "mock"

    return TrackerOutput(
        iso_timestamp=iso_now(),
        source=source,
        audits_open=audits_open,
        hours_billed_month=round(float(hours_billed_month), 2),
        hours_per_audit_avg=round(float(hours_per_audit_avg), 2),
        top_audit_clients=top_audit_clients,
        deadline_breaches=deadline_breaches,
    )


def _load_anchors() -> list:
    raw = os.getenv("DF_166_K17_ANCHORS", "").strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in raw.split(",") if item.strip()]


def main() -> int:
    if not acquire_lock_with_identity():
        return 3

    try:
        pav = k17_pre_action_verification(_load_anchors())
        if not pav.get("ok"):
            payload = {
                "df": "DF-166",
                "iso_timestamp": iso_now(),
                "source": pav.get("env_tag", "mock"),
                "error": "k17_pre_action_verification_failed",
                "missing_anchors": pav.get("missing_anchors", []),
            }
            text = json.dumps(payload, ensure_ascii=False, indent=2)
            assert_no_decision_keywords(text)
            return 3

        output = collect_tracker_output()
        payload = asdict(output)
        payload["k17_pre_action_verification"] = pav

        report_text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        assert_no_decision_keywords(report_text)

        report_dir = DF_DIR / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        date_part = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        report_path = report_dir / f"df-166-{date_part}.json"
        report_path.write_text(report_text + "\n", encoding="utf-8")
        return 0
    except Exception as exc:
        sys.stderr.write(f"DF-166 failed: {exc}\n")
        return 3
    finally:
        release_lock()


if __name__ == "__main__":
    sys.exit(main())