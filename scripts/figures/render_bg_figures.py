#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/render_bg_figures.py
#
# PURPOSE: Produce Bulgarian versions of the figures without editing the 64
#   plotting scripts, which are research artefacts tied to the reports.
#
#   Each script is executed with a translation layer installed:
#     - matplotlib's labelling methods look every string up in the approved
#       mapping and substitute the Bulgarian
#     - the project's own diagram helpers (box / note / panel_bg in each
#       stepNN/summary/_diagram_utils.py) are wrapped the same way, because the
#       architecture diagrams route all their text through those
#     - tick numbers are formatted with the Bulgarian decimal comma
#     - savefig writes <stem>_bg.png beside the original
#
#   A script that fails is reported and skipped; the English figure stays.
#
# USAGE (run from repo root):
#   python scripts/figures/render_bg_figures.py --list
#   python scripts/figures/render_bg_figures.py --only step06
#   python scripts/figures/render_bg_figures.py
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import importlib
import json
import locale
import os
import runpy
import sys
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
LABELS = REPO_ROOT / "scripts" / "figures" / "out" / "figure_labels.json"

sys.path.insert(0, str(REPO_ROOT / "scripts" / "figures"))
from extract_labels import plotting_scripts  # noqa: E402

BG_LOCALES = ["bg_BG.UTF-8", "bg_BG.utf8", "bg_BG", "Bulgarian_Bulgaria.1251"]


def load_mapping(overlays: list[Path] | None = None) -> dict[str, str]:
    """The approved mapping, with any overlay files applied on top.

    An overlay is a JSON object {english: bulgarian} or a list of {"en", "bg"}
    entries. It lets one chapter's fixes be tried without editing the shared
    figure_labels.json, which every chapter's figures read.
    """
    entries = json.loads(LABELS.read_text(encoding="utf-8"))
    mapping = {e["en"]: e["bg"] for e in entries if e.get("bg")}
    for path in overlays or ():
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(data, list):
            data = {e["en"]: e["bg"] for e in data if e.get("bg")}
        mapping.update(data)
    return mapping


# Bulgarian runs ~15 % longer than English, so a label that fitted its box in
# English often spills over. box() re-wraps it to the box width, and shrinks the
# type only down to this floor - below it the figure is illegible in print, so a
# label that still does not fit is reported and the box has to be enlarged.
FIT_MARGIN = 0.90
MIN_FONT = 9.0
overflow_warnings: list[str] = []


def fit_label(ax, text: str, w: float, h: float, fs: float,
              fontweight=None) -> tuple[str, float]:
    """Wrap `text` (and if needed shrink it, not below MIN_FONT) to fit a w×h box."""
    import textwrap

    fig = ax.figure
    renderer = fig.canvas.get_renderer()
    (x0, y0), (x1, y1) = ax.transData.transform([(0, 0), (w, h)])
    box_w, box_h = abs(x1 - x0) * FIT_MARGIN, abs(y1 - y0) * FIT_MARGIN

    def extent(s: str, size: float) -> tuple[float, float]:
        t = ax.text(0, 0, s, fontsize=size, fontweight=fontweight)
        bb = t.get_window_extent(renderer=renderer)
        t.remove()
        return bb.width, bb.height

    def fits(s: str, size: float) -> bool:
        ew, eh = extent(s, size)
        return ew <= box_w and eh <= box_h

    if fits(text, fs):
        return text, fs
    size = fs
    words = text.replace("\n", " ").split()
    candidate = text
    while True:
        # greedy re-wrap: the widest line count that still fits the width
        for width in range(max(len(text), 1), 3, -1):
            candidate = "\n".join(textwrap.wrap(" ".join(words), width,
                                                break_long_words=False))
            if extent(candidate, size)[0] <= box_w:
                break
        if fits(candidate, size):
            return candidate, size
        if size - 0.5 < min(MIN_FONT, fs):
            overflow_warnings.append(
                f"{text!r} (fs {fs}) does not fit its {w:g}×{h:g} box")
            return candidate, size
        size -= 0.5


def install(mapping: dict[str, str], written: list[Path],
            seen: set[str] | None = None, suffix: str = "_bg") -> None:
    """Patch matplotlib so labels are translated and output is renamed.

    When `seen` is given, every string that reaches a labelling call is recorded
    instead of only being translated. Static parsing cannot find these: several
    diagrams keep their text in a module-level table

        ROWS = [("MCCFR", ...), ("Card / information abstraction", ...)]
        ax.text(-0.9, y, label)          # label is a variable

    so the literal never appears at the call site. Running the script and
    watching what actually arrives is exact and needs no guessing.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    def tr(v):
        if isinstance(v, str):
            if seen is not None and v.strip():
                seen.add(v)
            return mapping.get(v, mapping.get(v.strip(), v))
        if isinstance(v, (list, tuple)):
            return type(v)(tr(x) for x in v)
        return v

    def wrap(owner, name, arg_index=0, kw=None):
        orig = getattr(owner, name, None)
        if orig is None or getattr(orig, "_bg_wrapped", False):
            return

        def patched(*args, **kwargs):
            args = list(args)
            if len(args) > arg_index:
                args[arg_index] = tr(args[arg_index])
            for k in (kw or ()):
                if k in kwargs:
                    kwargs[k] = tr(kwargs[k])
            return orig(*args, **kwargs)

        patched._bg_wrapped = True
        setattr(owner, name, patched)

    # bound methods: index 0 is self, so the text is at index 1
    for meth in ("set_xlabel", "set_ylabel", "set_title", "set_xticklabels",
                 "set_yticklabels", "annotate"):
        wrap(Axes, meth, 1, ("label", "title"))
    wrap(Axes, "text", 3)                    # ax.text(self, x, y, s)
    wrap(Axes, "legend", 1, ("title",))
    wrap(Figure, "suptitle", 1)
    wrap(Figure, "text", 3)
    wrap(Figure, "legend", 1, ("title",))
    for fn in ("xlabel", "ylabel", "title", "suptitle"):
        wrap(plt, fn, 0)
    wrap(plt, "text", 2)
    wrap(plt, "figtext", 2)
    wrap(plt, "legend", 0, ("title",))

    # `label=` is the usual way a legend entry is named
    for meth in ("plot", "bar", "barh", "scatter", "fill_between", "step",
                 "axhline", "axvline", "hist", "errorbar", "stackplot"):
        wrap(Axes, meth, 999, ("label",))

    # Bulgarian decimal comma on tick numbers
    for loc in BG_LOCALES:
        try:
            locale.setlocale(locale.LC_NUMERIC, loc)
            matplotlib.rcParams["axes.formatter.use_locale"] = True
            break
        except locale.Error:
            continue

    # savefig -> <stem>_bg.png, resolved the way the script expects
    def bg_path(fname):
        p = Path(str(fname))
        if not p.is_absolute():
            cwd = Path.cwd()
            first = p.parts[0] if p.parts else ""
            # Some scripts write repo-root-relative paths ("deliverables/...").
            # Running them from their own directory would nest a whole copy of
            # the tree underneath, e.g. step07/summary/deliverables/reports/...
            if first in {"deliverables", "implementation", "scripts", "docs"}:
                p = REPO_ROOT / p
            # Others assume the working directory is their parent, so a leading
            # component repeats the directory we are already in.
            elif first and cwd.name == first:
                p = cwd.parent / p
            else:
                p = cwd / p
        p = p.resolve()
        if p.stem.endswith(suffix):
            return p
        return p.with_name(f"{p.stem}{suffix}{p.suffix or '.png'}")

    orig_save = Figure.savefig

    def savefig(self, fname, *a, **kw):
        if isinstance(fname, (str, os.PathLike)):
            out = bg_path(fname)
            out.parent.mkdir(parents=True, exist_ok=True)
            written.append(out)
            return orig_save(self, str(out), *a, **kw)
        return orig_save(self, fname, *a, **kw)

    Figure.savefig = savefig
    plt.savefig = lambda *a, **kw: savefig(plt.gcf(), *a, **kw)


def patch_diagram_utils(script: Path, mapping: dict[str, str],
                        seen: set[str] | None = None) -> None:
    """Wrap the project's own text helpers for this script's step.

    The diagrams call box(ax, x, y, w, h, label) and note(ax, x, y, text)
    rather than matplotlib, so patching matplotlib alone leaves them English.
    Each step keeps its own copy of _diagram_utils, so this runs per script.
    """
    utils = script.parent / "_diagram_utils.py"
    if not utils.exists():
        return
    sys.path.insert(0, str(script.parent))
    for stale in [m for m in sys.modules if m == "_diagram_utils"]:
        del sys.modules[stale]
    mod = importlib.import_module("_diagram_utils")

    def tr(v):
        if not isinstance(v, str):
            return v
        if seen is not None and v.strip():
            seen.add(v)
        return mapping.get(v, mapping.get(v.strip(), v))

    def wrap(name, idx, kw=None):
        orig = getattr(mod, name, None)
        if orig is None or getattr(orig, "_bg_wrapped", False):
            return

        def patched(*args, **kwargs):
            args = list(args)
            if len(args) > idx:
                args[idx] = tr(args[idx])
            for k in (kw or ()):
                if k in kwargs:
                    kwargs[k] = tr(kwargs[k])
            return orig(*args, **kwargs)

        patched._bg_wrapped = True
        setattr(mod, name, patched)

    # box(ax, x, y, w, h, label, fc=..., fs=..., ...): translate, then fit
    orig_box = getattr(mod, "box", None)
    if orig_box is not None and not getattr(orig_box, "_bg_wrapped", False):
        import inspect
        default_fs = inspect.signature(orig_box).parameters.get("fs")
        default_fs = default_fs.default if default_fs is not None else 9.0

        def box(*args, **kwargs):
            args = list(args)
            if len(args) > 5:
                args[5] = tr(args[5])
            elif "label" in kwargs:
                kwargs["label"] = tr(kwargs["label"])
            ax, w, h = args[0], args[3], args[4]
            label = args[5] if len(args) > 5 else kwargs.get("label")
            fs = kwargs.get("fs", args[7] if len(args) > 7 else default_fs)
            if isinstance(label, str) and label.strip() and "$" not in label:
                new, size = fit_label(ax, label, w, h, fs,
                                      kwargs.get("fontweight"))
                if len(args) > 5:
                    args[5] = new
                else:
                    kwargs["label"] = new
                if len(args) > 7:
                    args[7] = size
                else:
                    kwargs["fs"] = size
            return orig_box(*args, **kwargs)

        box._bg_wrapped = True
        mod.box = box
    wrap("panel_bg", 6, ("label",))
    wrap("note", 3, ("text",))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="substring filter on the script path")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--collect", metavar="FILE",
                    help="record every string that reaches a labelling call "
                         "and write it here, instead of only translating")
    ap.add_argument("--labels-overlay", metavar="FILE", action="append",
                    type=Path, default=[],
                    help="JSON {en: bg} applied on top of figure_labels.json "
                         "(repeatable); for trying one chapter's label fixes")
    args = ap.parse_args()

    scripts = plotting_scripts()
    if args.only:
        scripts = [s for s in scripts
                   if args.only in s.relative_to(REPO_ROOT).as_posix()]
    if args.list:
        for s in scripts:
            print("  ", s.relative_to(REPO_ROOT).as_posix())
        print(f"{len(scripts)} scripts")
        return

    mapping = load_mapping(args.labels_overlay)
    print(f"{len(mapping)} approved label translations"
          + (f" (with {len(args.labels_overlay)} overlay(s))"
             if args.labels_overlay else ""))

    seen: set[str] | None = set() if args.collect else None
    if seen is not None:
        # Collect with translation OFF. The diagram helpers call matplotlib
        # internally, so both wrappers fire on one label: with translation on,
        # the inner wrapper records the Bulgarian the outer one just produced
        # and it comes back as a new "English" string to translate.
        mapping = {}
        print("  collect mode: translation disabled while recording")
    ok = failed = 0
    all_written: list[Path] = []
    failures: list[tuple[str, str]] = []

    for script in scripts:
        rel = script.relative_to(REPO_ROOT).as_posix()
        written: list[Path] = []
        cwd = os.getcwd()
        saved_modules = set(sys.modules)
        added_paths: list[str] = []
        try:
            install(mapping, written, seen)
            patch_diagram_utils(script, mapping, seen)
            # These scripts are normally launched from their step root, so an
            # exploration/ script imports a sibling package like `cfr` or
            # `kuhn_tools`. Running from the script's own directory breaks that,
            # so every ancestor up to the step root goes on the path while the
            # working directory stays put for relative output paths.
            for anc in [script.parent, *script.parents[1:4]]:
                if anc.is_dir() and str(anc) not in sys.path:
                    sys.path.insert(0, str(anc))
                    added_paths.append(str(anc))
            os.chdir(script.parent)
            # The script must see its own argv, not ours: a plotting script
            # with argparse would otherwise reject "--only stepNN" and exit
            # before drawing anything.
            saved_argv, sys.argv = sys.argv, [str(script)]
            try:
                runpy.run_path(str(script), run_name="__main__")
            finally:
                sys.argv = saved_argv
            ok += 1
            all_written += written
            print(f"  ok    {rel}  ({len(written)} figure(s))", flush=True)
        except SystemExit:
            ok += 1
            all_written += written
            print(f"  ok    {rel}  ({len(written)} figure(s), exited)", flush=True)
        except Exception as exc:                      # noqa: BLE001
            failed += 1
            failures.append((rel, f"{type(exc).__name__}: {exc}"))
            print(f"  FAIL  {rel}  {type(exc).__name__}: {exc}", flush=True)
        finally:
            os.chdir(cwd)
            import matplotlib.pyplot as plt
            plt.close("all")
            # Drop only modules loaded from inside this repo, so the next
            # script picks up its own _diagram_utils. Purging everything new
            # also evicts numpy's C extensions, which cannot be re-imported
            # in the same process.
            for name in set(sys.modules) - saved_modules:
                mod = sys.modules.get(name)
                path = getattr(mod, "__file__", None)
                if not path:
                    continue
                resolved = Path(path).resolve()
                # .venv sits inside the repo, so "under REPO_ROOT" alone still
                # matches numpy and evicts its C extensions.
                if "site-packages" in resolved.parts or ".venv" in resolved.parts:
                    continue
                if resolved.is_relative_to(REPO_ROOT):
                    sys.modules.pop(name, None)
            for p in added_paths:
                if p in sys.path:
                    sys.path.remove(p)

    if seen is not None:
        known = set(mapping) | {k.strip() for k in mapping}
        new = sorted(s for s in seen if s not in known and s.strip() not in known)
        Path(args.collect).write_text(
            json.dumps(sorted(seen), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        print(f"\nstrings observed at runtime : {len(seen)}")
        print(f"  not yet translated         : {len(new)}")
        for s in new[:12]:
            print(f"     {s[:72]!r}")
        print(f"written to {args.collect}")

    print(f"\nscripts ok {ok}, failed {failed}")
    print(f"BG figures written: {len(all_written)}")
    if overflow_warnings:
        print(f"\nlabels that still overflow their box at fs {MIN_FONT} "
              "(enlarge the box in the script):")
        for w in overflow_warnings:
            print(f"   {w[:140]}")
    if failures:
        print("\nfailures (their English figures stay in place):")
        for rel, why in failures:
            print(f"   {rel}\n      {why[:130]}")


if __name__ == "__main__":
    main()
