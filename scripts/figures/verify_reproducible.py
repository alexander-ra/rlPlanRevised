#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/verify_reproducible.py
#
# PURPOSE: Decide which Bulgarian figures are safe to keep.
#
#   Re-rendering a plot re-runs its script, and a script that reads saved run
#   logs will draw whatever is on disk *today*. step01's dqn_comparison came
#   back with 50 episodes instead of 1,061 and no Custom DQN curve at all - a
#   figure that flatly contradicts the report text beside it.
#
#   So each script is first re-rendered in ENGLISH and compared against its
#   committed English figure. Only if the script reproduces its own output is
#   the Bulgarian version trustworthy; otherwise the _bg file is removed and
#   the document keeps pointing at the English original.
#
#   Comparison is on image content, not bytes: PNG encoders are not
#   deterministic across runs, so identical plots can differ byte for byte.
#
# USAGE (run from repo root):
#   python scripts/figures/verify_reproducible.py --dry-run
#   python scripts/figures/verify_reproducible.py
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import os
import runpy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT / "scripts" / "figures"))
from extract_labels import plotting_scripts          # noqa: E402
from render_bg_figures import install, patch_diagram_utils  # noqa: E402

CHECK_SUFFIX = "_reprocheck"
# Fraction of pixels allowed to differ. Measured on this corpus the two causes
# separate cleanly: hardcoded diagrams reproduce at 0.00% and renderer noise
# tops out at 2.3%, while a genuinely changed dataset moves 11-30% of pixels.
# 4% sits in that gap with margin on both sides.
TOLERANCE = 0.04


def images_match(a: Path, b: Path) -> tuple[bool, float]:
    """Compare two renders, tolerant of the renderer but not of the data.

    A size difference of a few pixels is normal: bbox_inches="tight" plus font
    metrics that shifted between the matplotlib that produced the committed PNG
    and the one running now. Treating any size mismatch as total failure called
    hardcoded diagrams "100% different" when they differed by one pixel.

    So the images are scaled to a common size and compared with a per-channel
    threshold, which absorbs anti-aliasing while leaving a changed dataset -
    different curves, different axis range - plainly visible.
    """
    from PIL import Image, ImageChops

    with Image.open(a) as ia, Image.open(b) as ib:
        ra, rb = ia.convert("RGB"), ib.convert("RGB")
        # wildly different proportions mean the layout really did change
        ar, br = ra.size[0] / ra.size[1], rb.size[0] / rb.size[1]
        if abs(ar - br) / max(ar, br) > 0.05:
            return False, 1.0
        if ra.size != rb.size:
            rb = rb.resize(ra.size, Image.BILINEAR)
        diff = ImageChops.difference(ra, rb)
        if diff.getbbox() is None:
            return True, 0.0
        # ignore small per-channel differences (anti-aliasing, hinting)
        mono = diff.convert("L").point(lambda v: 255 if v > 48 else 0)
        differing = sum(mono.point(lambda v: 1 if v else 0)
                        .getdata())
        frac = differing / (ra.size[0] * ra.size[1])
        return frac <= TOLERANCE, frac


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()

    scripts = plotting_scripts()
    if args.only:
        scripts = [s for s in scripts
                   if args.only in s.relative_to(REPO_ROOT).as_posix()]

    reproducible: list[Path] = []
    drifted: list[tuple[Path, float]] = []
    unchecked: list[Path] = []

    for script in scripts:
        rel = script.relative_to(REPO_ROOT).as_posix()
        written: list[Path] = []
        cwd = os.getcwd()
        added: list[str] = []
        saved = set(sys.modules)
        try:
            install({}, written, None, suffix=CHECK_SUFFIX)
            patch_diagram_utils(script, {}, None)
            for anc in [script.parent, *script.parents[1:4]]:
                if anc.is_dir() and str(anc) not in sys.path:
                    sys.path.insert(0, str(anc))
                    added.append(str(anc))
            os.chdir(script.parent)
            runpy.run_path(str(script), run_name="__main__")
        except SystemExit:
            pass
        except Exception as exc:                       # noqa: BLE001
            print(f"  skip  {rel}: {type(exc).__name__}", flush=True)
        finally:
            os.chdir(cwd)
            import matplotlib.pyplot as plt
            plt.close("all")
            for name in set(sys.modules) - saved:
                mod = sys.modules.get(name)
                path = getattr(mod, "__file__", None)
                if not path:
                    continue
                r = Path(path).resolve()
                if "site-packages" in r.parts or ".venv" in r.parts:
                    continue
                if r.is_relative_to(REPO_ROOT):
                    sys.modules.pop(name, None)
            for p in added:
                if p in sys.path:
                    sys.path.remove(p)

        for probe in written:
            original = probe.with_name(
                probe.name.replace(CHECK_SUFFIX, ""))
            bg = probe.with_name(probe.name.replace(CHECK_SUFFIX, "_bg"))
            if not original.exists():
                unchecked.append(probe)
            else:
                same, frac = images_match(probe, original)
                if same:
                    reproducible.append(original)
                else:
                    drifted.append((original, frac))
                    # Remove EVERY copy, not just the one beside the script.
                    # sync_figures.py mirrors each variant into the report's
                    # figures/ and its summary/, so deleting only the source
                    # leaves the drifted figure in the deliverables, still
                    # referenced - which is the exact failure this gate exists
                    # to prevent.
                    if not args.dry_run:
                        for stale in REPO_ROOT.rglob(bg.name):
                            if ".venv" not in stale.parts:
                                stale.unlink(missing_ok=True)
            if not args.dry_run:
                probe.unlink(missing_ok=True)

    print(f"\nreproduces its committed figure : {len(reproducible)}")
    print(f"DRIFTED - BG version discarded   : {len(drifted)}")
    print(f"no committed original to compare : {len(unchecked)}")
    for p, frac in sorted(drifted, key=lambda t: -t[1])[:20]:
        print(f"   {frac*100:5.1f}% of pixels differ   {p.name}")


if __name__ == "__main__":
    main()
