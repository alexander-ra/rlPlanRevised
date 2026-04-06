"""Verify that all dependencies for Step 02 are installed and working."""

import sys

def check(name, test_fn):
    try:
        test_fn()
        print(f"  ✓ {name}")
        return True
    except Exception as e:
        print(f"  ✗ {name}: {e}")
        return False

def main():
    print("Step 02 — Environment Verification\n")
    results = []

    # Python version
    v = sys.version_info
    print(f"Python {v.major}.{v.minor}.{v.micro}")
    results.append(check("Python >= 3.10", lambda: None if v >= (3, 10) else (_ for _ in ()).throw(
        RuntimeError(f"Need 3.10+, got {v.major}.{v.minor}"))))

    # NumPy
    def test_numpy():
        import numpy as np
        _ = np.zeros((3, 3))
        print(f"       numpy {np.__version__}")
    results.append(check("NumPy", test_numpy))

    # Matplotlib
    def test_mpl():
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        plt.close(fig)
        print(f"       matplotlib {matplotlib.__version__}")
    results.append(check("Matplotlib", test_mpl))

    # OpenSpiel (optional)
    def test_openspiel():
        import pyspiel
        game = pyspiel.load_game("kuhn_poker")
        state = game.new_initial_state()
        print(f"       open_spiel OK | kuhn_poker loaded")
    ok = check("OpenSpiel (optional)", test_openspiel)
    if not ok:
        print("       ↳ OpenSpiel is optional — compare_openspiel.py will be unavailable")
    results.append(True)  # always pass — OpenSpiel is optional

    # Quick CFR smoke test
    def test_cfr_import():
        sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
        from cfr.cfr_trainer import KuhnTrainer
        trainer = KuhnTrainer()
        val = trainer.train(100)
        assert abs(val - (-1/18)) < 0.1, f"Game value {val} too far from -1/18"
    results.append(check("CFR smoke test (100 iterations)", test_cfr_import))

    # Summary
    passed = sum(results)
    total = len(results)
    print(f"\n{'='*40}")
    if passed == total:
        print(f"ALL {total} CHECKS PASSED — ready to run!")
    else:
        print(f"{passed}/{total} checks passed. Fix failures above before proceeding.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
