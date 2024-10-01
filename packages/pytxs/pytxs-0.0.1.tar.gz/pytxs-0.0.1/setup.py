__author__ = "Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "01/01/2021"


import versioneer
from setuptools import setup


setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
