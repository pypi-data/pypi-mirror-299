# -*- coding: utf-8 -*-
"""Utilities functions for trx."""

__author__ = "Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "01/09/2021"


import os
import re
import glob
import time
import numpy as np
import h5py
import fabio

from tqdm import tqdm
from shutil import copy
from collections import namedtuple

from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pyFAI.detectors import RayonixMx170
from pyFAI.detectors import Maxipix2x2
from pyFAI.detectors import Maxipix5x1

try:
    from pyFAI.detectors import Jungfrau1M
except ImportError:
    from pyFAI.detectors import Eiger
    class Jungfrau1M(Eiger):
        MAX_SHAPE = (1064, 1032)
        aliases = ["Jungfrau 1M"]
    # from pyFAI.detectors import Eiger1M as Jungfrau1M
    # print("WARNING:Jungfrau1M not available among pyFAI.detectors")

from txs.common import en_to_wl


RayonixMx170.aliases = ['Rayonix MX170-HS', 'Rayonix MX170', 'RayonixMX170HS',
                        'RayonixMX170']
Maxipix2x2.aliases = ['Maxipix 2x2', 'Maxipix2x2']
Maxipix5x1.aliases = ['Maxipix 5x1', 'Maxipix5x1']


DETECTORS = {
    'rayonix': RayonixMx170(),
    'maxipix5x1': Maxipix5x1(),
    'maxipix2x1': Maxipix2x2(),
    'jungfrau1m': Jungfrau1M()
}



si = {-15: {'multiplier': 1e15, 'prefix': 'fs'},
      -14: {'multiplier': 1e15, 'prefix': 'fs'},
      -13: {'multiplier': 1e15, 'prefix': 'fs'},
      -12: {'multiplier': 1e12, 'prefix': 'ps'},
      -11: {'multiplier': 1e12, 'prefix': 'ps'},
      -10: {'multiplier': 1e12, 'prefix': 'ps'},
      -9: {'multiplier': 1e9, 'prefix': 'ns'},
      -8: {'multiplier': 1e9, 'prefix': 'ns'},
      -7: {'multiplier': 1e9, 'prefix': 'ns'},
      -6: {'multiplier': 1e6, 'prefix': 'us'},
      -5: {'multiplier': 1e6, 'prefix': 'us'},
      -4: {'multiplier': 1e6, 'prefix': 'us'},
      -3: {'multiplier': 1e3, 'prefix': 'ms'},
      -2: {'multiplier': 1e3, 'prefix': 'ms'},
      -1: {'multiplier': 1e3, 'prefix': 'ms'},
      0: {'multiplier': 1, 'prefix': 's'},
      1: {'multiplier': 1, 'prefix': 's'},
      2: {'multiplier': 1, 'prefix': 's'},
      3: {'multiplier': 1, 'prefix': 's'},
      4: {'multiplier': 1, 'prefix': 's'},
     }

# TO DO: add very long delays (min, hours, ...)

def get_ai(energy, distance, center, pixel=None, detector=None, binning=None):
    """Initialize pyFAI azimuthal integrator obj.

    Parameters
    ----------
    energy : float
        X-ray photon energy (eV). 
    distance : float
        Sample-to-detector distance (m).
    center : tuple
        Coordinates of the image center (hor, ver) (pixel).
    pixel : float or tuple or None, optional
        Pixel size (m). If tuple, first value is the horizontal pizel size
        and second value is the vertical pixel size. Default is None.
    detector : str or None, optional
        Detector nickname. Default is None.
    binning : tuple or None, optional
        Detector binning (hor, ver). Default is None.

    Returns
    -------
    pyfai_ai : pyFAI azimuthal integrator obj
        pyFAI ai

    Examples
    --------
    >>> ai = get_ai(18e3, 0.05, detector='rayonix', binning=(2, 2))

    """

    if detector is not None:
        if detector.lower() in DETECTORS.keys():
            detector = DETECTORS[detector.lower()]
        else:
            raise ValueError("'%s' not among ID09 detectors.\n" % detector +
                             "Available detectors are: %s" % DETECTORS.keys())
        pixel1 = pixel2 = None
        if binning is not None:
            detector.set_binning(binning)
        elif pixel is not None:
            detector_binnings = list(detector.BINNED_PIXEL_SIZE.values())
            if not isinstance(pixel, (tuple, list, np.ndarray)):
                k = np.argmin(np.abs(np.array(detector_binnings)-pixel))
            else:
                pixel_ave = 0.5*(pixel[0]+pixel[1])
                k = np.argmin(np.abs(np.array(detector_binnings)-pixel_ave))
            detector.set_binning((k+1, k+1))
        else:
            raise Exception("If 'detector' is not None, either 'pixel' or " +
                            "'binning' must be not None.")
    elif pixel is not None:
        if isinstance(pixel, (tuple, list)):
            if len(pixel) != 2:
                raise ValueError("'pixel' must have len=2 if tuple or list.")
            else:
                pixel1, pixel2 = pixel[0], pixel[1]
        elif not isinstance(pixel, (int, float)):
            raise TypeError("'pixel' must be scalar, tuple or list.")
        else:
            pixel1 = pixel2 = pixel
    else:
        raise ValueError("'pixel' and 'detector' cannot be both None.")

    if not isinstance(center, (tuple, list)):
        raise TypeError("'center' must be tuple or list.")
    elif len(center) != 2:
        raise ValueError("'center' must have length=2.")

    wavelength = en_to_wl(energy)

    pyfai_ai = AzimuthalIntegrator(pixel1=pixel1, pixel2=pixel2,
                                   detector=detector, wavelength=wavelength)

    pyfai_ai.setFit2D(centerX=float(center[0]), centerY=float(center[1]),
                      directDist=distance*1e3)

    # add properties and methods
    Fit2D = pyfai_ai.getFit2D()
    pyfai_ai.center = (Fit2D['centerX'], Fit2D['centerY'])
    pyfai_ai.tilt = (Fit2D['tilt'], Fit2D['tiltPlanRotation'])
    pyfai_ai.energy = energy/1e3

    def as_dict(self):
        """Convert pyFAI azimuthal intagrator obj to dictionary."""
        methods = dir(self)
        methods = [m for m in methods if m.find("get_") == 0]
        names = [m[4:] for m in methods]
        values = [getattr(self, m)() for m in methods]
        ret = dict(zip(names, values))
        ret["detector"] = self.detector.get_name()
        ret["center"] = self.center
        ret["energy"] = self.energy
        ret['binning'] = self.detector.binning
        return ret

    def as_str(self):
        """Convert pyFAI azimuthal intagrator obj to str."""
        det = self.detector.name
        spline = self.spline
        if spline is None:
            spline = "None"
        px = (self.pixel1, self.pixel2)
        dist = self.dist
        wl = self.wavelength
        en = self.energy
        # poni1, poni2 = self.poni1, self.poni2
        rot1, rot2, rot3 = self.rot1, self.rot2, self.rot3
        cpx = self.center
        cmm = (cpx[0]*px[0]*1e3, cpx[1]*px[1]*1e3)
        tilt, tpr = self.tilt[0], self.tilt[1]
        s = ["# Detector         : %s" % det,
             "# Spline           : %s" % spline,
             "# Binning          : %dx%d" % self.detector.binning,
             "# Pixel      [um]  : (%.2f, %.2f)" % (px[0]*1e6, px[1]*1e6),
             "# Distance   [mm]  : %.3f" % (dist*1e3),
             "# Center     [px]  : (%.2f, %.2f)" % (cpx[0], cpx[1]),
             "# Center     [mm]  : (%.3f, %.3f)" % (cmm[0], cmm[1]),
             "# Wavelength [A]   : %.5f" % (wl*1e10),
             "# Energy     [keV] : %.3f" % en,
             "# Rotations  [rad] : (%.3f, %.3f, %.3f)" % (rot1, rot2, rot3),
             "# Tilt       [rad] : %.3f" % tilt,
             "# Tilt Plane Rotation [rad] : %.3f" % tpr]
        return "\n".join(s)

    def show(self):
        print(self.as_str())

    import types

    pyfai_ai.as_dict = types.MethodType(as_dict, pyfai_ai)

    pyfai_ai.as_str = types.MethodType(as_str, pyfai_ai)

    pyfai_ai.show = types.MethodType(show, pyfai_ai)

    return pyfai_ai


def get_fnames(pattern, folder="./"):
    """Get sorted list of file names matching a pattern."""
    fnames = glob.glob(os.path.join(folder, pattern))
    fnames.sort()
    return fnames


def load_image(fname):
    """Load image using fabio."""
    img = fabio.open(fname).data
    return img


def load_mask(fname):
    """Load mask using fabio and check if pyFAI compatible."""
    mask = load_image(fname)
    if not all(item in mask for item in (0, 1)):
        print("WARNING: image is not a pyFAI-type mask.")
    return mask


def save_dict_as_hdf5(d, h5fname, h5path='/', create_dataset_args=None,
                      verbose=False):
    """Save dictionary to hdf5 file.

    Strings, scalars and array_like with size <= 2 are saved as attributes.
    Everything else is saved as dataset.
    If sub-dictionaries exist, corresponding sub-groups are created.

    Parameters
    ----------
    d : dict
        Data dictionary.
    h5fname : str
        Output file name.
    h5path : str, optional
        Target path in HDF5 file in which groups are created.
        Default is '/'.
    create_dataset_args : dict or None, optional
        Parameters to pass to `hdf5.create_dataset`. This allows to specify
        filters and compression parameters. Default is None.

    Credits
    -------
    - silx.io.dictdump.dicttoh5
    - M. Cammarata (https://github.com/marcocamma/datastorage)

    Example
    -------
    >> save_dict_as_hdf5(mydict, 'test.h5',
           create_dataset_args={'compression': 'gzip', 'compression_opts': 9))

    """

    if not isinstance(d, dict):
        raise TypeError("'d' must be dict.")

    os.environ["HDF5_USE_FILE_LOCKING"] = "TRUE"

    def fill_h5(d, f, h5path, create_dataset_args):
        """
        Function to fill (even recursively) the hdf5 file from within a
        context manager.
        """

        for k, v in tqdm(d.items()):

            if v is None or (isinstance(v, (dict, tuple)) and not len(v)):
                # create empty group (error with h5py v2.10)
                f[h5path].attrs[k] = h5py.Empty(dtype="f")

            elif isinstance(v, h5py.Empty):
                f[h5path].attrs[k] = h5py.Empty("f")

            elif isinstance(v, dict):
                # recurse
                f.create_group(h5path + k)
                fill_h5(v, f, h5path + k + "/",
                        create_dataset_args=create_dataset_args)

            elif isinstance(v, str):
                f[h5path].attrs[k] = str(v)

            elif isinstance(v, (int, float, np.integer)):
                f[h5path].attrs[k] = v

            elif isinstance(v, (bool, np.bool_)):
                f[h5path].attrs[k] = v

            elif isinstance(v, (list, tuple, np.ndarray)):
                # take care of cases with lists having different lengths
                orig_shapes = []
                try:
                    v_new = np.array(v)
                    if v_new.dtype.kind == 'O':
                        orig_shapes = [val.shape for val in v_new]
                        v = np.concatenate(v_new)

                except ValueError:
                    orig_shapes = [val.shape for val in v]
                    v = [np.ravel(val) for val in v]
                    v = np.concatenate(v)

                if v_new.dtype.kind in ["S", "U"]:
                    v = np.array(v_new, dtype=np.bytes_)

                # if size <= 2, assume it is attribute rather than dataset
                if np.size(v) <= 2:
                    f[h5path].attrs[k] = v
                else:
                    # handle list of strings or numpy array of strings
                    if create_dataset_args is None:
                        f.create_dataset(h5path+k, data=v)
                    else:
                        f.create_dataset(h5path+k, data=v,
                                         **create_dataset_args)

                    f[h5path+k].attrs['orig_shapes'] = orig_shapes

            else:
                print("ERROR: unrecongnized data type for key='%s'" % k)

    t0 = time.time()

    with h5py.File(h5fname, "w", locking=True) as f:
        fill_h5(d, f, h5path, create_dataset_args)

    if verbose:
        print("Saving time: %.3f s" % (time.time() - t0))


def load_hdf5_as_dict(h5fname, h5path='/', verbose=False):
    """Read a HDF5 file and return a nested dictionary.

    Parameters
    ----------
    h5fname : str
        HDF5 file name.
    h5path : str, optional
        Name of HDF5 group to use as dictionary root level.
        Default is '/'.

    Credits
    -------
    - silx.io.dictdump.h5todict

    """

    os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

    ddict = {}

    t0 = time.time()

    with h5py.File(h5fname, mode='r', locking=False) as f:
        for k in f[h5path]:
            if isinstance(f[h5path+k], h5py.Group):
                ddict[k] = load_hdf5_as_dict(h5fname, h5path+k+"/")
            else:
                # convert HDF5 dataset to numpy array
                ddict[k] = f[h5path+k][...]

                # convert to unicode string, int or float if scalar
                if ddict[k].size == 1:
                    if ddict[k].dtype.kind in ['S', 'U']:
                        ddict[k] = ddict[k].astype('unicode').astype(str)
                    elif ddict[k].dtype.kind == 'i':
                        ddict[k] = int(ddict[k])
                    elif ddict[k].dtype.kind == 'f':
                        ddict[k] = float(ddict[k])
                    else:
                        raise Exception("Unrecognized data type for '%s'" % k)

                # convert to array of unicode strings if array of strings
                if ddict[k].dtype.kind == 'S':
                    ddict[k] = ddict[k].astype('unicode').astype(str)

                if "orig_shapes" in f[h5path + k].attrs.keys():
                    if f[h5path + k].attrs['orig_shapes'].size > 0:
                        entry = []
                        start_idx = 0
                        for _, shape in enumerate(
                                f[h5path + k].attrs["orig_shapes"]
                        ):
                            end_idx = np.prod(shape)
                            entry.append(
                                ddict[k][start_idx:end_idx].reshape(shape)
                            )
                        ddict[k] = entry

                # special case
                if k == "filt_res":
                    ddict[k] = [tuple(val) for val in ddict[k]]

        for k, v in f[h5path].attrs.items():
            if isinstance(v, np.ndarray):
                if v.dtype.kind == "S":
                    v = v.astype(str)
                if k == "filt_res":
                    v = [tuple(val) for val in v]
            ddict[k] = v

    if verbose:
        print("Loading time: %.3f s" % (time.time() - t0))

    return ddict


def get_exponent_and_mantissa(f):
    """Get exponent and mantissa from float."""
    if abs(f) < 1e-15:
        exponent = 0
    else:
        exponent = int(np.floor(np.log10(abs(f))))
    mantissa = f*si[exponent]['multiplier']
    return exponent, mantissa


def t2str(delay, digits=None, decimals=None, strip_spaces=True):
    """
    Convert delay from float to str.

    Parameters
    ----------
    delay : float or array-like
        Float delay.
    digits : int or None, optional
        Number of significant digits of the number without units.
    decimals : int or None, optional
        Number of digits after the dot.

    Returns
    -------
    t : str or array_like
        String delay.

    """

    if isinstance(delay, str):
        return delay

    if isinstance(delay, float):
        delay = [delay]

    if not isinstance(delay, (list, tuple, np.ndarray)):
        raise TypeError("'delay' must be float or array-like.")

    if digits is not None and not isinstance(digits, int):
        raise TypeError("'digits' must be int or None.")

    if decimals is not None and not isinstance(decimals, int):
        raise TypeError("'decimals' must be int or None.")

    if digits is not None and digits < 1:
        raise ValueError("'digits' must be > 0")

    t = []

    for k, d in enumerate(delay):

        if isinstance(d, str):
            t.append(d)
            continue

        if abs(d) < 1e-15:
            t.append("0")
            continue

        if d in [9999.999, 9999, 10000]:
            t.append("off")
            continue

        exponent, mantissa = get_exponent_and_mantissa(d)

        if digits is not None:
            mantissa_exponent = np.floor(np.log10(abs(mantissa)))
            mantissa /= 10**mantissa_exponent
            mantissa = np.round(mantissa, digits-1)
            mantissa *= 10**mantissa_exponent

            if abs(mantissa) == 1000:
                exponent += 1
                mantissa = 1 if mantissa > 0 else -1

        if decimals is not None:
            mantissa = np.round(mantissa, decimals)
        
        if (abs(mantissa) - int(abs(mantissa))) == 0:
            # to avoid truncation issues with floats
            mantissa = int(mantissa)

        string = str(mantissa) + " " + si[exponent]["prefix"]

        if strip_spaces:
            string = string.replace(" ", "")

        t.append(string)

    if len(t) == 1:
        t = t[0]

    return t


_t_in_str_regex = re.compile("_(-?\d+\.?\d*(?:ps|ns|us|ms)?)")


def get_delay_from_str(string):
    match = _t_in_str_regex.search(string)
    return match and match.group(1) or None


_t_regex = re.compile("(-?\d+\.?\d*)\s*((?:s|fs|ms|ns|ps|us)?)")


def str2t(delay):
    """
    Convert delay from string to float.

    Parameters
    ----------
    delay : str or array-like
        String delay.

    Returns
    -------
    t : float or array_like
        Float delay.

    """

    if isinstance(delay, str):
        delay = [delay]
        return_array = False
    else:
        return_array = True

    if not isinstance(delay, (list, tuple, np.ndarray)):
        raise TypeError("'delay' must be float or array-like.")

    t2val = dict(fs=1e-15, ps=1e-12, ns=1e-9, us=1e-6, ms=1e-3, s=1)

    t = []

    for k, d in enumerate(delay):

        if isinstance(d, bytes):
            d = d.decode('ascii')

        match = _t_regex.search(d)

        if match:
            n, t0 = float(match.group(1)), match.group(2)
            val = t2val.get(t0, 1)
            t.append(n*val)
        else:
            # unrecognized string will be kept
            t.append(d)

    if not return_array:
        t = t[0]

    return t


def sort_string_delays(delays, digits=None, return_indices=False):
    """Sort string delays in ascending order.

    Parameters
    ----------
    delays : array-like
        Array of strings.
    return_indices : bool
        If True, returns also the indices of the original array arranged 
        according to the new, sorted array.
        Can be used to sort data as well later on.

    Returns
    -------
    sorted_delays : array-like
        Array of strings.
    sorted_indices : array-like
        Array of integer giving th position of the old array elements
        in the new, sorted array.

    Notes
    -----
    - If a string that cannot be converted to float is present (e.g. 'off'),
      it is placed at the beginning of the array.

    """

    delays = str2t(delays)
    num_delays = [d for d in delays if not isinstance(d, str)]
    str_delays = [d for d in delays if isinstance(d, str)]

    sorted_indices = np.argsort(num_delays)
    num_delays = [num_delays[idx] for idx in sorted_indices]
    
    # add possible string delays and update the indices accordingly.
    sorted_indices = np.concatenate((
        np.arange(len(str_delays)),
        sorted_indices + len(str_delays)
    ))

    sorted_delays = t2str(str_delays + num_delays, digits=digits, decimals=1)

    if return_indices:
        return sorted_delays, sorted_indices
    else:
         return sorted_delays


def sim_live_dataset(orig_path, dest_path, sleep_time):

    # check what *.log files are available in 'orig_path'

    fnames = get_fnames("*.log", folder=orig_path)

    if len(fnames) == 0:
        full_path = os.path.join(os.getcwd(), orig_path)
        raise Exception("No *.log file found in '%s'." % full_path)

    diagnostics = os.path.join(orig_path, 'diagnostics.log')
    if diagnostics in fnames:
        fnames.remove(diagnostics)

    orig_logfile = fnames[0]

    if len(fnames) > 1:
        print("WARNING: found more that one *.log that is " +
              "not diagnostics.log\nUsing: %s" % orig_path)

    dest_logfile = os.path.join(dest_path, os.path.basename(orig_logfile))

    filelist = get_fnames("*.edf", folder=orig_path)

    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)

    # empty destination folder:
    for f in os.listdir(dest_path):
        os.remove(os.path.join(dest_path, f))

    # read whole file content
    with open(orig_logfile, 'r') as f:
        lines = f.readlines()

    # find last line starting with '#'
    for iline, line in enumerate(lines):
        if line.lstrip()[0] != '#':
            break
    if iline == 0:
        raise Exception("No comment lines. " +
                        "Does not seem a waxscollect log file.")

    for line in lines[:iline]:
        with open(dest_logfile, 'a') as log:
            log.write(line)

    loglines = lines[iline:]

    for f, line in zip(filelist, loglines):
        with open(dest_logfile, 'a') as log:
            print(line)
            log.write(line)
        time.sleep(sleep_time)
        print(f)
        copy(f, dest_path)


def convert_units(value, unit, target_unit):
    """Converts the value to the given target units.

    The base units used are the SI units.
    
    Parameters
    ----------
    value : float
        The value to be converted.
    unit : str
        The unit the provided value is given into.
        For instance, 'm', 'eV', 'g/L', J/m^2, m.s^(-1), m.s^{-1}, J/m^2/s.
    target_unit : str
        The unit of the value to be returned.
    
    """
    prefixes = {
        'f':1e-15, 
        'p':1e-12, 
        'angs': 1e-10,  # special case for distances
        'n':1e-9, 
        'u':1e-6, 
        'm':1e-3, 
        'c':1e-2,
        'd':1e-1,
        '':1,
        'h':1e2,
        'k':1e3,
        'M':1e6,
        'G':1e9,
        'T':1e12,
        'P':1e15,
    }

    current_singlets = _parse_unit(unit)
    target_singlets = _parse_unit(target_unit)

    for key, val in current_singlets.items():
        curr_scale = prefixes[val['prefix']] ** val['exponent']

        if key not in target_singlets.keys():
            raise KeyError(
                "The current and target units do not seem to correspond."
            )
        
        target = target_singlets[key]
        target_scale = prefixes[target['prefix']] ** target['exponent']

        scale = curr_scale / target_scale

        value = value * scale

    return value


def _parse_unit(unit):
    bases = [
        "angs",
        "mol",
        "rad",
        "cd",
        "eV",
        "Da",
        "ohm",
        "s", 
        "g",
        "A",
        "K",
        "J",
        "Hz",
        "N",
        "Pa",
        "W",
        "V",
        "F",
        "T",
        "L",
        "dB",
    ]

    converters = {
        "rad": "m/m",
        "J": "kg.m^2.s^{-2}",
        "Hz": "s^{-1}",
        "N": "kg.m.s^{-2}",
        "Pa": "kg.m^{-1}.s^{-2}",
        "W": "kg.m^2.s^{-3}",
        "V": "kg.m^2.s^{-3}.A^{-1}",
        "F": "kg^{-1}.m^{-2}.s^4.A^2",
        "ohm": "kg.m^2.s^{-3}.A^{-2}",
        "T": "kg.s^{-2}.A^{-1}",
        "L": "dm^3",
    }

    pattern = re.compile("([a-zA-Z]+)\^?[({]?(-?\d*)[)}]?")

    singlets = {}

    # get the denominators and set the exponent sign to negative
    units = unit.split('/')
    for idx, val in enumerate(units):
        val = val.split(".")
        for sub_idx, single_unit in enumerate(val):
            is_negative = False
            # first element has negative exponent due to the '/'.
            if idx > 0 and sub_idx == 0:
                is_negative = True

            name, exponent = pattern.search(single_unit).groups()

            # process the name, look for a prefix
            if re.match("\w?m$", name):  # a distance
                base_start_idx = name.rfind("m")

            else:
                for base in bases:
                    base_start_idx = name.rfind(base)
                    if base_start_idx != -1:
                        break
            
            if base_start_idx == -1:
                raise ValueError(
                    f"Unit {name} is not recognized.\n"
                    f"Available values (with or without scaling "
                    f"prefix are: {bases}.\n"
            )
            elif base_start_idx == 0:
                prefix = ''
            else:
                prefix = name[:base_start_idx]
                name = name[base_start_idx:]

            if name == 'angs':
                name = 'm'
                prefix = 'angs'

            # process the exponent, if any
            exponent = float(exponent) if exponent != '' else 1.
            if exponent < 0:
                is_negative = not is_negative

            singlets[name] = {
                "prefix": prefix,
                "exponent": -abs(exponent) if is_negative else abs(exponent), 
            }

    return singlets
