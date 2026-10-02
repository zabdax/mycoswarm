#!/usr/bin/env python3
"""DQN chemotaxis (C09 protocol template): discrete-turn agent navigating a
C06-style pheromone field to a source. State = last NT=4 (c, heading-vs-gradient)
frames; actions = {left, straight, right} by pi/6; reward = scaled dc + capture
bonus - step cost. Run with the isolated torch env:
  C:\\Users\\MIT\\.venvs\\myco-torch\\Scripts\\python.exe dqn_chemotaxis.py [--episodes N]
Saves results_dqn/{model.pt, train.json, eval.json}. Success bar: beat greedy 8.84 min.
"""
import argparse, json, os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycoswarm_abm as sim  # 2-D field/agent geometry for the single-source test
import torch
import torch.nn as nn

GRID, DX = sim.GRID, sim.DX
STEP = sim.V_TIP * sim.DT / DX
CAPTURE_R, T_MAX = sim.CAPTURE_R, 1200.0
NT, NACT = 4, 3
START = np.array([5.0, 55.0])
TARGET = (30, 30)

C, GX, GY = None, None, None

def build_field():
    global C, GX, GY
    C, GX, GY = sim.make_field([TARGET], 200.0)

def sense(p):
    ix, iy = int(np.clip(p[0], 0, GRID - 1)), int(np.clip(p[1], 0, GRID - 1))
    cc = float(C[iy, ix])
    g = np.array([GX[iy, ix], GY[iy, ix]])
    n = float(np.hypot(*g)) + 1e-12
    return cc, g / n

class QNet(nn.Module):
    def __init__(self, din=NT * 5, hidden=64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(din, hidden), nn.ReLU(),
                                 nn.Linear(hidden, hidden), nn.ReLU(),
                                 nn.Linear(hidden, NACT))
    def forward(self, x):
        return self.net(x)

def frame(p, h):
    cc, gh = sense(p)
    gd = np.arctan2(-gh[1], gh[0])
    dh = (gd - h + np.pi) % (2 * np.pi) - np.pi
    return [cc, gh[0], gh[1], np.cos(dh), np.sin(dh)]

def run_episode(net, rng, eps, train=True, buf=None):
    p = START + rng.uniform(-2, 2, 2)
    h = rng.uniform(-np.pi, np.pi)
    hist = [frame(p, h)] * NT
    prev_c = hist[-1][0]
    tot_r, steps = 0.0, 0
    max_steps = 1500
    done = False
    while not done and steps < max_steps:
        s = torch.tensor(np.array(hist).ravel(), dtype=torch.float32)
        if train and rng.random() < eps:
            a = rng.integers(0, NACT)
        else:
            with torch.no_grad():
                a = int(net(s).argmax())
        h = h + (a - 1) * (np.pi / 6)
        p = np.clip(p + np.array([np.cos(h), -np.sin(h)]) * STEP, 0, GRID - 1)
        cc, _ = sense(p)
        r = 100.0 * (cc - prev_c) - 0.001
        prev_c = cc
        steps += 1
        if np.hypot(p[0] * DX - TARGET[0] * DX, p[1] * DX - TARGET[1] * DX) < CAPTURE_R:
            r += 1.0
            done = True
        hist = hist[1:] + [frame(p, h)]
        tot_r += r
        if train and buf is not None:
            buf.append((s.numpy(), a, r,
                        np.array(hist).ravel().astype(np.float32), done))
    return tot_r, steps * sim.DT, done

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=600)
    args = ap.parse_args()
    build_field()
    os.makedirs("results_dqn", exist_ok=True)
    torch.manual_seed(0)
    rng = np.random.default_rng(0)
    net, tgt = QNet(), QNet()
    tgt.load_state_dict(net.state_dict())
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()
    buf, hist_r, hist_t = [], [], []
    gamma = 0.99
    t0 = time.time()
    for ep in range(1, args.episodes + 1):
        eps = max(0.05, 1.0 - 0.95 * ep / (args.episodes * 0.75))
        tot_r, tmin, done = run_episode(net, rng, eps, True, buf)
        hist_r.append(tot_r)
        hist_t.append(tmin)
        # learn every 4 steps worth of transitions
        if len(buf) >= 512:
            for _ in range(4):
                idx = rng.choice(len(buf), 64)
                b = [buf[i] for i in idx]
                s = torch.tensor(np.stack([x[0] for x in b]))
                a = torch.tensor([x[1] for x in b]).unsqueeze(1)
                r = torch.tensor([x[2] for x in b])
                s2 = torch.tensor(np.stack([x[3] for x in b]))
                d = torch.tensor([x[4] for x in b])
                with torch.no_grad():
                    qn = r + gamma * tgt(s2).max(1).values * (~d)
                loss = loss_fn(net(s).gather(1, a).squeeze(), qn)
                opt.zero_grad()
                loss.backward()
                opt.step()
            if ep % 200 == 0:
                tgt.load_state_dict(net.state_dict())
        if ep % 100 == 0:
            print(f"ep {ep}/{args.episodes} eps={eps:.2f} "
                  f"rew={np.mean(hist_r[-100:]):.2f} t={np.mean(hist_t[-100:]):.1f}min", flush=True)
    torch.save(net.state_dict(), "results_dqn/model.pt")
    json.dump({"episodes": args.episodes, "train_reward": [float(x) for x in hist_r],
               "train_time_min": [float(x) for x in hist_t],
               "seconds": time.time() - t0},
              open("results_dqn/train.json", "w"))
    # eval on fixed seeds vs greedy baseline (8.84 min)
    ev = []
    for i in range(10):
        _, tmin, _ = run_episode(net, np.random.default_rng(9000 + i), 0.0, False)
        ev.append(tmin)
    json.dump({"eval_time_min": [float(x) for x in ev],
               "mean": float(np.mean(ev)), "greedy_baseline": 8.84},
              open("results_dqn/eval.json", "w"), indent=2)
    print(f"EVAL mean={np.mean(ev):.2f}min vs greedy 8.84min "
          f"-> {'BEATS' if np.mean(ev) < 8.84 else 'does not beat'} greedy", flush=True)

if __name__ == "__main__":
    main()
