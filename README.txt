About: 
Liquid helium stands out as the paradigmatic instance of a superfluid -- a state of matter that flows without viscosity, transfers heat without a temperature gradient, and exhibits quantized rotational flow.  According to quantum many-body theory, the extraordinary properties of superfluid helium emerge from an underlying Bose broken symmetry.  This fundamental prediction can be tested by means of inelastic neutron scattering measurements at high momenta and high energies.  If one could access the impulse approximation regime, where atoms freely recoil from the impact of an incoming neutron, then one could directly observe the Bose-Einstein condensate present in superfluid helium.  However, in practical experiments, interactions of the recoiling helium atom with its nearest neighbors broaden the observed spectrum in such a way that the condensate does not appear a distinct and obvious feature in the data.  One must accurately work out the form of these "final state effects," if inelastic neutron scattering experiments are to be correctly interpreted.

This Python program is a numerical implementation of Richard Silver's Hard Core Perturbation Theory (HCPT), historically the first successful theory of final state effects in liquid helium.  An simple intuitive picture underlies the model.  Before the scattering event, the helium atoms are distributed according to the pair-correlation function of the system: they are each located near the minimum of the potential well created by their nearest neighbors.  Upon the impact of a high-energy neutron, a recoiling helium atom travels a finite distance away from that minimum, after which it may encounter the steeply repulsive cores of its neighbors.  Heuristically, HCPT is a semiclassical trajectory calculation that relates final state effects to the probability the recoiling helium atom will suffer no collisions as a function of distance.  The only inputs to the theory are the interatomic potential and pair-correlation function.  Using HCPT, this python module compares ab initio predictions of the one-body density matrix of superfluid with inelastic neuton scattering measurements.

References:
-- R. N. Silver, "Theory of deep inelastic neutron scattering: Hard-core perturbation theory," Phys. Rev. B 38, 2283-2296 (1988).
-- R. N. Silver, "Theory of deep inelastic neutron scattering.  II.  Application to normal and superfluid 4He," Phys. Rev. B 39, 4002-4029 (1989).
-- T. R. Prisk et al, "The Momentum Distribution of Liquid 4-He," J. Low Temp Phys. 189, 158-184 (2017).

Contents:
  -- requirements.txt: This file lists all needed python libraries.
  -- He4_calc.py: This is the main module.  The script calculates a theoretical
  prediction for the neutron Compton profile and then compares it to
  experimental data.
  -- He4_function_test_script.py: This script is intended to check that the
  various functions yield physically reasonable and correct results.  A number
  of curves are generated and then plotted.
  -- He4_data.py: This module contains numerical data required for the program.
  -- He4_functions.py: This module is a function library for the program.
  -- x_27.0.npy, rGammas_27.0.npy, iGammas_27.0.npy: Numerical data needed to
  run the test script.

Notes:
  -- To install needed packages, use: pip install -r requirements.txt
  -- The main module requires ~1 core-hour to finish.
