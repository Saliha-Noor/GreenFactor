"""
Agent 0 - Environment Detection Agent

Runs ONCE at the start of the whole experiment. Decides measurement_mode
("RAPL" or "TDP") and stores it so every language/pattern/repo run in this
batch uses the SAME mode (mixing real RAPL joules with TDP-estimated
numbers in one comparison table is invalid).
"""
import json
import os
import platform

STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "measurement_mode.json")


def detect_rapl() -> tuple[str | None, str | None]:
    """Return (vendor, energy_file_path). vendor is 'intel', 'amd', or None.
    energy_file_path is the SPECIFIC zone file confirmed readable -- this
    must be persisted and reused as-is, since measurement_agent previously
    hardcoded zone 0 (intel-rapl:0) regardless of which zone this function
    actually confirmed, silently producing None energy readings whenever
    the readable zone wasn't zone 0."""
    intel_path = "/sys/class/powercap/intel-rapl"
    amd_path = "/sys/class/powercap/amd_energy"
    if os.path.isdir(intel_path) and os.listdir(intel_path):
        # confirm we can actually read an energy_uj file (permissions can block this)
        for entry in sorted(os.listdir(intel_path)):
            energy_file = os.path.join(intel_path, entry, "energy_uj")
            if os.path.isfile(energy_file):
                try:
                    with open(energy_file, "r", encoding="utf-8") as f:
                        f.read()
                    return "intel", energy_file
                except PermissionError:
                    continue
    if os.path.isdir(amd_path) and os.listdir(amd_path):
        # AMD energy sysfs exists, but measurement_agent._read_rapl_uj() only
        # implements the Intel path. Return None so AMD falls back to TDP mode
        # until a proper AMD energy-file read path is added.
        return None, None
    return None, None


def run_detection(force_tdp: bool = False) -> dict:
    rapl_vendor, rapl_energy_file = (None, None) if force_tdp else detect_rapl()
    mode = "RAPL" if rapl_vendor else "TDP"
    result = {
        "measurement_mode": mode,
        "rapl_vendor": rapl_vendor,
        "rapl_energy_file": rapl_energy_file,
        "platform": platform.platform(),
        "processor": platform.processor(),
    }
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    return result


def get_mode() -> str:
    """Read the mode already decided for this batch. Raises if detection wasn't run."""
    if not os.path.isfile(STATE_FILE):
        raise RuntimeError(
            "measurement_mode.json not found — run env_detect.run_detection() once "
            "before starting any per-language jobs."
        )
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["measurement_mode"]


def get_rapl_energy_file() -> str | None:
    """Read the specific RAPL zone file confirmed readable during detection.
    Falls back to the legacy zone-0 default if measurement_mode.json predates
    this field (back-compat with older state files)."""
    if not os.path.isfile(STATE_FILE):
        raise RuntimeError(
            "measurement_mode.json not found — run env_detect.run_detection() once "
            "before starting any per-language jobs."
        )
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("rapl_energy_file") or "/sys/class/powercap/intel-rapl:0/energy_uj"


if __name__ == "__main__":
    print(json.dumps(run_detection(), indent=2))
