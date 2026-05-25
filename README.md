# hard-core-perturbation-theory

## About

`hard-core-perturbation-theory` is a Python implementation of Richard
Silver's Hard Core Perturbation Theory (HCPT) for final-state effects in
deep-inelastic neutron scattering from liquid helium.

Liquid helium stands out as the paradigmatic instance of a superfluid -- a
state of matter that flows without viscosity, transfers heat without a
temperature gradient, and exhibits quantized rotational flow. According to
quantum many-body theory, the extraordinary properties of superfluid helium
emerge from an underlying Bose broken symmetry. This fundamental prediction can
be tested by means of inelastic neutron scattering measurements at high momenta
and high energies. If one could access the impulse approximation regime, where
atoms freely recoil from the impact of an incoming neutron, then one could
directly observe the Bose-Einstein condensate present in superfluid helium.
However, in practical experiments, interactions of the recoiling helium atom
with its nearest neighbors broaden the observed spectrum in such a way that the
condensate does not appear as a distinct and obvious feature in the data. One
must accurately work out the form of these "final state effects," if inelastic
neutron scattering experiments are to be correctly interpreted.

This Python program is a numerical implementation of Richard Silver's Hard
Core Perturbation Theory (HCPT), historically the first successful theory of
final state effects in liquid helium. A simple intuitive picture underlies the
model. Before the scattering event, the helium atoms are distributed according
to the pair-correlation function of the system: they are each located near the
minimum of the potential well created by their nearest neighbors. Upon the
impact of a high-energy neutron, a recoiling helium atom travels a finite
distance away from that minimum, after which it may encounter the steeply
repulsive cores of its neighbors. Heuristically, HCPT is a semiclassical
trajectory calculation that relates final state effects to the probability the
recoiling helium atom will suffer no collisions as a function of distance. The
only inputs to the theory are the interatomic potential and pair-correlation
function. Using HCPT, this Python module compares ab initio predictions of the
one-body density matrix of superfluid helium with high-precision inelastic
neutron scattering measurements.

## Status

Version: `1.0.0`

## Requirements

Required Python packages:

```text
numpy
scipy
matplotlib
pyfiglet
tqdm
```

Optional Python packages:

```text
scienceplots
```

## Usage

Main driver:

```powershell
python main.py
```

Diagnostic plots:

```powershell
python tests\diagnostics.py
```

## Repository layout

```text
hard-core-perturbation-theory/
├── main.py
├── src/
│   ├── __init__.py
│   ├── data.py
│   └── functions.py
├── data/
│   ├── x_27.0.npy
│   ├── rGammas_27.0.npy
│   ├── iGammas_27.0.npy
│   ├── x_vals.txt
│   ├── gamma_vals_real.txt
│   ├── gamma_vals_imag.txt
│   ├── Y_data.txt
│   ├── J_data.txt
│   ├── err_data.txt
│   ├── Y_theory.txt
│   └── J_theory.txt
├── tests/
│   └── diagnostics.py
├── requirements.txt
├── README.md
└── LICENSE
```

## References and Citations

If you find this code helpful for either teaching or research, please cite the
original work by Silver and this repository:

```text
R. N. Silver,
"Theory of deep inelastic neutron scattering: Hard-core perturbation theory,"
Physical Review B 38, 2283-2296 (1988).
```

```text
R. N. Silver,
"Theory of deep inelastic neutron scattering. II. Application to normal and
superfluid 4He,"
Physical Review B 39, 4022-4029 (1989).
```

```text
T. R. Prisk et al.,
"The Momentum Distribution of Liquid 4-He,"
Journal of Low Temperature Physics 189, 158-184 (2017).
```

```text
Timothy Prisk, hard-core-perturbation-theory, version 1.0.0,
https://github.com/prisktr/hard-core-perturbation-theory
```