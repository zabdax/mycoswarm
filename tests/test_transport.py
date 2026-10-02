"""Transport physics tests: FD diffusion solver + effective-diffusion measurement.
RED step: transport.py does not exist yet — these must fail with ModuleNotFoundError.
"""
import numpy as np


def test_solver_matches_analytic_empty_domain():
    # Scheme correctness via manufactured smooth solution (Dirichlet faces).
    # Point-source Yukawa comparison is singularity-limited on any grid and is
    # covered by the correlation test below instead.
    from transport import solve_steady_state
    import numpy as np
    n, dx, lam = 24, 5.0, 30.0
    k2 = 1.0 / lam ** 2
    L = (n - 1) * dx
    z, y, x = np.mgrid[0:n, 0:n, 0:n] * dx
    exact = np.sin(np.pi * x / L) * np.sin(np.pi * y / L) * np.sin(np.pi * z / L)
    f = (-3 * (np.pi / L) ** 2 - k2) * exact
    obst = np.zeros((n, n, n), bool)
    # drive solver with explicit forcing by placing scaled source density
    from transport import _solve_general
    num = _solve_general(f, k2, n, dx, obst)
    rel = np.linalg.norm(num - exact) / np.linalg.norm(exact)
    assert rel < 0.01, f"scheme inaccurate on smooth MMS: rel = {rel:.4f}"


def test_solver_yukawa_shell_correlation():
    from transport import solve_steady_state, analytic_field
    import numpy as np
    n = 40
    obst = np.zeros((n, n, n), bool)
    num = solve_steady_state([(20, 20, 20)], lam=30.0, n=n, dx=5.0, obstacles=obst)
    ana = analytic_field([(20, 20, 20)], lam=30.0, n=n, dx=5.0)
    z, y, x = np.mgrid[0:n, 0:n, 0:n]
    r = np.sqrt(((x - 20) * 5) ** 2 + ((y - 20) * 5) ** 2 + ((z - 20) * 5) ** 2)
    m = (r > 15) & (r < 80)
    cc = np.corrcoef(num[m], ana[m])[0, 1]
    # 0.995, not 1.0: lattice cell-delta steepens near-source kappa by ~25%
    # (measured 0.0417 vs 0.0333); shape agreement outside the singular core
    assert cc > 0.995, f"Yukawa shell shape mismatch: r = {cc:.4f}"


def test_deff_empty_domain_equals_free_diffusion():
    from transport import measure_deff
    obst = np.zeros((20, 20, 20), bool)
    deff, d0 = measure_deff(obst, dx=5.0, d0=500.0, n_walkers=2000, steps=2000, seed=3)
    assert abs(deff / d0 - 1.0) < 0.10, f"tortuosity off in empty domain: {deff/d0:.3f}"


def test_deff_obstructed_below_free():
    from transport import measure_deff
    sim = __import__("mycoswarm_abm_3d", fromlist=["build_obstacles"])
    import mycoswarm_abm_3d as m
    obst = m.build_obstacles(11)  # 15% grains, same generator as v1
    deff, d0 = measure_deff(obst, dx=5.0, d0=500.0, n_walkers=2000, steps=2000, seed=4)
    assert deff < d0, f"grains should obstruct: {deff:.1f} vs {d0:.1f}"
    assert deff / d0 > 0.3, f"unphysical blockage: {deff/d0:.3f}"
