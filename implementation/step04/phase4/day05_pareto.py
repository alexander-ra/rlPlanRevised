"""Aggregate phase-4 results into the §8 Pareto frontier dataset.

Reads the per-day result JSONs and emits two artefacts:

- `phase4/.day05_pareto_table.csv` — one row per configuration with
  columns `(name, info_sets, exploit_gap, emd_proxy, wall_clock_s)`.
- `phase4/.day05_pareto.json`     — same data in JSON for the plot
  driver `day05_plots.py`.

The script tolerates missing day JSONs: if a day didn't run, its rows
are skipped and a warning is printed. This lets the Pareto driver run
incrementally.
"""

import csv
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


def _load(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def collect_rows() -> list:
    rows = []
    leduc_baseline_exploit = None

    day1 = _load(os.path.join(_HERE, ".day01_results.json"))
    if day1:
        # The full engine = the unabstracted baseline (Δ_abs = 0 by
        # definition).
        e_full = day1.get("exploitability_full")
        leduc_baseline_exploit = e_full
        rows.append({
            "name": "day1_full_leduc",
            "info_sets": day1["full_engine"]["info_sets"],
            "exploit": e_full,
            "exploit_gap": 0.0 if e_full is not None else None,
            "emd_proxy": 0.0,
            "wall_clock_s": day1["full_engine"]["wall_clock_s"],
            "notes": "unabstracted Leduc",
        })
        rows.append({
            "name": "day1_rank_canonical",
            "info_sets": day1["rank_engine"]["info_sets"],
            "exploit": day1.get("exploitability_rank"),
            "exploit_gap": (None if e_full is None or
                            day1.get("exploitability_rank") is None
                            else max(0.0,
                                     day1["exploitability_rank"] - e_full)),
            "emd_proxy": 0.0,
            "wall_clock_s": day1["rank_engine"]["wall_clock_s"],
            "notes": "lossless suit-iso (rank engine)",
        })
    else:
        print("warning: .day01_results.json not found, skipping")

    day2 = _load(os.path.join(_HERE, ".day02_results.json"))
    if day2:
        for entry in day2["results"]:
            exploit = entry.get("exploitability")
            if leduc_baseline_exploit is None or exploit is None:
                exploit_gap = None
            else:
                exploit_gap = max(0.0, exploit - leduc_baseline_exploit)
            rows.append({
                "name": f"day2_{entry['config']}",
                "info_sets": entry["info_sets"],
                "exploit": exploit,
                "exploit_gap": exploit_gap,
                "emd_proxy": None,    # filled by emd_evaluator
                "wall_clock_s": entry["wall_clock_s"],
                "notes": (f"k_pre={entry['k_preflop']}, "
                          f"k_post={entry['k_postflop']}, "
                          f"recall={entry['recall']}"),
            })
    else:
        print("warning: .day02_results.json not found, skipping")

    day3 = _load(os.path.join(_HERE, ".day03_results.json"))
    if day3:
        rows.append({
            "name": "day3_mini_nl_full",
            "info_sets": day3["full_info_sets"],
            "exploit": day3["exploit_full"],
            "exploit_gap": 0.0,
            "emd_proxy": 0.0,
            "wall_clock_s": day3["wall_clock_full_s"],
            "notes": "mini-NL full",
        })
        for tname, e in day3["exploit_per_translator"].items():
            rows.append({
                "name": f"day3_translator_{tname}",
                "info_sets": day3["abstract_info_sets"],
                "exploit": e,
                "exploit_gap": e - day3["exploit_full"],
                "emd_proxy": None,
                "wall_clock_s": day3["wall_clock_abstract_s"],
                "notes": f"action-abstracted, translator={tname}",
            })
    else:
        print("warning: .day03_results.json not found, skipping")

    day4 = _load(os.path.join(_HERE, ".day04_results.json"))
    if day4:
        rows.append({
            "name": "day4_extended_unabstracted",
            "info_sets": day4["info_sets_unabstracted"],
            "exploit": None,
            "exploit_gap": None,
            "emd_proxy": 0.0,
            "wall_clock_s": None,
            "notes": "Extended Leduc baseline",
        })
        rows.append({
            "name": "day4_extended_suit_iso",
            "info_sets": day4["info_sets_suit_iso"],
            "exploit": None,
            "exploit_gap": None,
            "emd_proxy": 0.0,
            "wall_clock_s": None,
            "notes": "Extended Leduc + suit isomorphism",
        })
        rows.append({
            "name": "day4_extended_suit_action",
            "info_sets": day4["info_sets_suit_iso_action_abstract"],
            "exploit": None,
            "exploit_gap": None,
            "emd_proxy": None,
            "wall_clock_s": None,
            "notes": "Extended Leduc + suit + action",
        })
        rows.append({
            "name": "day4_extended_triple",
            "info_sets": day4["info_sets_triple_abstract"],
            "exploit": None,
            "exploit_gap": None,
            "emd_proxy": None,
            "wall_clock_s": day4["wall_clock_s"],
            "notes": (f"Extended Leduc + suit + action + bucket "
                      f"k_pre={day4['k_preflop']} "
                      f"k_post={day4['k_postflop']}"),
        })
    else:
        print("warning: .day04_results.json not found, skipping")

    return rows


def write_outputs(rows: list, csv_path: str, json_path: str):
    fieldnames = ["name", "info_sets", "exploit", "exploit_gap",
                  "emd_proxy", "wall_clock_s", "notes"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    with open(json_path, "w") as f:
        json.dump(rows, f, indent=2)


def main():
    rows = collect_rows()
    csv_path = os.path.join(_HERE, ".day05_pareto_table.csv")
    json_path = os.path.join(_HERE, ".day05_pareto.json")
    write_outputs(rows, csv_path, json_path)

    print(f"\nCollected {len(rows)} configurations.")
    print(f"  → {csv_path}")
    print(f"  → {json_path}")
    print()
    print(f"{'Configuration':<35} {'info_sets':>10} {'exploit':>10} "
          f"{'gap':>10}")
    print("-" * 70)
    for r in rows:
        e = "—" if r["exploit"] is None else f"{r['exploit']:.4f}"
        g = "—" if r["exploit_gap"] is None else f"{r['exploit_gap']:.4f}"
        print(f"{r['name']:<35} {r['info_sets']:>10} {e:>10} {g:>10}")


if __name__ == "__main__":
    main()
