"""
Filename: diagnostics.py
Author: Timothy Prisk
Version: 1.0.0
Description: Diagnostic script.
"""

# General modules.
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Science modules.
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# hcpt modules.
from src.functions import v, g, r0, phase_shift, OBDM, R, resolution
from src.functions import prediction
from src.data import Q, DISTANCE, PAIR_DISTRIBUTION

# Nature-style one-column figure geometry.
try: 
    import scienceplots
    plt.style.use(['science', 'nature', 'no-latex'])
    plt.rcParams['axes.linewidth'] = 1
except ImportError:
    print("SciencePlots not found.  Using default matplotlib style.")


MM_PER_INCH = 25.4
FIG_WIDTH = 89.0 / MM_PER_INCH
FIG_HEIGHT = 63.0 / MM_PER_INCH
DISPLAY_DPI = 120
EXPORT_DPI = 1200

plt.rcParams.update({
    "figure.figsize": (FIG_WIDTH, FIG_HEIGHT),
    "figure.dpi": DISPLAY_DPI,
    "savefig.dpi": EXPORT_DPI,
    "font.size": 7,
    "axes.labelsize": 7,
    "axes.titlesize": 7,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,
})

#
# Diagnostic visualizations of the interatomic potential, pair distribution 
# function, turning point, phase shift, gamma function, one-body density matrix,
# final state effect function, resolution, and final predictions. 
#

OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures" / "diagnostics"
FIGURE_DIR.mkdir(parents = True, exist_ok = True)

def save_and_show(name: str) -> None:
    """Save the current diagnostic figure as PDF and PNG, then show it."""
    fig = plt.gcf()
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"{name}.pdf", bbox_inches = "tight")
    fig.savefig(FIGURE_DIR / f"{name}.png",
                dpi = EXPORT_DPI,
                bbox_inches = "tight")
    plt.show()
    plt.close(fig)


# Verify that the shape of the interatomic potential is correct.

r_test = np.arange(2.6, 4.3, 0.05)
v_test = np.zeros(len(r_test))

for j in range(len(r_test)):
    v_test[j] = 11.60451812*v(r_test[j]) # 1 meV = 11.60451812 K

plt.plot(r_test, v_test, 'k-')
plt.xlabel(r'r [$\AA$]')
plt.ylabel(r'V(r) [K]')
plt.title('Aziz Potential')
save_and_show("aziz_potential")


# Verify that the interpolation of g(r) is correct.

r_structure_test = np.arange(0.0, 15.0, 0.01)
g_structure_test = np.zeros(len(r_structure_test))

for k in range(len(r_structure_test)):
    g_structure_test[k] = g(r_structure_test[k])

plt.plot(DISTANCE, PAIR_DISTRIBUTION, 'ko', label = 'Exp')
plt.plot(r_structure_test, g_structure_test, 'r-', label = 'interpolation')
plt.xlabel(r'r [$\AA$]')
plt.xlim([0.0, 15.0])
plt.ylabel(r'g(r)')
plt.title('Pair Distribution Function')
save_and_show("pair_distribution")


# Verify turning point calculation is correct.  Use an impact parameter of
# of zero (b = 0).

BTEST = 0.0

q_test = np.arange(5.0, 220.0, 10.0)
r0_test = np.zeros(len(q_test))

for k in range(len(q_test)):
    r0_test[k] = r0(0.0, q_test[k])

plt.semilogx(q_test, r0_test, 'k-')
plt.xlabel(r'$Q~[\AA^{-1}]$')
plt.ylabel(r'$r_0~[\AA]$')
plt.title('Classical turning point')
save_and_show("turning_point")


# Check the JWKB phase shift calculations.

b_test = np.arange(0.0, 4.0, 0.05)
phase_test = np.zeros(len(b_test))

for k in range(len(phase_test)):
    phase_test[k] = phase_shift(b_test[k], Q)

plt.plot(b_test, phase_test, 'k-')
plt.xlabel(r'Impact parameter $b~[\AA]$')
plt.ylabel(r'$\delta_b$')
plt.title('JKWB phase shift')
save_and_show("phase_shift")

# Visualize the HCPT gamma function.  Pre-existing files are loaded because
# the determination of Gamma is computation intensive.

x_test = np.load(DATA_DIR / "x_27.0.npy")
rGamma_test = np.load(DATA_DIR / "rGammas_27.0.npy")
iGamma_test = np.load(DATA_DIR / "iGammas_27.0.npy")

plt.plot(x_test, rGamma_test, 'k--',
         label = r'$\mathrm{Re}[\Gamma(x)]$')
plt.plot(x_test, iGamma_test, 'k-',
         label = r'$\mathrm{Im}[\Gamma(x)]$')
plt.xlabel(r'$x~[\AA]$')
plt.legend(loc = 'upper right')
save_and_show("gamma_function")

# Interpolation over real and imaginary parts of gamma.
gamma_r = interpolate.interp1d(x_test, rGamma_test, kind = 'cubic')
gamma_i = interpolate.interp1d(x_test, iGamma_test, kind = 'cubic')

# Verify that the one-body density matrix, final state effect function,
# resolution, and final predictions look reasonable.

s_test = np.arange(0.0, 15.0, 0.1)

obdm_test = np.zeros(len(s_test), dtype = float)

r_test_full = np.zeros(len(s_test), dtype = complex)
r_test_reals = np.zeros(len(s_test), dtype = float)
r_test_imags = np.zeros(len(s_test), dtype = float)

resolution_test = np.zeros(len(s_test), dtype = float)

prediction_test = np.zeros(len(s_test), dtype = complex)
prediction_test_reals = np.zeros(len(s_test), dtype = float)
prediction_test_imags = np.zeros(len(s_test), dtype = float)

for k in range(len(s_test)):
    obdm_test[k] = OBDM(s_test[k])
    r_test_full[k] = R(s_test[k], gamma_r, gamma_i)
    resolution_test[k] = resolution(s_test[k])
    prediction_test[k] = prediction(s_test[k], gamma_r, gamma_i)

r_test_reals = np.real(r_test_full)
r_test_imags = np.imag(r_test_full)

prediction_test_reals = np.real(prediction_test)
prediction_test_imags = np.imag(prediction_test)

plt.plot(s_test, obdm_test, 'k-', label = 'OBDM')
plt.plot(s_test, r_test_reals, 'r-', label = 'Re HCPT')
plt.plot(s_test, r_test_imags, 'r--', label = 'Im HCPT')
plt.plot(s_test, resolution_test, 'b-', label = 'Res.')
plt.plot(s_test, prediction_test_reals, 'g-', label = 'Re J(s, Q)')
plt.plot(s_test, prediction_test_imags, 'g--', label = 'Im J(s, Q)')
plt.xlabel(r'$s~[\AA]$')
plt.legend(loc = 'upper right')
save_and_show("predictions")




