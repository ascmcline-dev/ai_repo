\
"""
CSV Qwen Suite — ComfyUI custom node(s)

Core node:
- CSV Qwen Prompt + Seed Iterator

Security / reliability goals:
- No eval/exec.
- No runtime pip installs.
- Works across queued runs even if ComfyUI re-instantiates nodes (no in-memory counters).
- Avoid "same row/seed forever" by forcing execution and using a file-backed counter if needed.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

try:
    import folder_paths  # ComfyUI helper for standard directories
except Exception:
    folder_paths = None  # type: ignore


# ----------------------------
# Utilities
# ----------------------------

def _norm_path(p: str) -> str:
    p = (p or "").strip()
    if not p:
        return ""
    # Expand ~ and environment variables, normalize separators
    p = os.path.expandvars(os.path.expanduser(p))
    return os.path.abspath(p)


def _to_int32(x: int) -> int:
    # Wrap into signed 32-bit range to match many samplers/seed expectations.
    x = int(x)
    x = x & 0xFFFFFFFF
    if x >= 0x80000000:
        x -= 0x100000000
    return x


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()


def _json_dumps_stable(obj: Any) -> str:
    # Stable JSON for hashing (avoid huge blobs where possible)
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _get_temp_dir() -> str:
    if folder_paths is not None:
        try:
            return folder_paths.get_temp_directory()
        except Exception:
            pass
    return os.path.abspath(os.path.join(os.getcwd(), "temp"))


def _safe_mkdir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


class _FileLock:
    """
    Minimal cross-platform lock using atomic create of a lockfile.

    Not perfect, but good enough for ComfyUI's typical single-queue execution.
    """
    def __init__(self, lock_path: str, timeout_s: float = 3.0, poll_s: float = 0.05):
        self.lock_path = lock_path
        self.timeout_s = timeout_s
        self.poll_s = poll_s
        self._acquired = False

    def acquire(self) -> None:
        deadline = time.time() + self.timeout_s
        while time.time() < deadline:
            try:
                fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                try:
                    os.write(fd, str(os.getpid()).encode("utf-8"))
                finally:
                    os.close(fd)
                self._acquired = True
                return
            except FileExistsError:
                time.sleep(self.poll_s)
        raise TimeoutError(f"Timed out acquiring lock: {self.lock_path}")

    def release(self) -> None:
        if not self._acquired:
            return
        try:
            os.remove(self.lock_path)
        except FileNotFoundError:
            pass
        finally:
            self._acquired = False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.release()
        return False


@dataclass
class CsvData:
    rows: List[Dict[str, Any]]
    columns: List[str]
    positive_col: str
    negative_col: str


def _load_csv_prompts(
    csv_path: str,
    positive_column: str = "",
    negative_column: str = "",
) -> CsvData:
    csv_path = _norm_path(csv_path)
    if not csv_path:
        raise ValueError("csv_path is empty.")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV appears to have no header row (no columns detected).")

        columns = [c for c in reader.fieldnames if c is not None]
        rows = []
        for r in reader:
            if r is None:
                continue
            rows.append(r)

    if len(rows) == 0:
        raise ValueError("CSV has headers but contains zero data rows.")

    def pick_col(user_choice: str, candidates: List[str]) -> str:
        if user_choice and user_choice.strip():
            want = user_choice.strip()
            # exact match (case-sensitive), then case-insensitive
            if want in columns:
                return want
            low_map = {c.lower(): c for c in columns}
            if want.lower() in low_map:
                return low_map[want.lower()]
            raise ValueError(f"Column '{want}' not found. Available: {columns}")

        low_map = {c.lower(): c for c in columns}
        for cand in candidates:
            if cand in low_map:
                return low_map[cand]
        # Heuristic: if exactly 2 columns, assume first=positive second=negative
        if len(columns) == 2:
            return columns[0] if candidates[0].startswith("pos") or "positive" in candidates else columns[1]
        raise ValueError(
            f"Could not auto-detect column. Available columns: {columns}. "
            f"Specify positive_column/negative_column explicitly."
        )

    pos = pick_col(positive_column, ["positive", "pos", "prompt", "text", "caption"])
    neg = pick_col(negative_column, ["negative", "neg", "uncond", "uc"])

    return CsvData(rows=rows, columns=columns, positive_col=pos, negative_col=neg)


# ----------------------------
# Run index resolver (best-effort)
# ----------------------------

def _try_get_int(d: Any, keys: List[str]) -> Optional[int]:
    if not isinstance(d, dict):
        return None
    for k in keys:
        if k in d:
            v = d.get(k)
            if isinstance(v, int):
                return v
            if isinstance(v, str) and v.strip().lstrip("-").isdigit():
                try:
                    return int(v)
                except Exception:
                    pass
    return None


def _resolve_run_index_from_context(prompt: Any, extra_pnginfo: Any) -> Tuple[Optional[int], str]:
    """
    Try to locate a run index / batch index inside Comfy's hidden context.
    Often not available, so we fall back to a file-backed counter.
    """
    keys = ["run_index", "queue_index", "batch_index", "batch_number", "iteration", "i", "index"]
    # Check extra_pnginfo first
    v = _try_get_int(extra_pnginfo, keys)
    if v is not None:
        return v, "extra_pnginfo"

    # Some setups may nest extra fields
    if isinstance(extra_pnginfo, dict):
        for subkey in ["extra", "meta", "info", "execution", "queue"]:
            v = _try_get_int(extra_pnginfo.get(subkey), keys)
            if v is not None:
                return v, f"extra_pnginfo.{subkey}"

    # Check PROMPT
    v = _try_get_int(prompt, keys)
    if v is not None:
        return v, "prompt"

    if isinstance(prompt, dict):
        for subkey in ["workflow", "extra_data", "extra", "meta", "execution", "queue"]:
            v = _try_get_int(prompt.get(subkey), keys)
            if v is not None:
                return v, f"prompt.{subkey}"

    return None, "none"


class _StateCounter:
    """
    File-backed counter keyed by a stable hash of config + node id + csv info.
    This avoids relying on in-memory state which can reset between queued runs.
    """

    def __init__(self, namespace: str = "csv_qwen_suite"):
        temp_dir = _get_temp_dir()
        _safe_mkdir(temp_dir)
        self.state_path = os.path.join(temp_dir, f"{namespace}_state.json")
        self.lock_path = self.state_path + ".lock"

    def _read(self) -> Dict[str, Any]:
        if not os.path.exists(self.state_path):
            return {"version": 1, "counters": {}}
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return {"version": 1, "counters": {}}
            if "counters" not in data or not isinstance(data["counters"], dict):
                data["counters"] = {}
            return data
        except Exception:
            # If corrupt, reset rather than crashing forever.
            return {"version": 1, "counters": {}}

    def _write_atomic(self, data: Dict[str, Any]) -> None:
        tmp = self.state_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.state_path)

    def next(self, key: str) -> int:
        with _FileLock(self.lock_path):
            data = self._read()
            counters: Dict[str, Any] = data.get("counters", {})
            entry = counters.get(key)
            if not isinstance(entry, dict):
                entry = {"value": 0, "updated": time.time()}
            value = int(entry.get("value", 0))
            entry["value"] = value + 1
            entry["updated"] = time.time()
            counters[key] = entry
            data["counters"] = counters
            self._write_atomic(data)
            return value


# One shared counter instance per process (safe; backed by file anyway)
_STATE_COUNTER = _StateCounter()


def _build_state_key(
    unique_id: Any,
    csv_path: str,
    batch_per_row: int,
    base_seed: int,
    row_stride: int,
    take_stride: int,
    positive_column: str,
    negative_column: str,
    wrap: bool,
) -> str:
    csv_path_n = _norm_path(csv_path)
    try:
        stat = os.stat(csv_path_n)
        csv_sig = f"{csv_path_n}|{stat.st_mtime_ns}|{stat.st_size}"
    except Exception:
        csv_sig = csv_path_n

    payload = {
        "unique_id": str(unique_id),
        "csv": csv_sig,
        "batch_per_row": int(batch_per_row),
        "base_seed": int(base_seed),
        "row_stride": int(row_stride),
        "take_stride": int(take_stride),
        "positive_column": (positive_column or "").strip().lower(),
        "negative_column": (negative_column or "").strip().lower(),
        "wrap": bool(wrap),
    }
    return _sha256_text(_json_dumps_stable(payload))


# ----------------------------
# Node implementation
# ----------------------------

class CSVQwenPromptSeedIterator:
    """
    ComfyUI Node: CSV Qwen Prompt + Seed Iterator

    Outputs:
      positive, negative, seed, row_count, row_index, take_index, debug_text
    """

    CATEGORY = "prompt/csv_qwen"
    FUNCTION = "run"

    RETURN_TYPES = ("STRING", "STRING", "INT", "INT", "INT", "INT", "STRING")
    RETURN_NAMES = ("positive", "negative", "seed", "row_count", "row_index", "take_index", "debug_text")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": ""}),
                "batch_per_row": ("INT", {"default": 4, "min": 1, "max": 1000, "step": 1}),
                "base_seed": ("INT", {"default": 1985, "min": -2147483648, "max": 2147483647, "step": 1}),
                "row_stride": ("INT", {"default": 1000, "min": 0, "max": 10_000_000, "step": 1}),
                "take_stride": ("INT", {"default": 1, "min": 0, "max": 1_000_000, "step": 1}),
            },
            "optional": {
                "positive_column": ("STRING", {"default": ""}),
                "negative_column": ("STRING", {"default": ""}),
                "wrap": ("BOOLEAN", {"default": True}),
                "debug": ("BOOLEAN", {"default": False}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Returning NaN forces execution every time (avoids Comfy caching the node output).
        return float("nan")

    def run(
        self,
        csv_path: str,
        batch_per_row: int,
        base_seed: int,
        row_stride: int,
        take_stride: int,
        positive_column: str = "",
        negative_column: str = "",
        wrap: bool = True,
        debug: bool = False,
        prompt: Any = None,
        unique_id: Any = None,
        extra_pnginfo: Any = None,
    ):
        # 1) Load CSV
        csv_data = _load_csv_prompts(
            csv_path=csv_path,
            positive_column=positive_column,
            negative_column=negative_column,
        )
        row_count = len(csv_data.rows)

        # 2) Resolve run index (best effort), else fall back to file-backed counter
        run_index, source = _resolve_run_index_from_context(prompt, extra_pnginfo)

        state_key = ""
        if run_index is None:
            state_key = _build_state_key(
                unique_id=unique_id,
                csv_path=csv_path,
                batch_per_row=batch_per_row,
                base_seed=base_seed,
                row_stride=row_stride,
                take_stride=take_stride,
                positive_column=positive_column,
                negative_column=negative_column,
                wrap=wrap,
            )
            run_index = _STATE_COUNTER.next(state_key)
            source = "file_counter"

        # 3) Map run_index -> row_index/take_index
        total = row_count * int(batch_per_row)
        if total <= 0:
            raise ValueError("Computed total runs per cycle is <= 0 (check CSV and batch_per_row).")

        if wrap:
            idx = int(run_index) % total
        else:
            if int(run_index) >= total:
                raise ValueError(
                    f"Run index {run_index} exceeds CSV capacity ({row_count} rows * {batch_per_row} per row = {total}). "
                    f"Enable wrap=true or queue fewer runs."
                )
            idx = int(run_index)

        row_index = idx // int(batch_per_row)
        take_index = idx % int(batch_per_row)

        # 4) Fetch prompts
        row = csv_data.rows[row_index]
        pos = row.get(csv_data.positive_col, "")
        neg = row.get(csv_data.negative_col, "")

        # Normalize to strings
        positive = "" if pos is None else str(pos)
        negative = "" if neg is None else str(neg)

        # 5) Seed
        seed = int(base_seed) + int(row_index) * int(row_stride) + int(take_index) * int(take_stride)
        seed = _to_int32(seed)

        # 6) Debug
        debug_text = ""
        if debug:
            debug_text = _json_dumps_stable({
                "csv_path": _norm_path(csv_path),
                "columns": csv_data.columns,
                "positive_col": csv_data.positive_col,
                "negative_col": csv_data.negative_col,
                "row_count": row_count,
                "batch_per_row": int(batch_per_row),
                "run_index": int(run_index),
                "run_index_source": source,
                "idx_used": int(idx),
                "row_index": int(row_index),
                "take_index": int(take_index),
                "seed": int(seed),
                "unique_id": str(unique_id),
                "state_key": state_key,
            })

        return (positive, negative, int(seed), int(row_count), int(row_index), int(take_index), debug_text)
