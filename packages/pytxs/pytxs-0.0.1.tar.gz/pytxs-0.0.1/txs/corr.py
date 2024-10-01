# -*- coding: utf-8 -*-
"""Corrections for azimuthal integrated curves."""

__author__ = "Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "01/09/2021"


import numpy as np
import xraydb

# create list of xraydb materials (materials name + materials formula)
_xraydb_materials = xraydb.materials._read_materials_db()
materials_names = list(_xraydb_materials.keys())
materials_formula = [m.formula for m in _xraydb_materials.values()]


def get_sensor_info(detector_name):
    """Get sensor material, thickness and density of known detectors."""

    detector_name = detector_name.lower()

    if detector_name in ['rayonix mx170-hs', 'rayonix']:
        sensor_material = 'Gd2O2S'
        sensor_thickness = 40e-6
        sensor_density = 4.3*1e3
    elif detector_name in ['maxipix 5x1', 'maxipix 2x2', 'maxipix']:
        sensor_material = 'Si'
        sensor_thickness = 500e-6
        sensor_density = get_density('Si')
    else:
        sensor_material = None
        sensor_thickness = None
        sensor_density = None

    return (sensor_material, sensor_thickness, sensor_density)


def sensor_absorption(tth, material, energy, thickness, density=None):
    """
    Calculate the angular dependent absorption of a sensor.

    Parameters
    ----------
    tth : float or array-like
        Scattering angle (deg).
    material : str
        Chemical formula or material from materials list ('xraydb').
    energy : float
        Photon energy (eV).
    thickness : float
        Sensor thickness (m).
    density : float
        Sensor density (kg/m3).

    Returns
    -------
    A : ndarray
        Sensor absorption.

    """

    mu = get_mu(material, energy, density=density)

    cos = np.cos(np.deg2rad(tth))

    t = np.exp(-mu*thickness/cos)

    A = (1-t)

    return A


def sample_transmission(tth, material, energy, thickness, density=None):
    """
    Calculate the angular dependent transmission of a sample.

    The sample is assumed to be a homogenous sheet with given thickness.

    Parameters
    ----------
    tth : float or array-like
        Scattering angle (deg).
    material : str
        Chemical formula or material from materials list ('xraydb').
    energy : float
        Photon energy (eV).
    thickness : float
        Sample thickness (m).
    density : float
        Sample density (kg/m3).

    Returns
    -------
    t : ndarray
        Sample transmission.

    """

    mu = get_mu(material, energy, density=density)

    cos = np.cos(np.deg2rad(tth))

    t1 = np.exp(-mu*thickness)
    t2 = np.exp(-mu*thickness/cos)

    t = 1/(mu*thickness) * cos/(1-cos) * (t1-t2)

    return t


def get_density(material):
    """
    Return the density of a material in kg/m3.
    """
    check_material(material)
    density = xraydb.get_material(material)[1]
    density *= 1e3
    return density


def get_mu(material, energy, density=None):
    """
    Return the absorption coefficient of a material in 1/m.
    """
    check_material(material)
    if density is not None:
        density /= 1e3
    mu = xraydb.material_mu(material, energy, density=density)*1e2
    return mu



def material_in_xraydb(material):
    """Check if material is in xraydb."""

    global materials_names, materials_formula

    cond1 = material.lower() in materials_names
    cond2 = material in materials_formula

    return (cond1 or cond2)


def check_material(material):
    """Check material and raise error if not in xraydb."""

    if not material_in_xraydb(material):
        raise ValueError("Material '%s' is not available in xraydb."
                         % material)
