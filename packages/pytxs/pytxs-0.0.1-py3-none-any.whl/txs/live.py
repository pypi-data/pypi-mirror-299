# -*- coding: utf-8 -*-
"""Functions for real-time data reduction."""

__author__ = "Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "01/09/2021"


import os
import time
import numpy as np
import matplotlib.pyplot as plt

from txs.utils import load_hdf5_as_dict, save_dict_as_hdf5
from txs.datasets import load_images
from txs.azav import _compare_ai_res, _compare_kwargs_res
from txs.azav import integrate1d_multi
from txs.datared import datared
from txs.plot import plot_diffs, track_abs_init, track_abs_update
from txs.plot import track_diff_init, track_diff_update
from txs.corr import get_density, get_sensor_info


plt.ion()

ana_continue = False


def ana(folder, ref_delay, ai=None, extension='h5', qnorm=None, qlim_azav=None,
        save_fname='id09_azav.h5', force=False, npt=600, method='csr',
        unit="q_A^-1", normalization_factor=1.0, mask=None, dark='auto',
        flat=None, solid_angle=True, polarization_factor=0.99,
        variance=None, error_model='poisson', radial_range=None,
        azimuthal_range=None, dummy=None, delta_dummy=None, safe=True,
        metadata=None, dezinger_method='mask_zingers', dezinger=None,
        sensor_material='auto', sensor_thickness=None, sensor_density=None,
        sample_material=None, sample_thickness=None, sample_density=None,
        norm=None, qlim_datared=None, shots=None, use_ratio=False,
        red_chi2_max=None, pts_perc_max=None, log='id09', do_azav=True,
        do_datared=True, sleep_azav=0.5, sleep_datared=0.1, sleep_save=1,
        sleep_loop=10, plot=False, track_abs=False, track_diff=False,
        track_diff_t='last', qmon=None, result_callback=None,
        track_abs_qmon=None, track_diff_qmon=None,
        progress_callback=None, debug=False, verbose=True):

    """
    Azimuthal average and data reduction real-time analysis.

    Parameters
    ----------
    ... parameters of integrate1d_dataset() and of datared() ...
    do_azav : bool
        If True (default), new images are azimuthally averaged.
    do_datared : bool
        If True (default), data reduction is performed on available data.
    sleep_azav : float
        Sleep time before new azimuthal average.
    sleep_datared : float
        Sleep time before new data reduction.
    plot_diffs ; bool
        if True, diffs patterns are plotted after every new data reduction.
    track_abs : bool
        If True, abs patterns are plotted after every new azimuthal average.
    qmon1 :
    qmon2 :

    Returns
    -------
    ... output from datared() ...

    """

    global ana_continue

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
              'verbose': verbose}

    azav, exclude = None, None

    folder = os.path.abspath(folder)

    first_attempt = True

    if track_abs_qmon is None:
        track_abs_qmon = qmon

    if track_diff_qmon is None:
        track_diff_qmon = qmon

    if save_fname is not None:

        if debug:
            print("\n1... Check if file is available\n")

        save_fname = os.path.join(folder, save_fname)

        if os.path.exists(save_fname) and not force:

            if debug:
                print("\n2... File exists!\n")

            if verbose:
                print("\nLoading results from previously stored analysis: " +
                      save_fname)

            azav = load_hdf5_as_dict(save_fname, verbose=verbose)
            first_attempt = False

            if ai is None:
                raise ValueError("'ai' must be not None.")

            ai_has_changes, ai_changes = _compare_ai_res(ai, azav)

            if kwargs['sensor_material'] == 'auto':
                sensor_info = get_sensor_info(ai.detector.name)
                kwargs['sensor_material'] = sensor_info[0]
                kwargs['sensor_thickness'] = sensor_info[1]
                kwargs['sensor_density'] = sensor_info[2]

            if sample_material is not None and sample_thickness is not None:
                if sample_density is None:
                    kwargs['sample_density'] = get_density(sample_material)

            pars_have_changes, pars_changes = _compare_kwargs_res(kwargs, azav)

            if ai_has_changes or pars_have_changes:

                if ai_has_changes and verbose:
                    print("WARNING: change in ai object\n" +
                          "\n".join(ai_changes) + "\n")

                if pars_have_changes and verbose:
                    print("WARNING: change in integrate1d() parameters\n" +
                          "\n".join(pars_changes) + "\n")

                if verbose:
                    print("\nData will be re-analyzed with new " +
                          "parameters.")
                azav = None

            if azav is not None:

                if do_datared:

                    res = datared(azav, ref_delay=ref_delay, norm=norm,
                                  qlim=qlim_datared, shots=shots,
                                  use_ratio=use_ratio,
                                  red_chi2_max=red_chi2_max,
                                  pts_perc_max=pts_perc_max, log=log,
                                  verbose=verbose)

                    if result_callback is not None:
                        result_callback.emit(res)

                    if plot:
                        fig_diffs = plot_diffs(res, return_fig=True,
                                               tpause=0.5)
                        if debug:
                            print("\n3... Plot 1st fig: %d\n" % fig_diffs.number)

                    if track_diff:
                        fig_diff, ax_diff, l_diff, sigd = track_diff_init(res,
                            qmon=track_diff_qmon, qnorm=qnorm, track_t=track_diff_t)

                if track_abs:
                    fig_abs, ax_abs, l_abs, sig = track_abs_init(azav,
                            qmon=track_abs_qmon, qnorm=qnorm)

                # data are azimuthally averaged only once
                exclude = azav['fnames']

        elif ai is None and extension == 'edf':

            raise Exception("'ai' must be not None if 'save_fname is None" +
                            " or 'force' is True.")

        else:

            print("\nNo previous analysis found.")

    elif not do_azav:

        raise Exception("'save_fname' cannot be None if 'do_azav' is False.")

    ana_continue = True

    tloop = time.time()

    while ana_continue:

        print(first_attempt)

        titer = time.time()

        try:

            if debug:
                print("\n4... Restart while loop\n")

            if do_azav:

                imgs, fnames = load_images(folder, extension=extension,
                                           exclude=exclude,
                                           return_fnames=True,
                                           verbose=True)

                if len(imgs) == 0:

                    if first_attempt:
                        print("WARNING: No images in folder!" +
                              "         Check that the folder you chose is" +
                              "         the correct one.")

                    if debug:
                        print("\n5... No new image found\n")

                    print("\nWaiting for new images...")

                    while len(imgs) == 0 and ana_continue:

                        time.sleep(1)

                        if progress_callback is not None:
                            # emit progress information to gui
                            progress_callback.emit(".")
                        else:
                            print(".", end="", flush=True)

                        imgs, fnames = load_images(folder, extension=extension,
                                                   exclude=exclude,
                                                   return_fnames=True,
                                                   verbose=False)

                    if not ana_continue:
                        return res

                    print("\nNew image(s) found...")

                    first_attempt = False


                if extension == 'h5' and ai is None:
                    ai = imgs.get_ai()

                if error_model is None:
                    q, i, info = integrate1d_multi(imgs, ai, return_info=True,
                                                   **kwargs)
                    q = q[0]
                    i = np.array(i).T
                    e = np.zeros_like(i)
                else:

                    if debug:
                        print("\n6... do azav\n")

                    q, i, e, info = integrate1d_multi(imgs, ai,
                                                      return_info=True,
                                                      **kwargs)
                    q = q[0]
                    i = np.array(i).T
                    e = np.array(e).T

                if azav is None:
                    # if no 'azav' has been saved, format results as in
                    # integrade1d_dataset()
                    azav = info.copy()
                    azav['q'], azav['i'], azav['e'] = q, i, e
                    azav['tth'] = azav['tth'][0]
                    azav['r_mm'] = azav['r_mm'][0]
                    azav['folder'] = folder
                    azav['fnames'] = fnames
                    # store ai info
                    azav['pixel'] = (ai.pixel1, ai.pixel2)
                    azav['tilt'] = ai.tilt[0]
                    azav['tilt_plane_rotation'] = ai.tilt[1]
                    azav['distance'] = ai.dist
                    ai_dict = ai.as_dict()
                    for k in ['energy', 'wavelength', 'center', 'detector',
                              'binning', 'poni1', 'poni2', 'rot1', 'rot2',
                              'rot3', 'spline']:
                        azav[k] = ai_dict[k]
                    azav['image_shape'] = ai.detector.shape
                else:
                    # add new curves to 'azav'
                    azav['i'] = np.hstack((azav['i'], i))
                    azav['e'] = np.hstack((azav['e'], e))
                    azav['fnames'] = np.hstack((azav['fnames'], fnames))
                    azav['zingers'] = np.hstack((azav['zingers'],
                                                info['zingers']))
                    azav['masks'] = np.vstack((azav['masks'], info['masks']))

                exclude = azav['fnames']

                if 'fig_abs' not in locals().keys() and track_abs:
                    fig_abs, ax_abs, l_abs, sig = track_abs_init(azav,
                            qmon=track_abs_qmon, qnorm=qnorm)
                elif track_abs:
                    l_abs, sig = track_abs_update(azav, fig_abs, ax_abs, l_abs,
                                                  sig, qmon=track_abs_qmon, qnorm=qnorm)

            dt = time.time() - titer

            print("\ndt = %.3fs; sleep_datared=%.1fs" % (dt, sleep_datared))

            if do_datared and (dt > sleep_datared):

                if debug:
                    print("\n7... do datared\n")

                res = datared(azav, ref_delay=ref_delay, norm=norm,
                              qlim=qlim_datared, shots=shots,
                              use_ratio=use_ratio, red_chi2_max=red_chi2_max,
                              pts_perc_max=pts_perc_max, log=log,
                              verbose=verbose)

                if result_callback is not None:
                    result_callback.emit(res)

                if plot:
                    if 'fig_diffs' not in locals().keys():
                        fig_diffs = None
                    fig_diffs = plot_diffs(res, fig=fig_diffs, tpause=0.5,
                                           return_fig=True)
                    if debug:
                        print("\n8... update plot (fig=%d)\n" % fig_diffs.number)

                if 'fig_diff' not in locals().keys() and track_diff:
                    fig_diff, ax_diff, l_diff, sigd = track_diff_init(res,
                            qmon=track_diff_qmon, qnorm=qnorm, track_t=track_diff_t)
                elif track_diff:
                    l_diff, sig = track_diff_update(res, fig_diff, ax_diff,
                            l_diff, sigd, qmon=track_diff_qmon, qnorm=qnorm,
                            track_t=track_diff_t)

            print("\ndt = %.3fs; sleep_save=%.1fs" % (dt, sleep_save))

            if do_azav and save_fname is not None and (dt > sleep_save):

                if debug:
                    print("\n9... save results\n")

                if verbose:
                    print("\nSaving azimuthal average results...")

                create_dataset_args = {'compression': 'gzip',
                                       'compression_opts': 9}

                save_dict_as_hdf5(azav, save_fname,
                                  create_dataset_args=create_dataset_args,
                                  verbose=verbose)

            print("\nLoop sleep (%.1f sec)..." % sleep_loop)
            time.sleep(sleep_loop)

        except KeyboardInterrupt:
            print("\nExiting real-time data reduction...")
            if 'res' in locals().keys():
                return res
            else:
                return None
