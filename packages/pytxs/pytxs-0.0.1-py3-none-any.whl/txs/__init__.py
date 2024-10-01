# -*- coding: utf-8 -*-
"""..."""

__author__ = "Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "01/09/2021"

import xraydb as _xraydb


def _init_xraydb():
    """Add extra materials to xraydb user config file"""
    extra_materials = (  # name, formula, density, category
        ("gallium nitride", "GaN", 6.15, "semiconductor"),
        ("epoxy", "C21H25ClO5", 1.2, "polymer"),
        ("zirconium", "Zr", 6.52, "metal"),
        ("gadox", "Gd2O2S", 4.3, "scintllator"),
    )

    for name, formula, density, category in extra_materials:
        material = _xraydb.find_material(name)
        if (
            material is None
            or material.formula != formula
            or material.density != density
            or category not in material.categories
        ):
            _xraydb.add_material(name, formula, density, [category])


_init_xraydb()


from . import utils
from . import azav
from . import datared
from . import live
from . import corr
from . import plot
from . import heating
from .common import *
from .datasets import load_images, BlissDataset
from .azav import integrate1d_dataset as int1d_dset
from .datared import datared as dred
from .live import ana
from .corr import get_density, get_mu
from .plot import *
from .utils import get_ai

from . import _version
__version__ = _version.get_versions()['version']
