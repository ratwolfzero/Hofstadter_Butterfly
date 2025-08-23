import numpy as np
import matplotlib.pyplot as plt
from math import gcd
from joblib import Parallel, delayed
from scipy.stats import gaussian_kde
from dataclasses import dataclass

# ---------------- CONFIG ----------------


@dataclass
class Config:
    max_q: int = 100
    grid_res: int = 100
    bw_method: float = 0.1
    figsize: tuple = (8, 6)
    dpi: int = 150
    cmap_kde: str = "coolwarm"
    cmap_scatter: str = "magma"

# ---------------- CORE COMPUTATION ----------------


def hofstadter_hamiltonian(q, alpha):
    """Return sorted eigenvalues of the Harper Hamiltonian with flux α = p/q."""
    n = np.arange(q)
    diag = 2 * np.cos(2 * np.pi * alpha * n)
    H = np.diag(diag) + np.roll(np.eye(q), 1, axis=0) + \
        np.roll(np.eye(q), -1, axis=0)
    return np.sort(np.linalg.eigvalsh(H))


def compute_eigenvalues(p, q):
    """Eigenvalues for (p, q) if coprime, else empty."""
    if gcd(p, q) == 1:
        alpha = p / q
        evals = hofstadter_hamiltonian(q, alpha)
        return np.full(len(evals), alpha), evals
    return np.array([]), np.array([])


def compute_q(q):
    """Compute all eigenvalues for fixed q."""
    results = [compute_eigenvalues(p, q) for p in range(1, q+1)]
    alphas, energies = zip(*results)
    return np.concatenate(alphas), np.concatenate(energies)


def generate_hofstadter_spectrum(max_q):
    """Return arrays of α and energies up to denominator max_q."""
    if not isinstance(max_q, int) or max_q <= 0:
        raise ValueError("max_q must be a positive integer")
    results = Parallel(n_jobs=-1)(delayed(compute_q)(q)
                                  for q in range(1, max_q+1))
    alphas, energies = zip(*results)
    return np.concatenate(alphas), np.concatenate(energies)

# ---------------- PLOTTING ----------------


def plot_hofstadter_butterfly(alphas, energies, cfg: Config):
    """
    Plot Hofstadter butterfly:
    - Background = KDE density of states (no colorbar)
    - Overlay = Eigenvalues colored by energy (with colorbar)
    """
    plt.style.use("dark_background")
    plt.figure(figsize=cfg.figsize, dpi=cfg.dpi)

    # KDE density (background shading)
    data = np.vstack([alphas, energies])
    kde = gaussian_kde(data, bw_method=cfg.bw_method)
    x_grid = np.linspace(0, 1, cfg.grid_res)
    y_grid = np.linspace(energies.min(), energies.max(), cfg.grid_res)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)
    plt.contourf(X, Y, Z, levels=20, cmap=cfg.cmap_kde, alpha=0.5)

    # Eigenvalue scatter overlay
    sc = plt.scatter(alphas, energies, s=1, c=energies,
                     cmap=cfg.cmap_scatter, alpha=0.6, edgecolors="none")

    # Axis and labels
    plt.gca().set_aspect("auto")
    plt.xlabel("Magnetic Flux (α = p/q)", fontsize=12, color="white")
    plt.ylabel("Energy", fontsize=12, color="white")
    plt.title(
        "Hofstadter Butterfly\n"
        "Background: KDE density of states\n"
        "Overlay: Eigenvalues (color = energy, see colorbar)",
        fontsize=12, color="white", pad=12
    )
    plt.grid(True, linestyle="--", alpha=0.3, color="gray")

    # Single colorbar for scatter (energy)
    plt.colorbar(sc, label="Energy")

    plt.show()


# ---------------- MAIN ----------------
if __name__ == "__main__":
    cfg = Config()  # all knobs in one place
    alphas, energies = generate_hofstadter_spectrum(cfg.max_q)
    plot_hofstadter_butterfly(alphas, energies, cfg)
