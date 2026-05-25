#!/usr/bin/env python3
"""
Filename: main.py
Author: Timothy Prisk
Version: 1.0.0
Description: Driver for Hard Core Perturbation Theory calculation.
"""

__version__ = "1.0.0"

# General modules.
import multiprocessing as mp
from pathlib import Path
import shutil
from tqdm import tqdm

# Science modules.
import numpy as np
import matplotlib.pyplot as plt
import pyfiglet
from scipy import interpolate

# hcpt modules.
from src.functions import gamma_hcpt, theory
from src.data import Q, Y_data, J_data, err_data

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
# Helpers.
#

def print_banner() -> None:

    text = "HCPT"
    width = shutil.get_terminal_size(fallback=(80, 24)).columns

    try:
        import pyfiglet
        banner = pyfiglet.figlet_format(text, font="small")
    except pyfiglet.FontNotFound:
        banner = text

    if any(len(line) > width for line in banner.splitlines()):
        print(text)
    else:
        print(banner.rstrip())

    print(f"Version: {__version__}\n")

def _gamma_task(args: tuple[float, float]) -> complex:
    x, q = args
    return gamma_hcpt(x, q)


def _theory_task(args) -> float:
    y, gamma_r, gamma_i = args
    return theory(y, gamma_r, gamma_i)



#
# Driver.
#

def main():
    
    print_banner()

    # Multicore calculation of Gamma(x) and J(Y, Q).
    # First, I generate a "table" of Gamma(x).  Then, I interpolate over the 
    # table in order to obtain smooth functions for its real and imaginary
    # parts.  Finally, a theoretical prediction for J(Y, Q) is generated.

    x_vals = np.arange(0.0, 30.0, 0.5)
    gamma_tasks = [(x, Q) for x in x_vals]


    with mp.Pool() as pool:
        gamma_vals = list(
            tqdm(pool.imap(_gamma_task, gamma_tasks, chunksize = 1),
                total = len(gamma_tasks),
                desc = "Computing Gamma(x)",
                unit = "point"))
        gamma_vals = np.asarray(gamma_vals, dtype = complex)

        gamma_r = interpolate.interp1d(
            x_vals, np.real(gamma_vals), kind = 'cubic')
        gamma_i = interpolate.interp1d(
            x_vals, np.imag(gamma_vals), kind = 'cubic')

        Y_theory = np.arange(-4.0, 4.0, 0.25)

        theory_tasks = [(Y, gamma_r, gamma_i) for Y in Y_theory]

        J_theory = list(
            tqdm(
                pool.imap(_theory_task, theory_tasks, chunksize = 1),
                total = len(theory_tasks),
                desc = "Computing J(Y,Q)",
                unit = "point",
            )
        )
        J_theory = np.asarray(J_theory, dtype = float)

    
    # Save the results.
    gamma_vals_real = np.real(gamma_vals)
    gamma_vals_imag = np.imag(gamma_vals)
    
    output_dir = Path("outputs")
    output_dir.mkdir(parents = True, exist_ok = True)

    np.savetxt(output_dir / "x_vals.txt", x_vals)
    np.savetxt(output_dir / "gamma_vals_real.txt", gamma_vals_real)
    np.savetxt(output_dir / "gamma_vals_imag.txt", gamma_vals_imag)

    np.savetxt(output_dir / "Y_theory.txt", Y_theory)
    np.savetxt(output_dir / "J_theory.txt", J_theory)

    np.savetxt(output_dir / "Y_data.txt", Y_data)
    np.savetxt(output_dir / "J_data.txt", J_data)
    np.savetxt(output_dir / "err_data.txt", err_data)
    

    # Compare the theoretical prediction with experimental results.
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents = True, exist_ok = True)

    fig, ax = plt.subplots()

    ax.errorbar(Y_data, 
                J_data, 
                yerr = err_data, 
                fmt = 'o', 
                color = 'k',
                label = 'Experiment',
                zorder = 1)
    ax.plot(Y_theory, 
            J_theory, 
            'r-', 
            label = 'Theory',
            zorder = 2)

    ax.set_xlabel(r"$Y~[\AA^{-1}]$")
    ax.set_ylabel(r"$J(Y,Q)~[\AA]$")
    ax.set_title('Neutron Compton profile')
    ax.legend(loc = 'best', frameon = False)

    fig.tight_layout()

    pdf_path = figure_dir / "hcpt_neutron_compton_profile.pdf"
    png_path = figure_dir / "hcpt_neutron_compton_profile.png"

    fig.savefig(pdf_path,
                 bbox_inches = "tight")

    fig.savefig(png_path,
                 dpi = EXPORT_DPI,
                 bbox_inches = "tight")
 
    print("\nCalculation complete.")
    print(f"Numerical outputs saved to: {output_dir.resolve()}")
    print(f"Figure PDF saved to:       {pdf_path.resolve()}")
    print(f"Figure PNG saved to:       {png_path.resolve()}")
    
    plt.show()
    plt.close(fig)
    print("\nGoodbye!")


if __name__ == "__main__":
    main()