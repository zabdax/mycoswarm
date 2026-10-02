#!/usr/bin/env python3
"""3-D multi-source DQN: single tip, 4 depleting sources, unit-vector headings.
State = NT=4 frames of [c, ghat(3), align]; 7 tilt actions; reward = scaled dc
+ capture bonus + completion bonus. Greedy-3D baseline included.
Run with isolated torch env. Saves results_dqn3d/. Success: beat greedy mean.
"""
import argparse, json, os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycoswarm_abm_3d as sim
import torch
import torch.nn as nn

GRID, DX = sim.GRID, sim.DX
STEP = sim.V_TIP * sim.DT / DX
CAPTURE_R = sim.CAPTURE_R
SOURCES = [(10, 10, 10), (30, 12, 28), (20, 30, 15), (32, 30, 32)]
NT, NACT, TILT = 4, 7, 0.35
MAX_STEPS = 6000
EYE = np.eye(3)

C, GX, GY, GZ = None, None, None, None

def rebuild(live):
    global C, GX, GY, GZ
    C, GX, GY, GZ = sim.make_field(live if live else SOURCES, 200.0)

def sense(p):
    i = np.clip(p.astype(int), 0, GRID - 1)
    cc = float(C[i[2], i[1], i[0]])
    g = np.array([GX[i[2], i[1], i[0]], GY[i[2], i[1], i[0]], GZ[i[2], i[1], i[0]]])
    n = float(np.linalg.norm(g)) + 1e-12
    return cc, g / n

def frame(p, v):
    cc, gh = sense(p)
    return [cc, gh[0], gh[1], gh[2], float(np.dot(v, gh))]

def step_env(p, v, a):
    if a > 0:
        e = EYE[(a - 1) // 2] * (1 if a % 2 == 1 else -1)
        v = v + TILT * e
        v = v / (np.linalg.norm(v) + 1e-12)
    p = np.clip(p + v * STEP, 0, GRID - 1)
    return p, v

class QNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(NT * 5, 64), nn.ReLU(),
                                 nn.Linear(64, 64), nn.ReLU(),
                                 nn.Linear(64, NACT))
    def forward(self, x):
        return self.net(x)

def rollout(net, rng, eps, train, buf, greedy=False):
    rebuild(SOURCES)
    p = np.array([20.0, 35.0, 20.0]) + rng.uniform(-2, 2, 3)
    v = rng.normal(0, 1, 3)
    v /= np.linalg.norm(v)
    live = list(SOURCES)
    captured = [False] * len(SOURCES)
    hist = [frame(p, v)] * NT
    prev_c = hist[-1][0]
    tot_r, steps, ncaps = 0.0, 0, 0
    um_src = np.array(SOURCES) * DX
    while steps < MAX_STEPS and ncaps < len(SOURCES):
        s = torch.tensor(np.array(hist).ravel(), dtype=torch.float32)
        if greedy:
            cc, gh = sense(p)
            gain = cc / (cc + 0.1)
            v = (1 - 0.8 * gain) * v + 0.8 * gain * gh
            v /= np.linalg.norm(v) + 1e-12
            a = 0
        elif train and rng.random() < eps:
            a = rng.integers(0, NACT)
        else:
            with torch.no_grad():
                a = int(net(s).argmax())
        p, v = step_env(p, v, a)
        cc, _ = sense(p)
        r = 100.0 * (cc - prev_c) - 0.002
        prev_c = cc
        steps += 1
        um = p * DX
        for i in range(len(SOURCES)):
            if not captured[i] and float(np.sqrt(((um - um_src[i]) ** 2).sum())) < CAPTURE_R:
                captured[i] = True
                ncaps += 1
                r += 1.0
                live = [sq for j, sq in enumerate(SOURCES) if not captured[j]]
                rebuild(live)
        if ncaps == len(SOURCES):
            r += 3.0
        hist = hist[1:] + [frame(p, v)]
        tot_r += r
        if train and buf is not None:
            buf.append((s.numpy(), a, r, np.array(hist).ravel().astype(np.float32),
                        ncaps == len(SOURCES)))
    return tot_r, steps * sim.DT, ncaps

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=1000)
    args = ap.parse_args()
    os.makedirs("results_dqn3d", exist_ok=True)
    torch.manual_seed(1)
    rng = np.random.default_rng(1)
    net, tgt = QNet(), QNet()
    tgt.load_state_dict(net.state_dict())
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()
    buf, gamma, hr, hc = [], 0.99, [], []
    t0 = time.time()
    for ep in range(1, args.episodes + 1):
        eps = max(0.05, 1.0 - 0.95 * ep / (args.episodes * 0.75))
        tot_r, tmin, nc = rollout(net, rng, eps, True, buf)
        hr.append(tot_r)
        hc.append(nc)
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
            print(f"ep {ep}/{args.episodes} eps={eps:.2f} rew={np.mean(hr[-100:]):.1f} "
                  f"caps={np.mean(hc[-100:]):.2f}/4", flush=True)
    torch.save(net.state_dict(), "results_dqn3d/model.pt")
    json.dump({"episodes": args.episodes, "seconds": time.time() - t0},
              open("results_dqn3d/train.json", "w"))
    dq, gr = [], []
    for i in range(10):
        _, t1, _ = rollout(net, np.random.default_rng(9000 + i), 0.0, False, None)
        _, t2, _ = rollout(net, np.random.default_rng(9000 + i), 0.0, False, None, True)
        dq.append(t1)
        gr.append(t2)
    json.dump({"dqn_min": [float(x) for x in dq], "greedy_min": [float(x) for x in gr],
               "dqn_mean": float(np.mean(dq)), "greedy_mean": float(np.mean(gr))},
              open("results_dqn3d/eval.json", "w"), indent=2)
    print(f"EVAL dqn={np.mean(dq):.1f} vs greedy={np.mean(gr):.1f} -> "
          f"{'BEATS' if np.mean(dq) < np.mean(gr) else 'does not beat'} greedy", flush=True)

if __name__ == "__main__":
    main()
