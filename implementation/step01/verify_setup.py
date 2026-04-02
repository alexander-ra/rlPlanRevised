"""Verify that all dependencies for Step 01 are installed and working."""

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
    print("Step 01 — Environment Verification\n")
    results = []

    # Python version
    v = sys.version_info
    print(f"Python {v.major}.{v.minor}.{v.micro}")
    results.append(check("Python >= 3.10", lambda: None if v >= (3, 10) else (_ for _ in ()).throw(
        RuntimeError(f"Need 3.10+, got {v.major}.{v.minor}"))))

    # PyTorch
    def test_torch():
        import torch
        x = torch.randn(2, 3)
        _ = x @ x.T  # basic tensor op
        print(f"       torch {torch.__version__} | CUDA: {torch.cuda.is_available()}")
    results.append(check("PyTorch", test_torch))

    # NumPy
    def test_numpy():
        import numpy as np
        _ = np.zeros((3, 3))
        print(f"       numpy {np.__version__}")
    results.append(check("NumPy", test_numpy))

    # Gymnasium + classic_control
    def test_gym_classic():
        import gymnasium as gym
        env = gym.make("CartPole-v1")
        obs, _ = env.reset()
        action = env.action_space.sample()
        obs, reward, term, trunc, info = env.step(action)
        env.close()
        print(f"       gymnasium {gym.__version__} | CartPole-v1 OK")
    results.append(check("Gymnasium (classic_control)", test_gym_classic))

    # Gymnasium + box2d (LunarLander)
    def test_gym_box2d():
        import gymnasium as gym
        env = gym.make("LunarLander-v3")
        obs, _ = env.reset()
        action = env.action_space.sample()
        obs, reward, term, trunc, info = env.step(action)
        env.close()
        print(f"       LunarLander-v3 OK")
    results.append(check("Gymnasium (box2d/LunarLander)", test_gym_box2d))

    # Stable-Baselines3
    def test_sb3():
        import stable_baselines3
        from stable_baselines3 import DQN, PPO
        from stable_baselines3.common.evaluation import evaluate_policy
        print(f"       stable-baselines3 {stable_baselines3.__version__}")
    results.append(check("Stable-Baselines3", test_sb3))

    # TensorBoard
    def test_tb():
        from torch.utils.tensorboard import SummaryWriter
        import tempfile, os
        with tempfile.TemporaryDirectory() as d:
            writer = SummaryWriter(log_dir=d)
            writer.add_scalar("test", 1.0, 0)
            writer.close()
    results.append(check("TensorBoard", test_tb))

    # Matplotlib
    def test_mpl():
        import matplotlib
        matplotlib.use("Agg")  # non-interactive backend
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        plt.close(fig)
        print(f"       matplotlib {matplotlib.__version__}")
    results.append(check("Matplotlib", test_mpl))

    # Quick SB3 smoke test (train 100 steps)
    def test_sb3_train():
        from stable_baselines3 import DQN
        model = DQN("MlpPolicy", "CartPole-v1", verbose=0)
        model.learn(total_timesteps=100)
    results.append(check("SB3 quick train (DQN, 100 steps)", test_sb3_train))

    # Summary
    passed = sum(results)
    total = len(results)
    print(f"\n{'='*40}")
    if passed == total:
        print(f"ALL {total} CHECKS PASSED — ready to implement!")
    else:
        print(f"{passed}/{total} checks passed. Fix failures above before proceeding.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
