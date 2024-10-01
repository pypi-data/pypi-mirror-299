# -*- coding: utf-8 -*-
"""Azimuthal average related functions."""

__author__ = "Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "01/09/2021"


import os
import time
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy import ndimage

from txs.common import tth_to_q, q_to_tth, tth_to_r, r_to_tth
from txs.utils import load_hdf5_as_dict, save_dict_as_hdf5, DETECTORS
from txs.datasets import ImageIteratorEDF, ImageIteratorHDF5, load_images
from txs.corr import get_sensor_info, sensor_absorption, sample_transmission
from txs.corr import get_density


plt.ion()

pyfai_methods = ("numpy", "cython", "bbox", "splitpixel", "lut", "csr",
                 "nosplit_csr", "full_csr", "lut_ocl", "csr_ocl")

CALIBRANTS = ['AgBe']


def get_poni(center, pixel, distance, tilt=0, tilt_plane_rotation=0):
    """
    Get poni1, poni2, rot1, rot2 and rot3.

    Parameters
    ----------
    center: 2D-tuple
        X-ray beam position on detector image (pixel).
    pixel: 2D-tuple
        Detector pixel size (m).
    distance: float
        Sample to detector distance (m).
    tilt: float
        Detector tilt (degrees).
    tilt_plane_rotation: float
        Rotation of the tilt plane around the detector z-axis (degrees)

    """
    cos_tilt = np.cos(np.deg2rad(tilt))
    sin_tilt = np.sin(np.deg2rad(tilt))
    cos_tpr = np.cos(np.deg2rad(tilt_plane_rotation))
    sin_tpr = np.sin(np.deg2rad(tilt_plane_rotation))
    poni1 = center[0] * pixel[0] - distance * sin_tilt * sin_tpr
    poni2 = center[1] * pixel[1] - distance * sin_tilt * cos_tpr
    rot2 = np.arcsin(sin_tilt * sin_tpr)
    val = cos_tilt / np.sqrt(1.0 - (sin_tpr * sin_tilt)**2)
    rot1 = np.arccos(min(1.0, max(-1.0, val)))
    if cos_tpr * sin_tilt > 0:
        rot1 = -rot1
    assert abs(cos_tilt - np.cos(rot1) * np.cos(rot2)) < 1e-6
    if tilt == 0.0:
        rot3 = 0
    else:
        val = cos_tilt * cos_tpr - cos_tpr * sin_tpr
        val /= np.sqrt(10 - sin_tpr**2 * sin_tilt**2)
        rot3 = np.arccos(min(1.0, max(-1.0, val)))

    return {'poni1': poni1, 'poni2': poni2, 'rot1': rot1, 'rot2': rot2,
            'rot3': rot3}


def integrate1d(img, ai, npt=600, method='csr', unit="q_A^-1",
                normalization_factor=1.0, mask=None, dark='auto', flat=None,
                solid_angle=True, polarization_factor=0.99,
                variance=None, error_model=None, radial_range=None,
                azimuthal_range=None, dummy=None, delta_dummy=None,
                safe=True, metadata=None, dezinger_method='mask_zingers',
                dezinger=None, sensor_material=None,
                sensor_thickness=None, sensor_density=None,
                sample_material=None, sample_thickness=None,
                sample_density=None, verbose=False):
    """
    Perform azimuthal integration of an image.

    Parameters
    ----------
    img : 2d ndarray
        Detector Image.
    ai : pyFAI.azimuthalIntegrator.AzimuthalIntegrator obj
        PyFAI azimuthal integrator.
    npt : int, optional
        Number of radial bins (number of points in the output pattern).
        Default is 600.
    method : str, optional
        PyFAI azimuthal integration method.
        Available choices are (pixel splitting | algorithm | implementation):
        "numpy"       : no split     | histogram             | python
        "cython"      : no split     | histogram             | cython
        "BBox"        : bounding box | histogram             | cython
        "splitpixel"  : full         | histogram             | cython
        "lut"         : bounding box | look-up table         | cython
        "csr"         : bounding box | compressed sparse row | cython
        "nosplit_csr" : no split     | compressed sparse row | cython
        "full_csr"    : full         | compressed sparse row | cython
        "lut_ocl"     : bounding box | look-up table         | opencl
        "csr_ocl"     : bounding box | compressed sparse row | opencl
        To specify the device: "csr_ocl_1,2".
        No pixel splitting --> high noise on bins with few pixels.
        Bounding box splitting --> fast, but blurs a bit the signal.
        Pseudo pixel splitting --> compromise between speed and precision.
        Full pixel splitting --> slow, high precision.
        Default is 'csr'.
    unit : str, optional
        Output unit. Can be "q_nm^-1", "q_A^-1", "2th_deg", "2th_rad", "r_mm".
        Default is "q_A^-1".
    normalization_factor : float or None, optional
        Value of a normalization monitor.
    mask : ndarray or None, optional
        Array (same size as image) with 1 for masked pixels, and 0 for valid
        pixels. Default is None.
    dark : ndarray or str or None, optional
        Dark noise image.
        If 'auto' (default) and 'ai.detector' is equal to 'rayonix', the
        constant offset 10 will be removed from 'img'. Otherwise 'dark' is set
        to None.
    flat : ndarray of None, optional
        Flat field image. Default is None.
    solid_angle : bool, optional
        If True (default), correct for solid angle of each pixel.
    polarization_factor : float or None, optional
        Polarization factor between -1 (vertical) and +1 (horizontal).
        0 for circular polarization or random,
        If None, no correction is applied.
        Default is 0.99.
    variance : ndarray or None, optional
        Array containing the variance of the data in 'img'.
        If None (default), no error propagation is done.
    error_model : str or None, optional
        If "poisson": variance = I.
        If "azimuthal": variance = (I-<I>)^2.
        Default is None.
    radial_range : (float, float) or None, optional
        The lower and upper values of the radial unit.
        If None (default), range is simply (img.min(), img.max()) and values
        outside the range are ignored.
    azimuthal_range : (float, float) or None, optional
        The lower and upper values of the azimuthal angle.
        If None (default), range is simply (img.min(), img.max()) and values
        outside the range are ignored.
    dummy : ndarray or None, optional
        Value for dead/masked pixels.
    delta_dummy : ndarray or None, optional
        Precision for dummy value.
    safe : bool, optional
        If True, extra checks are performed to ensure LUT/CSR is valid.
        Default is False.
    metadata : dict or None, optional
        JSON serializable object containing the metadata.
        Default is None.
    dezinger_method : str, optional
        Can be 'medfilt1d' or 'mask_zingers'. Default is 'mask_zingers'.
        Ignored if 'dezinger' is None.
    dezinger : float or tuple or str or None, optional
        - If None (default), no zinger is removed.
        - If 'dezinger_method' is 'medfilt1d':
          Percentile used for removing pixels corresponding to zingers (or
          Bragg peaks) from the amorphous part of the image.
          Percentile=90: 90% of pixels are retained.
          Avoid using percentile>95.
        - If tuple, specifies a region to average out.
        - If str, can be only 'mask_zingers' (currently it is the only
          implemented alternative to the pyFAI medifilt1() method).
        - If 'dezinger_method' is 'mask_zingers':
          Must be len=2 tuple. The first element is the pixel intensity
          threshold used to detect zingers (40e3 is a good default). The
          second element is the radius of the masking circle (5 pixels is
          a good default).
    sensor_material : str or None, optional
        Material of which the detector sensitive area is made of.
        Can be expressed as chemical formula or name from materials
        list available in the python package 'xraydb'.
        If 'auto', the chemical formula and thickness are deduced from
        'ai.detector'.
        Default is None.
    sensor_thickness : float or None, optional
        Thickness of the detector sensitive area (m).
        Default is None.
        If both 'sensor_material' and 'sensor_thickness' are not None,
        the azimuthal averaged intensity is scaled (divided) by the
        (angular dependent) sensor absorption.
    sensor_density : float or None, optional
        Density of the detector sensitive area (kg/m3).
        If None, the density is guessed automatically.
    sample_material : str or None, optional
        Material of which the sample is made of.
        Can be expressed as chemical formula or name from materials
        list available in the python package 'xraydb'.
        Default is None.
    sample_thickness : float or None, optional
        Thickness of the sample (m).
        Default is None.
        If both 'sample_material' and 'sample_thickness' are not None,
        the azimuthal averaged intensity is scaled (divided) by the
        (angular dependent) sample transmission.
    sensor_density : float or None, optional
        Density of the sample (g/cm3).
        If None, the density is guessed automatically.

    Returns
    -------
    res : pyFAI.containers.Integrate1dResult obj
        Result of PyFAI 1D integration. Attributes include "radial" (center
        position of radial bins), "intensity" (azimuthally integrated
        intensities) and "sigma" (errors on intensities).

    Notes
    -----
    - To get main results only, it is possible to use:
          q, i, e = integrate1d(...)
      or even:
          q, i = integrate1d(...)
    - Property 'zingers' add to 'res': could be None or bool.

    """
    if not isinstance(img, np.ndarray):
        raise TypeError("'img' must be a numpy array.")

    if method not in pyfai_methods:
        raise ValueError("'method' must be one of ", pyfai_methods)

    kwargs = {'npt': npt, 'filename': None,
              'correctSolidAngle': solid_angle, 'variance': variance,
              'error_model': error_model, 'radial_range': radial_range,
              'azimuth_range': azimuthal_range, 'mask': mask,
              'dummy': dummy, 'delta_dummy': delta_dummy,
              'polarization_factor': polarization_factor, 'dark': dark,
              'flat': flat, 'method': method, 'unit': unit, 'safe': safe,
              'normalization_factor': normalization_factor,
              'metadata': metadata}

    if dark is not None:
        if isinstance(dark, str) and dark == 'auto':
            if ai.detector == DETECTORS['rayonix']:
                kwargs['dark'] = 10 * np.ones_like(img)
            else:
                kwargs['dark'] = None

    if dezinger is None:

        if mask is None:
            mask = np.zeros_like(img)

        res = ai.integrate1d(img, **kwargs)
        res.mask = mask
        res.zingers = 0

    else:

        if dezinger_method not in ['medfilt1d', 'mask_zingers']:
            raise ValueError("'dezinger_method' must be 'medfilt1d' or " +
                             "'mask_zingers'.")

        if dezinger_method == 'mask_zingers':

            if not isinstance(dezinger, (tuple, list)):
                raise TypeError("'dezinger' must be tuple when " +
                                "'dezinger_method' is 'mask_zingers'")

            zingers_mask = get_mask_zingers(
                img, threshold=dezinger[0], circle_radius=dezinger[1],
                verbose=verbose)

            if mask is not None:
                mask = np.copy(mask | zingers_mask)
            else:
                mask = np.copy(zingers_mask)
            kwargs['mask'] = mask

            res = ai.integrate1d(img, **kwargs)

            res.mask = mask
            res.zingers = zingers_mask.sum()

        if dezinger_method == 'medfilt1d':

            kwargs = {'npt_rad': npt, 'npt_azim': 512,
                      'correctSolidAngle': solid_angle,
                      'mask': mask, 'dummy': dummy, 'delta_dummy': delta_dummy,
                      'polarization_factor': polarization_factor, 'dark': dark,
                      'flat': flat, 'method': 'splitpixel', 'unit': unit,
                      'normalization_factor': normalization_factor,
                      'metadata': metadata, 'percentile': dezinger}

            # Note: for medfilt1d, method="splitpixel" (default) corresponds to
            #       pseudo split | histogram | cython

            res = ai.medfilt1d(img, **kwargs)
            res.mask = mask
            res.zingers = 0

    wl = ai.wavelength

    if res.unit.name in ["q_nm^-1", "q_A^-1"]:
        res.q = np.copy(res.radial)
        q = res.q / res.unit.scale * 1e9
        tth = q_to_tth(q, wl)
        # tth = 2*np.arcsin(wl*q/(4*np.pi))
        res.tth = np.rad2deg(tth)
        # res.r_mm = ai.dist*np.tan(tth)*1e3
        res.r_mm = tth_to_r(tth, ai.dist) * 1e3
    elif res.unit.name in ["2th_deg", "2th_rad"]:
        if res.unit == "2th_rad":
            tth = np.copy(res.radial)
            res.tth = np.rad2deg(tth)
        else:
            res.tth = np.copy(res.radial)
            tth = np.deg2rad(res.tth)
        # res.q = 4*np.pi*np.sin(tth/2)/wl
        res.q = tth_to_q(tth, wl)
        # res.r_mm = ai.dist*np.tan(tth)*1e3
        res.r_mm = tth_to_r(tth, ai.dist) * 1e3
    elif res.unit.name == "r_mm":
        res.r_mm = np.copy(res.radial)
        # tth = np.arctan2(res.r_mm*1e-3/ai.dist)
        tth = r_to_tth(res.r_mm * 1e-3, ai.dist)
        # res.q = 4*np.pi*np.sin(tth/2)/wl
        res.q = tth_to_q(tth, wl)
        res.tth = np.rad2deg(tth)
    else:
        raise ValueError("'unit' must be one of 'q_nm^-1', 'q_A^-1', " +
                         "'2th_deg', '2th_rad', 'r_mm'")

    res.i = np.copy(res.intensity)
    if error_model is not None:
        res.e = np.copy(res.sigma)
    else:
        res.e = None

    res.detector = ai.detector
    res.dark = kwargs['dark']

    if sensor_material == 'auto' and ai.detector is not None:
        sensor_info = get_sensor_info(ai.detector.name)
        sensor_material, sensor_thickness, sensor_density = sensor_info

    if sensor_material is not None and sensor_thickness is not None:

        if sensor_density is None:
            sensor_density = get_density(sensor_material)

        corr = 1 / sensor_absorption(tth=res.tth,
                                     material=sensor_material,
                                     energy=ai.energy * 1e3,
                                     thickness=sensor_thickness,
                                     density=sensor_density)
        res.i *= corr
        if res.e is not None:
            res.e *= corr
        res.sensor_material = sensor_material
        res.sensor_thickness = sensor_thickness
        res.sensor_density = sensor_density
    else:
        res.sensor_material = None
        res.sensor_thickness = None
        res.sensor_density = None

    if sample_material is not None and sample_thickness is not None:

        if sample_density is None:
            sample_density = get_density(sample_material)

        corr = 1 / sample_transmission(tth=res.tth,
                                       material=sample_material,
                                       energy=ai.energy * 1e3,
                                       thickness=sample_thickness)
        res.i *= corr
        if res.e is not None:
            res.e *= corr
        res.sample_material = sample_material
        res.sample_thickness = sample_thickness
        res.sample_density = sample_density
    else:
        res.sample_material = None
        res.sample_thickness = None
        res.sample_density = None

    return res


def integrate1d_multi(imgs, ai, npt=600, method='csr', unit="q_A^-1",
                      normalization_factor=1.0, mask=None, dark='auto',
                      flat=None, solid_angle=True, polarization_factor=0.99,
                      variance=None, error_model=None, radial_range=None,
                      azimuthal_range=None, dummy=None, delta_dummy=None,
                      safe=True, metadata=None, dezinger_method='mask_zingers',
                      dezinger=None, sensor_material=None,
                      sensor_thickness=None, sensor_density=None,
                      sample_material=None, sample_thickness=None,
                      sample_density=None, return_info=False,
                      store_all_masks=False, verbose=True):
    """
    Perform the azimuthal integration of a series of images.

    Parameters
    ----------
    imgs : list or ndarray
        Detector images.
    ai : pyFAI.azimuthalIntegrator.AzimuthalIntegrator obj
        PyFAI azimuthal integrator.
    npt ... dezinger : ...
        See 'integrate1d' docinfo.
    return_info : bool, optional
        If True, all azimuthal average parameters are stored and returned.
    store_all_mask : bool, optional
        If False (default), only the mask applied to the first image is stored.
        If True, a mask is stored for each image. This is useful when
        'dezinger' is not None.

    Returns
    -------
    q : list
        List of q-vectors.
    i : list
        List of intensity vectors.
    e : list
        List of intensity error vectors.
        Returned only if 'error_model' is not None.
    info : dict
        Info on azimuthal average parameters.
        Retured only if 'return_info' is True.

    """

    if imgs is None:
        raise ValueError("'imgs' must be not None.")
    elif not isinstance(
        imgs, (list, np.ndarray, ImageIteratorEDF, ImageIteratorHDF5)
    ):
        raise TypeError("'imgs' must be list or ndarray.")

    kwargs = {'npt': npt, 'method': method, 'unit': unit,
              'normalization_factor': normalization_factor,
              'mask': mask, 'dark': dark, 'flat': flat,
              'solid_angle': solid_angle,
              'polarization_factor': polarization_factor,
              'variance': variance, 'error_model': error_model,
              'radial_range': radial_range, 'azimuthal_range': azimuthal_range,
              'dummy': dummy, 'delta_dummy': delta_dummy,
              'safe': safe, 'metadata': metadata,
              'dezinger_method': dezinger_method, 'dezinger': dezinger,
              'sensor_material': sensor_material,
              'sensor_thickness': sensor_thickness,
              'sample_material': sample_material,
              'sample_thickness': sample_thickness,
              'sample_density': sample_density,
              'verbose': verbose}

    t0 = time.time()

    if verbose:
        print("\nAzimuthally averaging %d images ..." % len(imgs))

    # res = [integrate1d(img, ai, **kwargs) for img in tqdm(imgs)]

    r0 = integrate1d(imgs[0], ai, **kwargs)

    q, i, e = [], [], []
    tth, r_mm, zingers = [], [], []
    masks = []  # masks are treated separately to reduce memory usage
    if not store_all_masks and not error_model:
        for img in tqdm(imgs):
            r = integrate1d(img, ai, **kwargs)
            q.append(r.q)
            i.append(r.i)
            tth.append(r.tth)
            r_mm.append(r.r_mm)
            zingers.append(r.zingers)
    elif not store_all_masks:
        for img in tqdm(imgs):
            r = integrate1d(img, ai, **kwargs)
            q.append(r.q)
            i.append(r.i)
            e.append(r.e)
            tth.append(r.tth)
            r_mm.append(r.r_mm)
            zingers.append(r.zingers)
    elif not error_model:
        for img in tqdm(imgs):
            r = integrate1d(img, ai, **kwargs)
            q.append(r.q)
            i.append(r.i)
            tth.append(r.tth)
            r_mm.append(r.r_mm)
            zingers.append(r.zingers)
            masks.append(r.mask)
    else:
        for img in tqdm(imgs):
            r = integrate1d(img, ai, **kwargs)
            q.append(r.q)
            i.append(r.i)
            e.append(r.e)
            tth.append(r.tth)
            r_mm.append(r.r_mm)
            zingers.append(r.zingers)
            masks.append(r.mask)

    if verbose:
        print("Azimuthal averaging time: %.3f s" % (time.time() - t0))

    if return_info:

        info = kwargs.copy()
        # info['init_mask'] = info.pop('mask')
        info['tth'] = tth
        info['r_mm'] = r_mm
        if store_all_masks:
            info['masks'] = masks
        else:
            info['masks'] = np.array([r0.mask])
        info['zingers'] = zingers
        del info['verbose']
        info['detector'] = r0.detector
        info['dark'] = r0.dark
        # update sensor in case 'auto' option was used
        info['sensor_material'] = r0.sensor_material
        info['sensor_thickness'] = r0.sensor_thickness
        info['sensor_density'] = r0.sensor_density
        # update sample_density in case it was initially None
        info['sample_density'] = r0.sample_density

        if error_model is not None:
            return q, i, e, info
        else:
            return q, i, info

    else:

        if error_model is not None:
            return q, i, e
        else:
            return q, i


def _compare_ai_res(ai, res):
    """Compare 'ai' and integrate1d_dataset() 'res' for changes."""

    has_changes = False
    changes = []

    if not np.isclose(ai.energy, res['energy'], atol=1e-4):
        has_changes = True
        changes.append("energy = %.3f keV --> %.3f keV"
                       % (res['energy'], ai.energy))

    if not np.isclose(ai.dist, res['distance'], atol=1e-6):
        has_changes = True
        changes.append("distance = %.2f mm --> %.2f mm"
                       % (res['distance'] * 1e3, ai.dist * 1e3))

    if ai.detector.name != res['detector']:
        has_changes = True
        changes.append("detector = %s --> %s"
                       % (res['detector'], ai.detector.name))

    if any(ai.detector.binning != res['binning']):
        has_changes = True
        changes.append("binning = (%d, %d) --> (%d, %d)"
                       % (res['binning'][0], res['binning'][1],
                          ai.detector.binning[0], ai.detector.binning[1]))

    if not all(np.isclose(ai.center, res['center'], atol=1e-2)):
        has_changes = True
        changes.append("center = (%.2f, %.2f) --> (%.2f, %.2f)"
                       % (res['center'][0], res['center'][1],
                          ai.center[0], ai.center[1]))

    if not np.isclose(ai.poni1, res['poni1'], atol=1e-6):
        has_changes = True
        changes.append("poni1 = %.2f mm --> %.2f mm"
                       % (res['poni1'] * 1e3, ai.poni1 * 1e3))

    if not np.isclose(ai.poni2, res['poni2'], atol=1e-6):
        has_changes = True
        changes.append("poni2 = %.2f mm --> %.2f mm"
                       % (res['poni2'] * 1e3, ai.poni2 * 1e3))

    if not np.isclose(ai.rot1, res['rot1'], atol=1e-3):
        has_changes = True
        changes.append("rot1 = %.2f rad --> %.2f rad"
                       % (res['rot1'], ai.rot1))

    if not np.isclose(ai.rot2, res['rot2'], atol=1e-3):
        has_changes = True
        changes.append("rot2 = %.2f rad --> %.2f rad"
                       % (res['rot2'], ai.rot2))

    if not np.isclose(ai.rot3, res['rot3'], atol=1e-3):
        has_changes = True
        changes.append("rot3 = %.2f rad --> %.2f rad"
                       % (res['rot3'], ai.rot3))

    return has_changes, changes


def _compare_kwargs_res(kwargs, res):
    """Compare kwargs and previously stored 'res' for changes."""

    has_changes = False
    changes = []

    exclude_pars = ['verbose', 'dark', 'store_all_masks']

    # exclude_pars = ['verbose', 'sensor_material', 'sensor_thickness',
    #                 'sample_material', 'sample_thickness']

    pars = [kw for kw in kwargs if kw not in exclude_pars]

    for par in pars:

        if par in ['mask', 'dark', 'flat', 'variance', 'dummy', 'delta_dummy',
                   'metadata', 'sensor_material', 'sensor_thickness',
                   'sensor_density', 'sample_material', 'sample_thickness',
                   'sample_density']:

            # check if 'h5py._hl.base.Empty'
            if hasattr(res[par], 'size'):
                if res[par].size is None:
                    res[par] = None

        if par in ['dezinger', 'azimuthal_range', 'radial_range']:
            if res[par].size is None:
                res[par] = None
            elif res[par].size == 1:
                res[par] = res[par][0]
            elif res[par].size == 2:
                res[par] = (res[par][0], res[par][1])

        if kwargs[par] is not None and res[par] is None:
            has_changes = True
            changes.append("%s = None --> %s" % (par, kwargs[par]))
        elif kwargs[par] is None and res[par] is not None:
            has_changes = True
            changes.append("%s = %s --> None" % (par, res[par]))
        elif (isinstance(kwargs[par], np.ndarray) and
            isinstance(res[par], np.ndarray)):
                if not np.array_equal(kwargs[par], res[par]):
                    has_changes = True
                    changes.append("%s = %s --> %s" % (par, res[par],
                                                       kwargs[par]))
        elif kwargs[par] != res[par]:
            has_changes = True
            changes.append("%s = %s --> %s" % (par, res[par], kwargs[par]))

    # check if 'dark' is h5py.Empty
    if hasattr(res['dark'], 'size') and res['dark'].size is None:
        res['dark'] = None

    if (isinstance(kwargs['dark'], str) or
            np.any(kwargs['dark'] != res['dark'])):

        par = 'dark'

        if kwargs['dark'] == 'auto' and res['detector'] == 'Rayonix MX170-HS':
            expected_dark = 10 * np.ones(res['image_shape'])
            if res['dark'] is not None:
                if not np.all(np.isclose(res['dark'], expected_dark)):
                    has_changes = True
                    changes.append("%s = %s --> %s" % (par, res[par],
                                                       kwargs[par]))
        else:
            has_changes = True
            changes.append("%s = %s --> %s" % (par, res[par], kwargs[par]))

    return has_changes, changes


def integrate1d_dataset(folder, ai=None, save_fname='id09_azav.h5',
                        force=False, extension='h5',
                        npt=600, method='csr', unit="q_A^-1",
                        normalization_factor=1.0, mask=None, dark='auto',
                        flat=None, solid_angle=True, polarization_factor=0.99,
                        variance=None, error_model='poisson',
                        radial_range=None, azimuthal_range=None, dummy=None,
                        delta_dummy=None, safe=True, metadata=None,
                        dezinger_method='mask_zingers', dezinger=None,
                        sensor_material='auto', sensor_thickness=None,
                        sensor_density=None, sample_material=None,
                        sample_thickness=None, sample_density=None,
                        store_all_masks=False, verbose=True):
    """
    Perform azimuthal integration of a dataset and save results.

    At difference with 'integrate1d_multi':
    - all images are assumed to be in the same folder and have the same format
    - results are returned as a single dict 'res'
    - res['q'] is a 1D numpy array
    - res['i'] is a 2D numpy array

    Parameters
    ----------
    folder : str
        Dataset path.
    ai : pyFAI.azimuthalIntegrator.AzimuthalIntegrator obj or None, optional
        PyFAI azimuthal integrator.
    mask : ndarray or None, optional
        Array (same size as image) with 1 for masked pixels, and 0 for valid
        pixels. Default is None.
    save_fname : str or None, optional
        If not None, the result of the azimuthal integration is saved in the
        save folder where the dataset is, with filename 'save_fname'.
        Default is 'id09_azav.h5'.
    force : bool, optional
        If False (default), the azimuthal integration is not performed
        and previously saved result (if existing) are returned. If True, or
        the file corresponding to 'save_fname' does not exist, the integration
        is performed.
    npt ... dezinger : ...
        See 'integrate1d' docinfo.
    store_all_mask : bool, optional
        If False (default), only the mask applied to the first image is stored.
        If True, a mask is stored for each image. This is useful when
        'dezinger' is not None.

    Returns
    -------
    ret : dict
        Results dictionary containing: q (1D ndarray), i (2D ndarray),
        e (2D ndarray) and info on azimuthal integration.

    """
    folder = os.path.abspath(folder)

    kwargs = {'npt': npt, 'method': method, 'unit': unit,
              'normalization_factor': normalization_factor,
              'mask': mask, 'dark': dark, 'flat': flat,
              'solid_angle': solid_angle,
              'polarization_factor': polarization_factor,
              'variance': variance, 'error_model': error_model,
              'radial_range': radial_range, 'azimuthal_range': azimuthal_range,
              'dummy': dummy, 'delta_dummy': delta_dummy,
              'safe': safe, 'metadata': metadata,
              'dezinger_method': dezinger_method, 'dezinger': dezinger,
              'sensor_material': sensor_material,
              'sensor_thickness': sensor_thickness,
              'sensor_density': sensor_density,
              'sample_material': sample_material,
              'sample_thickness': sample_thickness,
              'sample_material': sample_material,
              'sample_density': sample_density,
              'store_all_masks': store_all_masks,
              'verbose': verbose}

    if save_fname is not None:

        save_fname = os.path.join(folder, save_fname)

        if os.path.exists(save_fname) and not force:

            if verbose:
                print("\nLoading results from previously stored analysis: " +
                      save_fname)

            res = load_hdf5_as_dict(save_fname, verbose=verbose)

            if ai is None:
                print("WARNING: since 'ai' is None, all the other input " +
                      "parameters will be ignored.\n")
                return res

            ai_has_changes, ai_changes = _compare_ai_res(ai, res)

            # update folder in case analysis was previously launched from
            # different location
            res['folder'] = folder

            if sensor_material == 'auto':
                sensor_info = get_sensor_info(ai.detector.name)
                kwargs['sensor_material'] = sensor_info[0]
                kwargs['sensor_thickness'] = sensor_info[1]
                kwargs['sensor_density'] = sensor_info[2]

            if sample_material is not None and sample_thickness is not None:
                if sample_density is None:
                    kwargs['sample_density'] = get_density(sample_material)

            pars_have_changes, pars_changes = _compare_kwargs_res(kwargs, res)

            if not ai_has_changes and not pars_have_changes:
                return res
            else:
                if ai_has_changes and verbose:
                    print("\nWARNING: change in ai object\n" +
                          "\n".join(ai_changes) + "\n")
                if pars_have_changes and verbose:
                    print("\nWARNING: change in integrate1d() parameters\n" +
                          "\n".join(pars_changes) + "\n")
                # re-do analysis

        elif ai is None and extension == 'edf':
            raise Exception("'ai' must be not None if 'save_fname' is None" +
                            " or 'force' is True.")

    imgs, fnames = load_images(folder, extension=extension, return_fnames=True,
                               verbose=verbose)

    if ai is None and extension == 'h5':
        ai = imgs.get_ai()

    if len(imgs) == 0:
        raise Exception("No images found in 'folder'.")

    if error_model is None:
        q, i, info = integrate1d_multi(imgs, ai, return_info=True, **kwargs)
        q = q[0]
        i = np.array(i).T
        e = np.zeros_like(i)
    else:
        q, i, e, info = integrate1d_multi(imgs, ai, return_info=True, **kwargs)
        q = q[0]
        i = np.array(i).T
        e = np.array(e).T

    # format results
    res = info.copy()
    res['q'], res['i'], res['e'] = q, i, e
    res['tth'] = res['tth'][0]
    res['r_mm'] = res['r_mm'][0]
    res['folder'] = folder
    res['fnames'] = fnames
    # store ai info
    res['pixel'] = (ai.pixel1, ai.pixel2)
    res['tilt'] = ai.tilt[0]
    res['tilt_plane_rotation'] = ai.tilt[1]
    res['distance'] = ai.dist
    ai_dict = ai.as_dict()
    for k in ['energy', 'wavelength', 'center', 'detector', 'binning',
              'poni1', 'poni2', 'rot1', 'rot2', 'rot3', 'spline']:
        res[k] = ai_dict[k]
    res['image_shape'] = ai.detector.shape

    if save_fname is not None:

        if verbose:
            print("\nSaving azimuthal average results...")

        # save_dict_as_hdf5(res, save_fname, verbose=verbose)

        create_dataset_args = {'compression': 'gzip', 'compression_opts': 9}

        save_dict_as_hdf5(res, save_fname,
                          create_dataset_args=create_dataset_args,
                          verbose=verbose)

    return res


def get_mask_from_limits(img, mask_lim, invert=False):
    """
    Get mask on the basis of a range defining tuple.

    Parameters
    ----------
    img : array_like
        Image to be analyzed.
    mask_lim : tuple or list
        Pixels with intensity < mask_lim[0] or > mask_lim[1] will be
        True in the mask.
    invert : bool
        If True, 'mask' is inverted. Default is False

    Returns
    -------
    mask : numpy array
        Image mask.

    """
    if mask_lim is None:
        return None

    if not isinstance(mask_lim, (tuple, list)):
        raise TypeError("'mask_lim' must be tuple or list.")

    img = np.array(img)

    if mask_lim[0] is None and mask_lim[1] is None:
        return None
    elif mask_lim[0] is None and mask_lim[1] is not None:
        mask = (img > mask_lim[1])
    elif mask_lim[1] is None and mask_lim[0] is not None:
        mask = (img < mask_lim[0])
    else:
        mask = (img < mask_lim[0]) | (img > mask_lim[1])

    if invert:
        mask = ~mask

    return mask


def get_zingers(img, threshold=2e4, plot=True, clim="auto", verbose=True):
    """
    Find clusters of pixels with intensity >= threshold.

    The center-of-mass of the clustered is returned.

    Parameters
    ----------
    img: numpy array
        image to be analyzed
    threshold: float
        pixel intensity threshold
    plot: bool
        if True, a red circle is plot around each cluster
    clim: str or tuple
        imshow clim, if "auto", clim=(0,threshold)
    verbose: bool
        if True, information on results are printed out

    Returns
    -------
    cluster_xy: list
        list of clusters center-of-mass

    """
    if plot:
        fig, ax = plt.subplots()
        if clim == "auto":
            ax.imshow(img, origin='lower', clim=(0, threshold))
        else:
            ax.imshow(img, origin='lower', clim=clim)

    mask = (img >= threshold)
    npxl = np.sum(mask)
    lw, num = ndimage.label(img * mask)
    if verbose:
        print("There are %d pixel(s) with intensity >= %d."
              % (npxl, threshold))
    if npxl == 0:
        return []
    if verbose:
        print("They are clustered in %d zinger(s).\n" % num +
              "Their center-of-mass is:")
    cluster_xy = []
    for k in range(num):
        yc, xc = ndimage.measurements.center_of_mass(img, lw, k+1)
        if verbose:
            print(xc, yc)
        cluster_xy.append((xc, yc))
        if plot:
            # plt.scatter(xc, yc, s=100, facecolors='none', edgecolor='red')
            circle = plt.Circle((xc, yc), 20, edgecolor='red', fill=False)
            ax.add_patch(circle)
    return cluster_xy


def get_mask_circle(img, radius, center=None):
    """
    Return an image with a masked circle.

    Parameters
    ----------
    img: numpy array
        Input image.
    radius: float
        Circle radius (in pixels).
    center: tuple
        Center coordinates (x,y) (in pixels).
        If None, center=(nrows/2,ncols/2).

    Returns
    -------
    mask: numpy array
        image mask

    """
    # get radius
    nrows, ncols = np.shape(img)
    if center is None:
        xc, yc = int(nrows/2), int(ncols/2)
    else:
        xc, yc = center
        if (xc < 0) or (xc > nrows):
            raise ValueError("Center x-coordinate outside available range.")
        if (yc < 0) or (yc > ncols):
            raise ValueError("Center y-coordinate outside available range.")
    y, x = np.ogrid[:nrows, :ncols]  # create meshgrid
    img_radius = np.sqrt((x-xc)**2 + (y-yc)**2)
    mask = (img_radius <= radius)
    return mask


def get_mask_zingers(img, threshold=2e4, circle_radius=5., verbose=False):
    """
    Returns a mask of the input image where pixels corresponding to
    zingers are masked with circles.

    Zingers are clustered pixels with intensity >= threshold.

    Parameters
    ----------
    img: numpy array
        Input image.
    threshold: float
        Pixel intensity threshold.
    circle_radius: float
        Radius of circles used to mask zingers.
    verbose: bool
        If True, information on zingers detection is printed out.

    Returns
    -------
    mask: numpy array
        image mask

    """
    zingers = get_zingers(img, threshold=threshold, plot=False,
                          verbose=verbose)

    mask = np.array(np.zeros(np.shape(img)), dtype=bool)

    if len(zingers) == 0:
        return mask

    # create a circle mask for every zinger
    for center in zingers:
        submask = get_mask_circle(img, radius=circle_radius, center=center)
        mask = mask | submask

    return mask
