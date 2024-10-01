# -*- coding: utf-8 -*-
"""Reader class for HDF5 files from BLISS."""

__author__ = "Kevin Pounot, Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "24/10/2022"


import os
from glob import glob
import re
import numpy as np
import time
from tqdm import tqdm
from dateutil.parser import parse
from functools import lru_cache

import json

from silx.io.h5py_utils import File

import fabio

from txs.utils import get_fnames, get_ai, convert_units
from txs.detectors.jungfrau import JungfrauData


_DETECTORS = "rayonix|jungfrau1m|mpx_5x1|mpx_2x1"


def load_images(folder, extension="h5", exclude=None, return_fnames=False,
                verbose=True):
    """Load images in folder.

    Parameters
    ----------
    folder : str
       Folder where images are located.
    extension : str, optional
       File extension of images. Default is 'edf'.
    exclude : list or None, optional
       List of filenames (basenames) that will not be loaded.
       Default is None.
    return_fnames : bool, optional
       If True, a list of images filenames (basenames) is also returned.
       Default is False.

    Returns
    -------
    imgs : list
       Images as returned as a list of numpy arrays.

    """
    if extension == "edf":
        imgs, fnames = load_EDF_images(folder, exclude, verbose)
        if verbose and len(imgs) == 0:
            print("No EDF images in folder: %s" % folder)
    elif extension == 'h5':
        imgs = ImageIteratorHDF5(folder, exclude=exclude)
        fnames = imgs.fnames
        if verbose and len(imgs) == 0:
            print("No HDF5 images in folder: %s" % folder)
    else:
        raise NotImplementedError("NOT IMPLEMENTED YET!")

    if return_fnames:
        return imgs, fnames
    else:
        return imgs


# --- SPEC part ---

def load_EDF_images(folder, exclude=None, verbose=True):
    """Load EDF images in folder.

    Parameters
    ----------
    folder : str
       Folder where images are located.
    exclude : list or None, optional
       List of filenames (basenames) that will not be loaded.
       Default is None.

    Returns
    -------
    imgs : list
       Images as returned as a list of numpy arrays.

    """
    pattern = "*.edf"
    fnames = get_fnames(pattern=pattern, folder=folder)

    if exclude is None:
        exclude = []

    if not isinstance(exclude, (list, np.ndarray)):
        raise TypeError("'exclude' must be None or list.")

    exclude = [os.path.join(folder, f) for f in exclude]
    fnames = [f for f in fnames if f not in exclude]
    imgs = ImageIteratorEDF(fnames, verbose)

    fnames = [os.path.basename(f) for f in fnames]
    return imgs, fnames


class ImageIteratorEDF:
    """
    Class to handle the loading of EDF images and metadata from the SPEC macro
    'waxscollect'.

    The class provides iterator and slicing capabilities to access images.

    Parameters
    ----------
    fnames : list
        List of EDF filenames.


    """

    def __init__(self, fnames, verbose=True):
        if isinstance(fnames, str):
            fnames = [fnames]

        self.fnames = fnames
        self.nimgs = len(fnames)
        self.verbose = verbose

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.nimgs:
            img = fabio.open(self.fnames[self.n]).data
            self.n += 1
            return img
        else:
            raise StopIteration

    def __getitem__(self, slice):
        sel_imgs = self.fnames[slice]
        if isinstance(sel_imgs, str):
            sel_imgs = [sel_imgs]

        if self.verbose:
            # only verbose if multiple images are loaded at once
            if len(sel_imgs) > 1:
                print(
                    "\nLoading %d images from %s ..."
                    % (len(sel_imgs), os.path.abspath(sel_imgs[0]))
                )

        loader = tqdm(sel_imgs) if len(sel_imgs) > 1 else sel_imgs
        imgs = [fabio.open(img).data for img in loader]

        return np.array(imgs).squeeze()

    def __len__(self):
        return len(self.fnames)


def get_info_from_id09_log_file(lines):
    """Get parameters values from ID09 log file comment section.

    Paramters
    ---------
    lines : list
        List of comment lines extracted with readlines.

    Returns
    -------
    pars : dict
        Retrieved parameters (info).

    """

    pars = {}

    pars_lbls = {'mode': ['mode'],
                 'primary_slits': ['primary slits'],
                 'filters': ['filters'],
                 'sblen': ['pulse duration'],
                 'sample_slits': ['sample_slits'],
                 'd': ['detector distance'],
                 'npulses': ['pulses per image'],
                 'time_between_pulses': ['time between pulses'],
                 'wpo': ['waveplate'],
                 'pd1_range': ['pd1 range'],
                 'pd2_range': ['pd2 range'],
                 'pd3_range': ['pd3 range'],
                 'pd4_range': ['pd4 range'],
                 'pd1_dark': ['pd1 dark'],
                 'pd2_dark': ['pd2 dark'],
                 'pd3_dark': ['pd3 dark'],
                 'pd4_dark': ['pd4 dark'],
                 'spindle': ['spindle']}

    for line in lines:
        for k, v_list in pars_lbls.items():
            if any(v in line for v in v_list):
                pars[k] = line.split(":")[-1].strip()

    return pars


def read_id09_log_file(fname, skip=None, format='auto',
                       out_format='datastorage', get_info=False):
    """Read ID09 log file associated to a tr-waxs dataset.

    Parameters
    ----------
    fname : str
        Name of log file or folder. If 'fname' is a folder, the file name
        will be guessed automatically.
    skip : int or tuple or None, optional
        First/last lines to be skipped. Default is None.
    format : str {'waxscollect', 'bliss', 'auto'}, optional
        Log file format. Default is 'waxscollect'.
    out_format : str, optional
        Can be 'ndarray', 'dict' or 'datastorage'. Default is 'datastorage'.
    get_info : boot, optional
        If True, extra info (parameters value) is also returned.
        Default is False.

    Returns
    -------
    data : ndarray or dict or DataStorage
        Retrieved data from id09 log file.
        Use 'out_format' to choose between np.genfromtxt() ndarray or dict.
    info : dict
        Retrieved info from id09 log file comment section. Returned only
        if 'get_info' is True.

    """

    if format == 'waxscollect':
        if os.path.isdir(fname):
            fnames = get_fnames("*.log", folder=fname)

            if len(fnames) == 0:
                full_path = os.path.join(os.getcwd(), fname)
                raise Exception("No *.log file found in '%s'." % full_path)

            diagnostics = os.path.join(fname, 'diagnostics.log')
            if diagnostics in fnames:
                fnames.remove(diagnostics)

            fname = fnames[0]

            if len(fnames) > 1:
                print("WARNING: found more that one *.log that is " +
                      "not diagnostics.log\nUsing: %s" % fname)

        if not os.path.exists(fname):
            raise Exception("'%s' does not exist." % fname)

        # read whole file content
        with open(fname, 'r') as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]

        # find last line starting with '#'
        for iline, line in enumerate(lines):
            if line.lstrip()[0] != '#':
                break
        if iline == 0:
            raise Exception("No comment lines. " +
                            "Does not seem a waxscollect log file.")

        # extract info from comments
        if get_info:
            info = get_info_from_id09_log_file(lines[:iline-1])

        # extract names from last commented line
        names = lines[iline-1][1:].split()

        # read data only (ndarray)
        # NOTE: if the file is read while the last row is written an error will
        #       be raised as the number of columns in last row will be less than
        #       in previous
        try:
            data = np.genfromtxt(
                fname, skip_header=iline, names=names, dtype=None,
                encoding=None, converters=None, excludelist=[]
            )
        except ValueError:
            time.sleep(0.03)
            data = np.genfromtxt(
                fname, skip_header=iline, names=names, dtype=None,
                encoding=None, converters=None, excludelist=[]
            )

        # skip first/last lines
        if skip is not None:
            if isinstance(skip, int):
                data = data[skip:]
            elif isinstance(skip, tuple):
                data = data[skip[0]:skip[1]]
            else:
                raise TypeError("'skip' must be int, tuple or None.")

        # strip '_' from each 'data.dtype.names'
        data.dtype.names = [name.strip('_') for name in data.dtype.names]

        if not isinstance(out_format, str):
            raise TypeError("'out_format' must be str.")

        if out_format.lower() not in ['ndarray', 'dict', 'datastorage']:
            raise ValueError("'out_format' must be 'ndarray', 'dict' or " +
                             "'datastorage'.")

        if out_format.lower() == 'ndarray':
            if get_info:
                return data, info
            else:
                return data
        else:
            # convert data to dictionary
            data = dict((name, data[name]) for name in data.dtype.names)
            data["log_fname"] = fname
            if get_info:
                return data, info
            else:
                return data

    elif format == 'bliss':
        scan = ImageIteratorHDF5(fname)
        return scan.metadata

    elif format == 'auto':
        path = os.path.abspath(fname)
        if os.path.isdir(path):
            edf_files = glob(path + "/*.edf")
            if len(edf_files) == 0:
                return read_id09_log_file(
                    fname, skip, 'bliss', out_format, get_info
                )
            else:
                return read_id09_log_file(
                    fname, skip, 'waxscollect', out_format, get_info
                )
        else:
            raise Exception(
                "'fname' should be a directory with 'auto' format option."
            )

    else:
        raise ValueError(
            "The `format` argument for the log file is not valid.\n"
            "It should be either 'waxscollect' or 'bliss'."
        )


# --- BLISS part ---
class BlissDataset:
    """Class to handle 'datasets' created by BLISS.

    This is intended to handle simultaneously the HDF5 file in a 'Dataset'
    folder and the associated HDF5 files of the corresponding scans.

    Metadata are gathered mainly from the dataset HDF5 file, while images
    are loaded directly from the scans HDF5 files.

    Parameters
    ----------
    fname : str
        Name of the HDF5 file corresponding to the dataset.
    detector : str
        The name of the detector in the HDF5 file.
    counters : 'all', list of str or None, optional
        Additional counters to be read along with the images.

    """
    def __init__(self, fname, detector='auto', counters=None):

        self.fname = os.path.abspath(fname)
        self.detector = detector
        self.counters = counters

        with File(fname, 'r') as data:
            if detector == 'auto':
                self.detector = _find_detector(data)

    @property
    def scans(self):
        with File(self.fname, 'r') as data:
            scans = sorted(
                [key for key in data.keys()],
                key=lambda x: float(x)
            )

            return scans

    @property
    def nscans(self):
        return len(self.scans)

    def __iter__(self):
        self.n = 1
        return self

    def __next__(self):
        if self.n <= self.nscans:
            folder = self._get_scan_paths(self.n)
            data = ImageIteratorHDF5(
                folder, 
                detector=self.detector, 
                counters=self.counters,
                dataset_file=self.fname,
            )
            self.n += 1
            return data
        else:
            raise StopIteration

    @lru_cache
    def __getitem__(self, scan_number):
        """Return the images corresponding to the selected datasets."""
        if isinstance(scan_number, int):
            if scan_number >= 0:
                scan_number = int(max(1, scan_number) - 1)

            folder = self._get_scan_paths(scan_number)
            return ImageIteratorHDF5(
                folder,
                detector=self.detector,
                counters=self.counters,
                dataset_file=self.fname,
            )

        if isinstance(scan_number, slice):
            scan_number = np.arange(
                scan_number.start if scan_number.start is not None else 1,
                scan_number.stop
                if scan_number.stop is not None else self.nscans,
            )

        if isinstance(scan_number, str):
            folder = self._get_scan_paths(scan_number)
            return ImageIteratorHDF5(
                folder, 
                detector=self.detector, 
                counters=self.counters,
                dataset_file=self.fname,
            )

        out = []
        for idx in scan_number:
            if idx >= 0:
                idx = int(max(1, idx) - 1)

            folder = self._get_scan_paths(idx)
            ii = ImageIteratorHDF5(
                folder, 
                detector=self.detector, 
                counters=self.counters,
                dataset_file=self.fname,
            )
            out.append(ii)

        return out

    @classmethod
    def from_scan_folder(cls, folder, detector='auto', counters=None):
        """Returns a `BlissDataset` instance and an iterator on the scan.

        Parameters
        ----------
        folder : str
            The folder containing the data of the BLISS `scan`.
        detector : str, optional
            The detector to be used.
            (default, 'auto')
        counters : list of str
            Additional counters to be read with the images.

        """
        folder = os.path.abspath(folder)
        dset_folder = os.path.dirname(folder.rstrip('/'))
        dset_file = dset_folder + f'/{dset_folder.split("/")[-1]}.h5'

        dset = cls(dset_file, detector, counters)
        scan_idx = dset.get_scan_from_folder(folder)

        return dset, dset[scan_idx]

    def get_scan_from_folder(self, folder):
        """Return the scan number corresponding to the folder."""
        scan_folders = self._get_scan_paths()

        folder = os.path.abspath(folder)
        for key, val in scan_folders.items():
            if folder in val:
                return key

    def get_counters(self, scan_number):
        """Returns the values of the counters corresponding to the scan."""
        if isinstance(scan_number, int):
            base = f"{self.scans[scan_number - 1]}/measurement"
        elif isinstance(scan_number, str):
            base = f"{scan_number}/measurement"
        else:
            raise ValueError(
                "The argument `scan_number` could not be understand.\n"
                "It should be either of type int or str."
            )

        counters = self.counters
        if counters is None:
            counters = []

        with File(self.fname, 'r') as data:
            if self.counters == 'all':
                counters = [
                    val for val in data[f"{base}"] if val != self.detector
                ]

            out = {
                counter: data[f"{base}/{counter}"][()] for counter in counters
                if counter in data[f"{base}"].keys()
            }

        return out

    def _get_arborescence(self):
        dirname = os.path.dirname(self.fname)
        red_path, dset_id = os.path.split(dirname)
        red_path, sample_id = os.path.split(red_path)
        exp_root, _ = os.path.split(red_path)
        
        raw = "RAW_DATA"
        if not os.path.exists(
            f"{exp_root}/{raw}/{sample_id}/{dset_id}"
        ):
            exp_root = red_path
            raw = ""
        
        return exp_root, raw, sample_id, dset_id

    def _get_scan_paths(self, idx=None):
        """Return the list of the absolute path of each scan."""
        exp_root, raw, sample_id, dset_id = self._get_arborescence()

        path = {}
        for scan in self.scans:
            path[scan] = ''
            with File(self.fname, 'r') as data:
                if "measurement" in data[f"{scan}"]:
                    if self.detector in data[f"{scan}/measurement"].keys():
                        scan_number = int(scan.split('.')[0])
                        scan_path = (f"{exp_root}/{raw}/{sample_id}/{dset_id}/"
                                    f"scan{scan_number:04}")
                        scan_folder = glob(scan_path)

                        if len(scan_folder) == 1:
                            path[scan] = os.path.abspath(scan_folder[0])

        if idx is not None:
            if isinstance(idx, int):
                if self.scans[idx] not in path.keys():
                    raise KeyError(
                        f"No images or folder can be found for scan "
                        f"{self.scans[idx]}.\n"
                        f"Verify that the folder "
                        f"'scan{int(self.scans[idx].split('.')[0]):04}' exists "
                        f"in the dataset folder."
                    )

                path = path[self.scans[idx]]

            elif isinstance(idx, str):
                path = path[idx]

            else:
                raise TypeError(
                    "`idx` must be int, str or None."
                )

        return path

    def __len__(self):
        return len(self.scans)

    def metadata(self, scan_number=1, subscan=1):
        """Return useful metadata for data reduction and analysis.

        If multiple files are present, the `idx` argument allows
        access to the corresponding file metadata (default is 0).

        Parameters
        ----------
        scan_number : str or int
            If string, should be in the format "<scan>.<subscan>".
        subscan : int
            Used only if scan_number is an integer.


        """
        out = {}

        # metadata from dataset
        if isinstance(scan_number, str):
            base = scan_number
        else:
            base = f"{scan_number}.{subscan}"

        with File(self.fname, 'r') as data:
            elapsed_time = data[f"{base}/measurement/elapsed_time"][()]
            epoch = data[f"{base}/measurement/epoch"][()]

            date = None
            time = None
            if 'start_time' in data[f"{base}"]:
                start_time = data[f"{base}/start_time"][()]
                datetime = parse(start_time)
                date = datetime.date().strftime("%d-%b-%y")
                time = datetime.time().strftime("%H:%M:%S")

            out.update({
                "date": date,
                "time": time,
                "elapsed_time": elapsed_time,
                "epoch": epoch,
                "log_fname": os.path.abspath(self.fname),
            })

            # additional metadata that could not be there
            if 'sample' in data[f"{base}"]:
                name = data[f"{base}/sample/name"][()]
                out.update(name=name)

            if 'positioners' in data[f"{base}/instrument"]:
                positions = {
                    key: val[()] for key, val
                    in data[f"{base}/instrument/positioners"].items()
                }
                out.update(**positions)

            if 'machine' in data[f"{base}/instrument"]:
                filling_mode = data[
                    f"{base}/instrument/machine/filling_mode"
                ][()]
                out.update(filling_mode=filling_mode)

            if 'srcur' in data[f"{base}/measurement"]:
                srcur = data[
                    f"{base}/measurement/srcur"
                ][()]
                out.update(srcur=srcur.squeeze())

            if 'sbcur' in data[f"{base}/measurement"]:
                sbcur = data[
                    f"{base}/measurement/sbcur"
                ][()]
                out.update(sbcur=sbcur.squeeze())

            if 'pd2ic' in data[f"{base}/measurement"]:
                pd2ic = data[
                    f"{base}/measurement/pd2ic"
                ][()]
                out.update(pd2ic=pd2ic.squeeze())

            # celine : below is a temporary patch to read lxt starting pos 
            #          saved for the moment as user metadata 
            #          when lxt is not scanned

            #if 'lxt_start_pos' in data[f'{base}/instrument/laser_timing'].keys():
            #    out.update(
            #        delay=data[f'{base}/instrument/laser_timing/lxt_start_pos'][()]
            #    )


            if 'lxt_ps' in data[f'{base}/instrument/positioners'].keys():
                out.update(
                    delay=data[f'{base}/instrument/positioners/lxt_ps'][()]
                )

            if 'lxt_ns' in data[f'{base}/instrument/positioners'].keys():
                out.update(
                    delay=data[f'{base}/instrument/positioners/lxt_ns'][()]
                )

            if 'lxt' in data[f'{base}/instrument/positioners'].keys():
                out.update(
                    delay=data[f'{base}/instrument/positioners/lxt'][()]
                )

            if 'scan' in data[f"{base}/instrument/"].keys():
                out['scan'] = dict(
                    motors=data[f"{base}/instrument/scan/motors"][()],
                    counters=data[f"{base}/instrument/scan/counters"][()]
                )

            det_base = f"{base}/instrument/{self.detector}"
            keys = [
                "sensor_material",
                "sensor_thickness",
                "sensor_density",
                "x_pixel_size",
                "y_pixel_size",
            ]
            for key in keys:
                if key in data[f"{det_base}"].keys():
                    out.update({key: data[f"{det_base}/{key}"][()]})
                    if 'units' in data[f"{det_base}/{key}"].attrs.keys():
                        out.update({
                            f"{key}_units":
                            data[f"{det_base}/{key}"].attrs['units']
                        })

        exp_root, raw, sample_id, dset_id = self._get_arborescence()
        proc_path = f"{exp_root}/PROCESSED_DATA/{sample_id}/{dset_id}"
        proc_dset = f"{proc_path}/{dset_id}_oda.h5"
        if os.path.exists(proc_dset):
            with File(proc_dset, 'r') as data:
                if f'{base}' in data.keys():
                    if 'rayonix_integrate' in data[f'{base}'].keys():
                        pyfai_config = data[
                            f"{base}/rayonix_integrate/configuration/data"
                        ][()]
                        pyfai_config = json.loads(pyfai_config.decode('utf8'))
                        for key in ['center', 'binning', 'dist', 'energy']:
                            if key in pyfai_config:
                                out[key] = pyfai_config[key]

        return out

    def filter(self, **conditions):
        """Filter the scans based on the given conditions

        Parameters
        ----------
        conditions : keyword arguments
            Conditions based on the metadata or the images.
            Should in the form of a callable that takes
            a single argument, the value of the metadata or the
            images.

        Returns
        -------
        sample : :py:class:`Sample`
            An instance of the :py:class:`Sample` class which contains
            the scans that passed the condition(s).

        Examples
        --------
        >>> sample = Sample('my_file.h5')
        >>> filt_sample = sample.filter(
        ...     positions=lambda val: val['gony'] > 0.5,
        ...     positions=lambda val: val['gonz'] < 1,
        ...     images=lambda val: np.mean(val) > 1000
        ... )

        """
        raise NotImplementedError


class ImageIteratorHDF5:
    """A class to handle HDF5 files corresponding to a single BLISS scan.

    This does not provide live monitoring yet (retry from silx for instance).
    That is, if a file is still being written by BLISS, the images and
    c unters will not be available and the iterator will stop at the 
    frame of the last closed file. #20221120

    However, the list of available images is updated each time the iterator is
    called or each time a slice is requested such that the class does not
    need to be re-instanciated.

    """

    def __init__(
            self,
            folder,
            scan='',
            detector='rayonix',
            counters=None,
            exclude=None,
            dataset_file=None,
            verbose=False,
    ):
        """Instantiate the class.

        Parameters
        ----------
        folder : str
            The folder where file(s) are to be opened and read.
        scan : str, optional
            The scan and subscan numbers as it appears in the dataset HDF5 file.
        detector : str, optional
            The name of the detector in the HDF5 file.
        counters : list of str, optional
            Additional counters to be read along with the images.
        exclude : list of str, optional
            List of files to be excluded from the iterator.

        """
        self.detector = detector
        self.folder = os.path.abspath(folder)
        self.scan = scan
        self.counters = counters
        self.exclude = list(exclude) if exclude is not None else []
        self.verbose = verbose

        self.dataset_file = dataset_file
        if dataset_file is None:
            # assumes the arborescence in 'RAW_SCANS'
            dset_folder = os.path.dirname(self.folder.rstrip('/'))
            dset_file = dset_folder + f'/{os.path.split(dset_folder)[-1]}.h5'
            self.dataset_file = dset_file

        self._chunk_size = None
        self._load_frames()
        if len(self.fnames) == 0 and self.verbose:
            print(
                f"WARNING: no images found yet in folder: {folder}.\n"
                f"Either no image files has been finished being written yet "
                f"or the folder path is not correct.\n"
            )

        self._shape = (0, 0, 0)

    def _load_frames(self):
        """Update the list of available frames"""

        folder_files = sorted(
            glob(self.folder + f"/*{self.detector}*.h5")
        )
        # Cut the list of files at the first missing file in the serie
        available_files = []
        for index, fname in enumerate(folder_files):
            match = re.match(r".*_(?P<index>\d+).h5$", fname)
            if match is None or int(match.group("index")) != index:
                break
            available_files.append(fname)

        fnames = [os.path.abspath(fname) for fname in available_files]

        # first call, check the image files to find the chunk size and
        # possibly the detector
        if self._chunk_size is None:
            for fname in fnames:
                try:
                    with File(fname, 'r') as data:
                        if 'creator' in data.attrs.keys():
                            if 'LIMA' in data.attrs['creator']:
                                self._chunk_size = data[
                                    'entry_0000/measurement/data'
                                ].shape[0]

                                if self.detector == 'auto':
                                    self.detector = _find_detector(data)

                                break  # break at first image file found

                        self.exclude.append(fname)

                except OSError:
                    # assumes no file is finished to be written
                    # (still locked).
                    pass

        # check if the last file is done being recorded.
        try:
            with File(fnames[-1], 'r') as data:
                pass
        except Exception:
            # assumes the file is not finished to be written (still locked).
            fnames = fnames[:-1]
            pass

        self._available_fnames = [fname for fname in fnames if fname not in self.exclude]

    @property
    def fnames(self):
        return self._available_fnames

    @property
    def shapes(self):
        fnames = self.fnames
        if len(fnames) > 0:
            with File(fnames[0], 'r') as data:
                shape = data['entry_0000/measurement/data'].shape

            with File(fnames[-1], 'r') as data:
                last_shape = data['entry_0000/measurement/data'].shape
        else:
            shape = self._shape
            last_shape = (0, 0, 0)

        self._shape = shape

        shapes = (len(fnames) - 1) * [shape] + [last_shape]

        return np.array(shapes)

    @property
    def nfiles(self):
        return len(self.fnames)

    @property
    def nimgs(self):
        return int(np.sum(self.shapes[:, 0]))

    @property
    def _last_first_index(self):
        last = np.cumsum(self.shapes[:, 0])
        first = np.insert(last, 0, 0)[:-1]

        return (last, first)

    @property
    @lru_cache
    def metadata(self):
        dset = BlissDataset(self.dataset_file, self.detector, self.counters)
        scan_idx = dset.get_scan_from_folder(self.folder)

        return dset.metadata(scan_idx)

    def __iter__(self):
        self.n = 0
        # snapshot of the images and fnames at the beginning of the iteration.
        self._fnames = self.fnames
        self._nimgs = self.nimgs
        self._stream = None

        return self

    def __next__(self):
        if self.n < self._nimgs:
            fidx = int(self.n / self._chunk_size)
            img_idx = int(self.n % self._chunk_size)

            # open a stream for the next chunk of images.
            if img_idx == 0:
                if self._stream is not None:
                    self._stream.close()
                self._stream = File(self._fnames[fidx], 'r')

            img = self._stream["entry_0000/measurement/data"][img_idx]

            if self.counters is None:
                out = np.atleast_2d(img.squeeze())
            else:
                out = {self.detector: img, **self._get_counters(self.n)}

            self.n += 1
            return out

        else:
            self._stream.close()
            raise StopIteration

    def __getitem__(self, slice):
        """Return the images corresponding to the selected files."""
        fnames, _, indices = self._get_imgs_fnames(slice, True)

        imgs = []
        counters = []
        for idx, fname in enumerate(fnames):
            with File(fname, 'r') as data:
                imgs.append(data["entry_0000/measurement/data"][indices[idx]])

        imgs = np.concatenate(imgs).squeeze()
        # BELOW LINES are not used anymore (to be removed):
        # out_counters = {}
        # for key in counters[0].keys():
        #     out_counters[key] = np.concatenate(
        #         [val[key] for val in counters]
        #     ).squeeze()
        
        if self.counters is None:
            return imgs
        else:
            counters = self._get_counters(slice)
            return {self.detector: imgs, **counters}

    def __len__(self):
        return self.nimgs

    def _get_counters(self, frames):
        """Reads the selected counters in an open HDF5 file."""
        counters = {}
        dset = BlissDataset(self.dataset_file, self.detector, self.counters)
        scan_idx = dset.get_scan_from_folder(self.folder)
        counters = dset.get_counters(scan_idx)

        counters = {
            key: val[frames]
            for key, val in counters.items()
        }

        return counters

    def _get_imgs_fnames(self, imgs, return_indices=True):
        """Returns the file names corresponding to the images.

        Parameters
        ----------
        imgs : int, list of int or slice
            The imgs to be selected.
        return_indices : bool, optional
            If True, returns the indices for each file in `self.fnames`
            that corresponds to the selected imgs.
            (default, True)

        Returns
        -------
        fnames : list of str
            The names of the files corresponding to the selected imgs.

        """
        if len(self.fnames) == 0:
            return ([], [], []) if return_indices else []

        if isinstance(imgs, slice):
            imgs = np.arange(
                imgs.start if imgs.start is not None else 0,
                imgs.stop if imgs.stop is not None else self.nimgs,
            )

        fnames = []
        indices1 = []
        indices2 = []
        last_idx, first_idx = self._last_first_index

        # determine where to start and where to stop for faster iteration
        # (concerns iteration on last_idx and first_idx)
        if isinstance(imgs, int):
            start_idx = int(imgs / self._chunk_size)
            stop_idx = start_idx + 1
        else:
            first_img = min(sorted(imgs))
            last_img = max(sorted(imgs))
            start_idx = int(first_img / self._chunk_size)
            stop_idx = int(last_img / self._chunk_size) + 1

        for idx, val in enumerate(last_idx[start_idx:stop_idx]):
            idx += start_idx
            if idx == stop_idx:
                break

            imgs_range = np.arange(first_idx[idx], val)
            ids, ids1, ids2 = np.intersect1d(
                imgs, imgs_range, return_indices=True
            )
            if len(ids) > 0:
                indices1.append(ids1)
                indices2.append(ids2)
                fnames.append(self.fnames[idx])

        if return_indices:
            return fnames, indices1, indices2
        else:
            return fnames

    def get_ai(self):
        """Generate an `AzimuthalIntegrator` object from the metadata."""
        meta = self.metadata
        try:
            energy = meta["energy"]
            energy_units = 'keV'
            center_x, center_y = meta["center"]
            pixel_x = meta["x_pixel_size"]
            pixel_x_units = meta["x_pixel_size_units"]
            pixel_y = meta["y_pixel_size"]
            pixel_y_units = meta["y_pixel_size_units"]
            distance = meta["dist"]
            distance_units = "m"
            binning = meta["binning"]
        except KeyError:
            print(
                "The metadata do not contain the necessary "
                "information to build the `AzimuthalIntegrator` automatically."
            )
            return

        ai = get_ai(
            convert_units(energy, energy_units, 'eV'),
            convert_units(distance, distance_units, 'm'),
            (center_x, center_y),
            (
                convert_units(pixel_x, pixel_x_units, 'm'),
                convert_units(pixel_y, pixel_y_units, 'm'),
            ),
            self.detector,
            binning,
        )

        return ai


# helper function for the different classes in this file
def _find_detector(stream):
    """Try to identify the detector used.

    Parameters
    ----------
    stream : :py:class:`silx.io.h5py_utils.File`
        An opened HDF5 file stream.

    """
    def det_finder(key):
        return re.search(_DETECTORS, key)

    detector = stream.visit(det_finder)
    if detector is not None:
        detector = detector.group()

    if detector is None:
        raise ValueError(
            "The detector could not be detected automatically.\n"
            "Either there are no images in the data set or "
            "a non-registered detector was used.\n"
            "Please provide a detector name as it appears in the "
            "BLISS HDF5 file.\n"
        )

    return detector
