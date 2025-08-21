# 🦋 The Hofstadter Butterfly

## 📖 Historical Context

The **Hofstadter butterfly** is a famous fractal pattern discovered by physicist **Douglas Hofstadter** in 1976. It appears when studying the motion of electrons on a two-dimensional lattice in the presence of a **perpendicular magnetic field**.

The system is modeled by the **Harper (or Aubry-André-Harper) Hamiltonian**, which describes the tight-binding approximation of an electron hopping between lattice sites with an applied magnetic flux.

When the **magnetic flux per plaquette** is a rational number \$\alpha = p/q\$, the spectrum splits into **\$q\$ subbands**, leading to a rich, self-similar structure that resembles a butterfly.

This fractal spectrum is one of the most iconic results in condensed matter physics, with deep connections to:

* **Bloch electrons in a magnetic field**
* **Quasicrystals**
* **Quantum Hall effect**
* **Topological phases of matter**

---

## ⚛️ Mathematical Background

The Harper Hamiltonian for a \$q \times q\$ system with magnetic flux \$\alpha = p/q\$ is written as:

$$
H_{n,m} = 2 \cos(2 \pi \alpha n) \, \delta_{n,m}
+ \delta_{n,m+1} + \delta_{n,m-1}
$$


Here:

* \$n, m \in {0, 1, \dots, q-1}\$ are lattice indices
* \$\alpha = p/q\$ is the magnetic flux per plaquette (in units of the magnetic flux quantum)
* \$\delta\$ is the Kronecker delta

The eigenvalues of \$H\$ give the allowed **energy levels** of the system.

When we scan \$\alpha \in \[0,1]\$, plotting the corresponding eigenvalues, the **Hofstadter butterfly** emerges.

---

## 🧮 Code Overview

This repository provides a **parallelized Python implementation** for generating and plotting the Hofstadter butterfly spectrum with additional visualization enhancements.

### 🔑 Core Components

#### 1. `hofstadter_hamiltonian(q, alpha)`

Constructs the \$q \times q\$ Harper Hamiltonian matrix for flux \$\alpha = p/q\$, and returns its sorted eigenvalues.
Optimized using NumPy for vectorized operations.

#### 2. `compute_eigenvalues(p, q)`

Computes eigenvalues for a single pair \$(p, q)\$ if \$\gcd(p, q) = 1\$.

* Returns both \$\alpha = p/q\$ and the associated eigenvalues.
* Ensures only **coprime pairs** are considered (avoiding redundant spectra).

#### 3. `compute_q(q)`

Computes eigenvalues for all valid numerators \$p\$ for a given denominator \$q\$.

#### 4. `generate_hofstadter_spectrum(max_q=50)`

Generates the complete spectrum for all \$\alpha = p/q\$ with denominators $q \leq \text{max\_q}$.

* Uses **joblib** for parallel computation.
* Returns two arrays:

  * `alphas`: magnetic flux values
  * `energies`: corresponding eigenvalues

#### 5. `plot_hofstadter_butterfly(max_q=120, grid_res=200)`

Plots the Hofstadter butterfly with:

* **KDE density heatmap** (using SciPy’s `gaussian_kde`)
* **Scatter overlay** with color-coded energies
* Dark aesthetic style with smooth contours

---

## 📊 Example Output

Running:

```bash
python hofstadter.py
```

will produce a high-resolution visualization of the Hofstadter butterfly:

![Example Output](example.png)  <!-- Replace with actual screenshot -->

---

## 🎨 Understanding the Visualization

The graphical output combines **two layers**:

### 1. KDE Density Map (background heatmap)

* Computed using *kernel density estimation (KDE)*.
* Represents the **density of states (DOS)** in the \$(\alpha, E)\$ plane.
* Bright/hot regions = high concentration of eigenvalues (energy bands).
* Dark/cool regions = low density → **spectral gaps**.

Mathematically, the DOS is estimated as:

$$
\rho(\alpha, E) \approx \frac{1}{N h^2} \sum_{i=1}^N
K\!\left(\frac{\alpha-\alpha_i}{h}, \frac{E-E_i}{h}\right),
$$

where \$K\$ is a Gaussian kernel, \$h\$ is the bandwidth, and \$(\alpha\_i, E\_i)\$ are eigenvalues.

### 2. Scatter Overlay (points)

* Each point \$(\alpha, E)\$ corresponds to an **actual eigenvalue** computed from the Harper Hamiltonian.
* The **color** of each point encodes its energy \$E\$ (see colorbar).
* Ensures the **raw spectrum** is visible, not only the smoothed KDE.

---

## 🚀 Usage

### Install dependencies

```bash
pip install numpy matplotlib joblib scipy
```

### Run the script

```bash
python hofstadter.py
```

### Adjust parameters

* `max_q`: controls the fineness of the spectrum (higher = more detailed but slower).
* `grid_res`: resolution of the KDE heatmap.

---

## ⚡ Performance Notes

* **Parallelization**: eigenvalue computations are distributed across available CPU cores via `joblib`.
* **Vectorization**: the Hamiltonian is built using NumPy operations instead of Python loops.
* **Concatenation**: eigenvalue arrays are concatenated efficiently to avoid list overhead.

---

## 📚 References

* D. R. Hofstadter, *“Energy levels and wave functions of Bloch electrons in rational and irrational magnetic fields”*, Phys. Rev. B **14**, 2239 (1976).
* M. Kohmoto, B. Sutherland, and C. Tang, *“Critical wave functions and a Cantor-set spectrum of a one-dimensional quasicrystal model”*, Phys. Rev. B **35**, 1020 (1987).

---

✨ With this code, you can generate your own Hofstadter butterflies, visualize the **density of states**, and explore the fractal spectrum of quantum systems under magnetic fields.
