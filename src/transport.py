"""Grain-aware transport physics: FD steady-state solver + Monte Carlo Deff.
Minimal implementation to satisfy tests/test_transport.py.
"""
import numpy as np


def analytic_field(sources, lam, n, dx):
    z, y, x = np.mgrid[0:n, 0:n, 0:n]
    c = np.zeros((n, n, n))
    for (sx, sy, sz) in sources:
        r = np.sqrt(((x - sx) * dx) ** 2 + ((y - sy) * dx) ** 2
                    + ((z - sz) * dx) ** 2) + dx
        c += np.exp(-r / lam) / (r / lam)
    return c / c.max()


def _solve_general(forcing, k2, n, dx, obstacles, tol=1e-5, max_iter=20000):
    """Jacobi solve of (Laplacian - k^2) c = forcing with Dirichlet faces.
    Blocked (grain) cells get zero-flux treatment via mirror fill: each takes
    the mean of its free neighbors (absorbing grains were tried and rejected —
    they act as sinks and distort gradients). Raises on non-finite result."""
    c = np.zeros((n, n, n))
    free = ~obstacles
    has_grains = bool((~free).any())
    free_f = free.astype(float)
    denom = 6.0 + k2 * dx ** 2

    def roll_sum(a):
        return (np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1)
                + np.roll(a, -1, 1) + np.roll(a, 1, 2) + np.roll(a, -1, 2))

    for _ in range(max_iter):
        nb = roll_sum(c)
        new = np.where(free, (nb - dx ** 2 * forcing) / denom, 0.0)
        # Dirichlet (absorbing) faces: infinite-domain analog; periodic wrap
        # traps a uniform background mode that corrupts the shape (see tests)
        new[0, :, :] = new[-1, :, :] = 0.0
        new[:, 0, :] = new[:, -1, :] = 0.0
        new[:, :, 0] = new[:, :, -1] = 0.0
        if has_grains:
            cnt = roll_sum(free_f)
            fill = np.where(cnt > 0, roll_sum(np.where(free, new, 0.0)) / np.maximum(cnt, 1), 0.0)
            new = np.where(free, new, fill)
        if not np.all(np.isfinite(new)):
            raise ValueError("solver diverged to non-finite values")
        delta = np.abs(new - c).max()
        c = new
        if delta < tol:
            break
    return c


def solve_steady_state(sources, lam, n, dx, obstacles, tol=1e-5, max_iter=20000):
    """Screened-Poisson (Yukawa) solve: (Laplacian - k^2) c = -S at sources,
    no-flux on blocked cells. Normalized to max 1 like analytic_field."""
    k2 = 1.0 / lam ** 2
    forcing = np.zeros((n, n, n))
    for (sx, sy, sz) in sources:
        forcing[int(sz), int(sy), int(sx)] = -6.0  # -S cell delta
    c = _solve_general(forcing, k2, n, dx, obstacles, tol, max_iter)
    if not np.all(np.isfinite(c)) or c.max() <= 0:
        raise ValueError("solver produced empty/non-finite field (source in grain?)")
    return c / c.max()


def solve_field(sources, lam, n, dx, obstacles):
    """Field + gradients wrapper for the ABM loop."""
    c = solve_steady_state(sources, lam, n, dx, obstacles)
    gz, gy, gx = np.gradient(c, dx)
    return c, gx, gy, gz


def measure_deff(obstacles, dx, d0, n_walkers=2000, steps=2000, seed=0):
    """Monte Carlo tracer diffusion in periodically tiled grain matrix.
    Returns (Deff, D0): Deff from MSD slope/6 over second half; D0 = input."""
    rng = np.random.default_rng(seed)
    n = obstacles.shape[0]
    dt = (dx / 2) ** 2 / (2 * d0)  # Gaussian sigma = dx/2 per axis per step
    sig = np.sqrt(2 * d0 * dt)
    pos = rng.uniform(0, n * dx, (n_walkers, 3))
    msd = np.zeros(steps)
    p0 = pos.copy()
    for s in range(steps):
        trial = pos + rng.normal(0, sig, pos.shape)
        cell = (np.floor(trial / dx).astype(int)) % n
        blocked = obstacles[cell[:, 2], cell[:, 1], cell[:, 0]]
        pos = np.where(blocked[:, None], pos, trial)  # reject into grains
        msd[s] = ((pos - p0) ** 2).sum(axis=1).mean()
    t = np.arange(1, steps + 1) * dt
    half = steps // 2
    slope = np.polyfit(t[half:], msd[half:], 1)[0]
    return float(slope / 6.0), float(d0)
