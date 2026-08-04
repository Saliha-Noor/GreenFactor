"""
Agent 6 - Energy Measurement Agent

Wraps N repeated run_once() calls from a BuildRunAdapter and attaches an
energy-per-run number, using whichever measurement_mode Agent 0 decided
for this batch (RAPL or TDP-estimate). Same if/else split as the earlier
GreenDev AI project, reused here.
"""
import json
import os
import subprocess
import time
from dataclasses import dataclass, asdict
from typing import Optional

from agents.env_detect import get_mode, get_rapl_energy_file

DEFAULT_TDP_WATTS = float(os.environ.get("ASSUMED_CPU_TDP_WATTS", "15"))  # override per host


@dataclass
class RunMeasurement:
    run_index: int
    elapsed_seconds: float
    exit_code: int
    energy_joules: Optional[float]
    mode: str


def _read_rapl_uj() -> Optional[int]:
    try:
        # Read micro-joule energy value from detected sysfs path
        energy_file = get_rapl_energy_file()
        with open(energy_file, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except (FileNotFoundError, PermissionError, ValueError, RuntimeError):
        return None


def _read_rapl_max_range_uj() -> int:
    """Read the actual sysfs per-zone energy ceiling if available, falling back to 2**32."""
    try:
        energy_file = get_rapl_energy_file()
        if energy_file:
            range_file = os.path.join(os.path.dirname(energy_file), "max_energy_range_uj")
            if os.path.isfile(range_file):
                with open(range_file, "r", encoding="utf-8") as f:
                    return int(f.read().strip())
    except Exception:
        pass
    return 2 ** 32


def _measure_rapl(run_fn) -> tuple:
    before = _read_rapl_uj()
    result = run_fn()
    after = _read_rapl_uj()
    if before is None or after is None:
        return result, None
    delta_uj = after - before
    if delta_uj < 0:
        max_range = _read_rapl_max_range_uj()
        delta_uj += max_range  # counter wraparound ceiling
    return result, delta_uj / 1_000_000.0  # micro-joules -> joules


def _measure_tdp(run_fn) -> tuple:
    """
    TDP-estimation fallback: energy(J) ~= mean_cpu_fraction * TDP_watts * elapsed_seconds.
    Samples system CPU utilization during execution interval to estimate energy consumption.
    """
    import threading

    samples = []
    stop_flag = {"stop": False}

    def _sampler():
        try:
            import psutil
            psutil.cpu_percent(interval=None)  # first call initializes baseline
        except Exception:
            return
        while not stop_flag["stop"]:
            time.sleep(0.05)
            try:
                samples.append(psutil.cpu_percent(interval=None))
            except Exception:
                break

    sampler_thread = threading.Thread(target=_sampler, daemon=True)
    sampler_thread.start()

    start = time.perf_counter()
    result = run_fn()
    elapsed = time.perf_counter() - start

    stop_flag["stop"] = True
    sampler_thread.join(timeout=1.0)

    if samples:
        cpu_frac = max(sum(samples) / len(samples) / 100.0, 0.05)
    else:
        cpu_frac = 0.5  # neutral assumption if psutil isn't installed or no samples captured

    energy_j = cpu_frac * DEFAULT_TDP_WATTS * elapsed
    return result, energy_j


def measure_n_runs(adapter, n: int = 30, idle_baseline_j: float = 0.0) -> list[RunMeasurement]:
    """
    Runs adapter.run_once() n times, measuring energy per the batch-wide mode.
    idle_baseline_j: energy of an equivalent idle period, subtracted per run
    (measure this once per machine before the batch, e.g. sleep for the
    mean run duration and record energy with nothing else running).
    """
    mode = get_mode()
    measurements = []
    for i in range(n):
        if mode == "RAPL":
            result, energy = _measure_rapl(adapter.run_once)
        else:
            result, energy = _measure_tdp(adapter.run_once)
        if energy is not None:
            energy = max(energy - idle_baseline_j, 0.0)
        measurements.append(
            RunMeasurement(
                run_index=i,
                elapsed_seconds=result.elapsed_seconds,
                exit_code=result.exit_code,
                energy_joules=energy,
                mode=mode,
            )
        )
    return measurements


def save_measurements(measurements: list[RunMeasurement], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump([asdict(m) for m in measurements], f, indent=2)
