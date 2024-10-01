# -*- coding: utf-8 -*-

"""
Common functions that are supposed to be imported in __init__.py
and thus made available to all modules.

"""

__author__ = "Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "03/06/2020"

import numpy as np
from scipy.constants import h, c, eV


def wl_to_en(wl):
    """Convert wavelength (m) to photon energy (eV)."""
    energy = h*c/np.array(wl)/eV
    return energy


def en_to_wl(energy):
    """Convert photon energy (eV) to wavelength (m)."""
    wl = h*c/np.array(energy)/eV
    return wl


def q_to_tth(q, wl):
    """Convert q (1/m) to scattering angle (rad)."""
    tth = 2*np.arcsin(wl*q/(4*np.pi))
    return tth


def tth_to_q(tth, wl):
    """Convert scattering angle (rad) to q (1/m)."""
    q = 4*np.pi*np.sin(tth/2)/wl
    return q


def tth_to_r(tth, dist):
    """Convert scattering angle (rad) to detector radius (m)."""
    r = dist*np.tan(tth)
    return r


def r_to_tth(r, dist):
    """Convert detector radius (m) to scattering angle (rad)."""
    tth = np.arctan2(r/dist)
    return tth
