"""
Agent 7 - Statistics Agent

Compares baseline vs refactored energy measurements (paired, same repo/pattern,
same n runs) for one (language, pattern, repo) cell. Reports:
  - Shapiro-Wilk normality check (decides t-test vs Wilcoxon)
  - paired t-test OR Wilcoxon signed-rank (whichever is valid)
  - Cohen's d (paired) as effect size
  - 95% CI on the mean difference
"""
import statistics
from dataclasses import dataclass, asdict

from scipy import stats


@dataclass
class ComparisonResult:
    n: int
    mean_baseline_j: float
    mean_refactored_j: float
    percent_change: float
    test_used: str
    p_value: float
    cohens_d: float
    ci_95_low: float
    ci_95_high: float
    significant: bool


def compare_before_after(baseline_j: list[float], refactored_j: list[float], alpha: float = 0.05) -> ComparisonResult:
    if len(baseline_j) != len(refactored_j):
        raise ValueError("baseline and refactored measurement lists must be the same length (paired runs)")
    n = len(baseline_j)
    if n < 3:
        raise ValueError("need at least 3 paired runs for a meaningful test")

    diffs = [b - r for b, r in zip(baseline_j, refactored_j)]  # positive = refactor saved energy
    mean_diff = statistics.mean(diffs)
    sd_diff = statistics.stdev(diffs)

    # normality check on the differences decides which test is valid
    try:
        _, p_norm = stats.shapiro(diffs)
        normal_enough = p_norm > 0.05
    except Exception:
        normal_enough = False

    if normal_enough:
        t_stat, p_value = stats.ttest_rel(baseline_j, refactored_j)
        test_used = "paired t-test"
    else:
        try:
            w_stat, p_value = stats.wilcoxon(baseline_j, refactored_j)
        except ValueError:
            # all diffs identical -> wilcoxon undefined, treat as non-significant
            p_value = 1.0
        test_used = "Wilcoxon signed-rank"

    cohens_d = mean_diff / sd_diff if sd_diff > 0 else 0.0

    se = sd_diff / (n ** 0.5)
    t_crit = stats.t.ppf(0.975, df=n - 1)
    ci_low = mean_diff - t_crit * se
    ci_high = mean_diff + t_crit * se

    mean_b = statistics.mean(baseline_j)
    mean_r = statistics.mean(refactored_j)
    pct_change = ((mean_r - mean_b) / mean_b * 100) if mean_b else 0.0

    return ComparisonResult(
        n=n, mean_baseline_j=float(mean_b), mean_refactored_j=float(mean_r), percent_change=float(pct_change),
        test_used=test_used, p_value=float(p_value), cohens_d=float(cohens_d),
        ci_95_low=float(ci_low), ci_95_high=float(ci_high), significant=bool(p_value < alpha),
    )
