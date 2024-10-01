# -*- coding: utf-8 -*-
"""Data reduction related functions."""

__author__ = "Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "01/09/2021"


import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

from txs.utils import sort_string_delays, t2str
from txs.datasets import read_id09_log_file


plt.ion()


def datared(data, ref_delay, delay_lbl_digits=2, norm=None, qlim=None,
            shots=None, use_ratio=False, red_chi2_max=None, pts_perc_max=None,
            log='id09', scan_motor=None, verbose=True):
    """
    Reduce time-resolved dataset.

    Parameters
    ----------
    data : dict
        Dictionary containing azimuthally averaged scattering patterns
        and information about azimuthal average.
        Keys are 'q', 'i', 'e', 'folder', ...
    ref_delay : str or float
        Reference time-delay. If 'auto', the minimum time-delay will be used.
    delay_lbl_digits : int, optional
        Number of digits used to convert float delays to strings.
        Default is 2 (i.e. 23.453e-9 --> '23ns')
    norm : tuple or dict or str or None
        If tuple, data is divided (normalized) by the mean in the q-range
        between norm[0] and norm[1].
        If str, 'norm' must be one the parameters in the dataset log
        file. Each pattern is then divided (normalized) by the corresponding
        parameter value.
    shots :
        Mask for selecting a subset of all the collected shots.
    log : str or dict, optional
        If of type `str`, the log file to be used to obtain the metadata.
        If of type `dict`, expects a dictionary containing the metadata.
        (default, 'id09')
    scan_motor : None, optional
        Name of motor (as it appears in the log file) whose position was
        changed during data collection. If None (default), it is disregarded.

    Results
    -------
    ...

    Examples
    --------
    >> datared(data, ref_delay="-50us", norm=(2.1, 2.2), qlim=(0, 2.5),
               red_chi2_max=3, verbose=True)

    """
    if data is None:
        raise TypeError("'data' cannot be None.")

    data = deepcopy(data)

    if verbose:
        print("\nReading ID09 log file...")

    if log == 'id09':
        log = read_id09_log_file(data['folder'])
    elif not isinstance(log, dict):
        raise TypeError("'log' must be str or dict.")
    elif 'delay' not in log.keys():
        raise ValueError("No 'delay' key found in 'log'.")

    delays = log['delay']
    if delays.dtype == 'float64':
        delays = np.array(t2str(delays, digits=delay_lbl_digits, decimals=1))

    t_unique = np.unique(delays)
    if isinstance(ref_delay, float):
        ref_delay = t2str(ref_delay, digits=delay_lbl_digits, decimals=1)
    if ref_delay == 'auto':
        ref_delay = sort_string_delays(t_unique, digits=delay_lbl_digits)[0]
    if ref_delay is not None and ref_delay not in t_unique:
        raise ValueError("'ref_delay'=%s not available." % ref_delay +
                         "'ref_delay' must be one of:\n%s" % t_unique)

    # if any([not isinstance(dl, str) for dl in delays]):
    #     raise Exception("All delays labels must be string.")

    if isinstance(norm, str):

        if norm not in log.keys():
            raise ValueError("The key '%s' is not available in 'log'.")

        norm = log[norm]

    # check for size mismatch and trunc if necessary
    if delays is not None:
        nd = delays.size
        ni = data['i'].shape[1]
        if nd != ni and verbose:
            print("\nWARNING: number of lines in log file (%d) !=" % nd +
                  " number of images (%d)." % ni)
        sub = slice(0, min(nd, ni))
        data['i'] = data['i'][:, sub]
        if data['e'] is not None:
            data['e'] = data['e'][:, sub]
        if 'fnames' in data.keys():
            data['fnames'] = data['fnames'][sub]
        if 'zingers' in data.keys():
            data['zingers'] = data['zingers'][sub]

    if scan_motor is None:

        res = datared_core(data['q'], data['i'], delays=delays, e=data['e'],
                           ref_delay=ref_delay, norm=norm, qlim=qlim,
                           shots=shots, use_ratio=use_ratio,
                           red_chi2_max=red_chi2_max,
                           pts_perc_max=pts_perc_max, verbose=verbose)

        res['azav'] = data
        res['delays'] = delays
        res['ref_delay'] = ref_delay
        res['norm'] = norm
        res['qlim'] = qlim
        res['shots'] = shots
        res['use_ratio'] = use_ratio
        res['log'] = log

    else:

        if scan_motor not in log.keys():
            raise ValueError("'scan_motor'='%s' not in log file." % scan_motor)

        scan_pos = np.unique(log[scan_motor])

        res = {}

        for pos in scan_pos:

            idx = (log[scan_motor][sub] == pos)

            if idx.sum() == 0:
                continue

            i_pos = data['i'][:, idx]
            e_pos = data['e'][:, idx]
            # add check in case dataset is analyzed befor the scan is finished
            if len(idx) < len(delays):
                delays_pos = delays[:len(idx)][idx]
            else:
                delays_pos = delays[idx]
            shots_pos = None
            if shots is not None:
                shots_pos = shots[idx]

            r = datared_core(data['q'], i_pos, delays=delays_pos, e=e_pos,
                             ref_delay=ref_delay, norm=norm, qlim=qlim,
                             shots=shots_pos, use_ratio=use_ratio,
                             red_chi2_max=red_chi2_max,
                             pts_perc_max=pts_perc_max, verbose=verbose)

            if verbose:
                print("%s =" % scan_motor, pos)

            r['azav'] = data
            r['delays'] = delays
            r['ref_delay'] = ref_delay
            r['norm'] = norm
            r['qlim'] = qlim
            r['shots'] = shots
            r['use_ratio'] = use_ratio
            r['log'] = log
            
            # res[pos] = r
            res[np.round(pos, 3)] = r  # quick improvement
            # TO DO: make a more proper handle of pos label

    return res


def datared_core(q, i, delays, e=None, ref_delay=None, delay_lbl_digits=None,
                 norm=None, qlim=None, shots=None, use_ratio=False,
                 red_chi2_max=None, pts_perc_max=None, verbose=True):
    """Reduce time-resolved dataset.

    Parameters
    ----------
    q : ndarray (1D)
        Scattering vector magnitude. Shape: (nq, ).
    i : ndarray (2D)
        Azimuthally averaged scattering intensities. Shape: (nq, nshots)
    delays : ndarray (1D)
        List of time-delays. Shape: (nshots, )
    e : ndarray (2D) or None, optional
        Errors on i. Shape: (nq, nshots)
    ref_delay : str or float or None, optional
        Reference time-delay to be used for calculating time-resolved signals.
        If not None, 'ref_delay' must be one of the elements of 'delays'.
        If None (default), absolute patterns are averaged over different
        repetitions, but no time-resolved signal is calculated.
    delay_lbl_digits : int or None, optional
        Number of digits used to convert float delays to strings (in case they
        were not converted before). Defaults is None.
    norm : array-like or None, optional
        Data normalization parameter.
        If array-like, size must be either 2 (q-normalization) or 'nshots'
        (normalization with respect to a monitor).
        In the first case data are divided by their average in the q-range
        between norm[0] and norm[1]. In the second case, each scattering
        pattern is divided by the corresponing element of 'norm'.
        If None (default), no normalization is applied.
    qlim : tuple or dict or None, optional
        Data limits parameter.
        If tuple or dict, must have size 2. Data outside the (qlim[0], qlim[1])
        q-range are discarded. Data limits are applied after data
        normalization.
        If None (default), data limits are not applied.
    shots : array-like or None, optional
        Shots mask.
        If array-like, size must be either 2 or 'nshots'. In the first case,
        shots outside the (shots[0], shots[1]) range are discarded. In the
        second case, 'shots' must be a boolean mask to select the shots to keep
        and those to discard. If None (default), all shots are retained for
        data reduction.
    use_ratio : bool, optional
        If True, the time-resolved signal is calculated as a ratio of
        intensities.
        If False (default), the time-resolved signal is calculated as a
        difference of intensities.
    red_chi2_max : float or None, optional
        Reduced-chi2 threshold. Patterns that deviate more than 'red_chi2_max'
        from the median over different shots are discarded.
    pts_perc_max : float or None, optional
        Maximum percentage of points of a pattern that deviate more than sigma
        from the median over different shots.
        Default is None.

    Returns
    -------
    res : dict
        Dictionary containing the following:

            - 'diff_av': average time-resolved signals (one for each delay)
            - 'diff_err': errors on diff_av.
            - 't': unique time-delays
            - 'diffs': list of time-resolved signals
            - 'red_chi2': list of reduced-chi2
            - 'q', 'i', 'e': arrays after 'qlim', 'shots' and 'norm'

    Examples
    --------
    >>> datared(
    ...     data, ref_delay="-50us", qnorm=(2.1, 2.2), qlim=(0, 2.5),
    ...     red_chi2_max=3, verbose=True
    ... )

    """

    q = deepcopy(q)
    i = deepcopy(i)
    e = deepcopy(e)
    delays = deepcopy(delays)

    if verbose:
        print("\nPerforming data reduction...")

    if np.ndim(i) != 2:
        raise ValueError("'i' must be a 2D array-like.")

    nq, nshots = np.shape(i)[0], np.shape(i)[1]

    if np.shape(q)[0] != nq:
        raise ValueError("Shape mismatch between 'q' and 'i': %s, %s"
                         % (np.shape(q), np.shape(i)))

    # if np.shape(delays)[0] != nshots:
    #     raise ValueError("Shape mismatch between 'i' and 'delays': %s, %s"
    #                      % (np.shape(i), np.shape(delays)))
    if np.shape(delays)[0] > nshots:
        delays = delays[:nshots]

    if red_chi2_max is not None and pts_perc_max is not None:
        raise ValueError("'red_chi2_max' and 'pts_perc_max' cannot be both" +
                         " not None.")

    if e is not None:
        if np.shape(i) != np.shape(e):
            raise ValueError("Shape mismatch between 'i' and 'e': %s, %s"
                             % (np.shape(i), np.shape(e)))
    else:
        e = np.zeros_like(i)

    if ref_delay is not None and ref_delay not in delays:
        raise ValueError("'ref_delay' must be one of the elments of 'delays'.")

    if norm is not None:

        if not hasattr(norm, "__len__"):
            raise TypeError("'norm' must be array-like or None.")

        if np.size(norm) == 2:
            norm_mask = (q >= norm[0]) & (q <= norm[1])
            norm = np.mean(i[norm_mask, :], axis=0)
        elif np.size(norm) != nshots:
            print("WARNING: 'norm' must have size =2 or =%d " % nshots +
                            "number of columns of 'i').")
            norm = norm[:nshots]

        i /= norm[np.newaxis, :]
        e /= norm[np.newaxis, :]

    if qlim is not None:

        if not hasattr(qlim, "__len__"):
            raise TypeError("'qlim' must be array-like or None.")

        if np.size(qlim) != 2:
            raise ValueError("'qlim' must have size 2.")

        q_mask = (q >= qlim[0]) & (q <= qlim[1])
        q = q[q_mask]
        i = i[q_mask, :]
        e = e[q_mask, :]

    if shots is not None:

        if not hasattr(shots, "__len__"):
            raise TypeError("'shots' must be array-like or None.")

        if np.size(shots) == 1:
            shots = (shots[0], nshots)

        if np.size(shots) == 2:
            shots = range(shots[0]-1, shots[1])
        elif np.size(shots) != nshots:
            raise ValueError("'shots' must have size =2 or =%d " % nshots +
                             "number of columns of 'i').")

        i = i[:, shots]
        e = e[:, shots]
        delays = delays[shots]

    sig, err = calc_time_resolved_signal(i, delays, ref_delay=ref_delay,
                                         use_ratio=use_ratio, e=e)

    res = average_time_resolved_signal(sig, delays, ref_delay=ref_delay,
                                       delay_lbl_digits=delay_lbl_digits,
                                       err=err)

    if red_chi2_max is not None or pts_perc_max is not None:

        unfilt = deepcopy(res)
        filt = filt_time_resolved_signal(res, red_chi2_max=red_chi2_max,
                                         pts_perc_max=pts_perc_max,
                                         err=err, verbose=verbose)
        res['diffs'] = filt['diffs']
        res['diff_av'] = filt['diff_av']
        res['diff_err'] = filt['diff_err']
        res['red_chi2'] = filt['red_chi2']
        res['red_chi2_max'] = filt['red_chi2_max']
        res['pts_perc'] = filt['pts_perc']
        res['pts_perc_max'] = filt['pts_perc_max']
        res['diffs_outliers'] = filt['diffs_outliers']
        res['outliers'] = filt['outliers']
        res['diffs_unfilt'] = unfilt['diffs']
        res['diff_av_unfilt'] = unfilt['diff_av']
        res['diff_err_unfilt'] = unfilt['diff_err']
        res['red_chi2_unfilt'] = unfilt['red_chi2']
        res['pts_perc_unfilt'] = unfilt['pts_perc']
        res['filt_res'] = []
        for (d, du) in zip(res['diffs'], res['diffs_unfilt']):
            res['filt_res'].append((d.shape[1], du.shape[1]))

    res['signoise_av'] = []
    for k, t in enumerate(res['t']):
        diff = res['diff_av'][:, k]
        S = np.abs(diff).max()
        N = np.nanstd(diff)
        res['signoise_av'].append(S/N)

    # store masked/normalized 'q', 'i', and 'e'
    res['q'] = q
    res['i'] = i
    res['e'] = e
    res['delays'] = delays

    return res


def calc_time_resolved_signal(i, delays, ref_delay, use_ratio=False, e=None):
    """
    Compute time-resolved signals from a set of scattering patterns measured
    at different time-delays with repetitions.

    The most important step is to calculate the appropriate reference pattern
    for each intensity curve. This is done by interp_refs().

    No averaging is performed besides that done by interp_refs().

    Paramaters
    ----------
    i : array_like (2D)
        Scattered intensity measured at different time-delays.
    delays : array_like (1D)
        List of time-delays at which each scattering pattern in 'i' has
        been collected.
    ref_delay : str or float
        Time-delay to be used as a reference.
    use_ratio : bool, optional
        If True, signal is the ratio between 'i' and 'iref'.
        If False (default), signal is the difference between 'i' and 'iref'.

    Returns
    -------
    sig : 2D np.ndarray
       Time-resolved scattering patterns. 'sig' has the same shape as 'i'.

    """
    if len(delays) != i.shape[1]:
        if len(delays) != i.shape[0]:
            raise ValueError("Shape mismatch between 'i' %s and 'delays' %s"
                             % (i.shape, np.shape(delays)))
        else:
            # if patterns are arranged by rows, transpose:
            i = i.copy().T

    if ref_delay is None:
        return i, e

    idx_ref = np.argwhere(delays == ref_delay)

    iref = interp_refs(i, idx_ref)

    i = deepcopy(i)

    if e is None:
        e = np.zeros_like(i)

    if use_ratio:
        sig = i / iref
        err = np.sqrt((e/i)**2 + (e/iref)**2)
    else:
        sig = i - iref
        err = np.sqrt(2)*e

    return sig, err


def interp_refs(i, idx_ref):
    """
    Linear interpolation of reference curves.

    The reference curve for each "shot" is calculated as the average between
    its two closest reference curves. A weight is introduced in the average
    to account for the distance between the shot and each of the two closest
    reference curves.

    The first available reference curve is used as the reference for all
    initial shots. The last available reference curve is used as the reference
    for all final shots.

    The reference curve for each "reference" is not the reference curve itself,
    but the average of the two closest reference curves.

    Parameters
    ----------
    i : (M, N) ndarray
        Input data. The array first index corresponds to the "shot" number.
    idx_ref : ndarray
        Indeces of reference curves.

    Returns
    -------
    iref : (M, N) ndarray or (N,) ndarray
        Reference curves for each curve in 'i'. If only one reference curve
        is available, a (N,) ndarray is returned.

    """
    iref = np.empty_like(i)
    idx_ref = np.squeeze(idx_ref)
    idx_ref = np.atleast_1d(idx_ref)

    # sometimes there is just one reference (e.g. sample scans)
    if idx_ref.shape[0] == 1:
        iref = i[idx_ref]
        return iref

    for (idx_ref_before, idx_ref_after) in zip(idx_ref[:-1], idx_ref[1:]):
        ref_before = i[:, idx_ref_before]
        ref_after = i[:, idx_ref_after]
        for idx in range(idx_ref_before, idx_ref_after):
            slope = (ref_after-ref_before)/float(idx_ref_after-idx_ref_before)
            iref[:, idx] = ref_before + slope*float(idx-idx_ref_before)
            # print("Ref indeces for shot %d: " % idx +
            #       "%d, %d" % (idx_ref_before, idx_ref_after))

    # for all curvers before first ref: use first ref
    if idx_ref[0] > 0:
        iref[:, :idx_ref[0]] = i[:, idx_ref[0]].reshape(i.shape[0], 1)

    # for all curves after last ref: use last ref
    if idx_ref[-1] < iref.shape[1]:
        iref[:, idx_ref[-1]:] = i[:, idx_ref[-1]].reshape(i.shape[0], 1)

    # take care of the reference for the references ...
    for (idx_ref_before, idx, idx_ref_after) in zip(idx_ref, idx_ref[1:],
                                                    idx_ref[2:-1]):
        ref_before = i[:, idx_ref_before]
        ref_after = i[:, idx_ref_after]
        slope = (ref_after-ref_before)/float(idx_ref_after-idx_ref_before)
        iref[:, idx] = ref_before + slope*float(idx-idx_ref_before)
        # print("Refs for reference %d: " % idx +
        #       "%d, %d" % (idx_ref_before, idx_ref_after))

    # for first ref: use second ref
    iref[:, idx_ref[0]] = i[:, idx_ref[1]]

    # for last ref: use second last ref
    iref[:, idx_ref[-1]] = i[:, idx_ref[-2]]

    return iref


def average_time_resolved_signal(diffs_all, delays, ref_delay,
                                 delay_lbl_digits=None,
                                 err=None, verbose=False):
    """
    Average 'i' for equivalent values in 'delays'.

    Calculate 'red_chi2' and 'pts_perc'.

    Parameters
    ----------
    diff_all : array_like (2D)
        Time-resolved signal.
    delays : array_like (1D)
        List of time-delays associated to 'diff_all'. Each column of 'diff_all'
        corresponds to an element of 'delays'. A given element in 'delays' can
        be repeated several times, i.e. delays != np.unique(delays).
    ref_delay : str
        Reference time-delay.
    delay_lbl_digits : int or None, optional
        Number of digits used to convert float delays to strings (in case they
        were not converted before). Default is None.
        Default is 2 (i.e. 23.453e-9 --> '23ns')
    err : array_like (2D) or None, optional
        Errors associated to scattered intensities.
        If None (default), errors on the average time-resolved signal are
        calculated as the standard deviation over different shots.
    use_ratio : bool, optional
        If True, the signal is the ratio between 'i' and 'iref'.
        If False, the signal is the difference between 'i' and 'iref'.
        Default is False.
    red_chi2_max : float or 'auto' or None, optional
        Threshold level to filter out shots on the basis of their reduced-chi2
        with respect to the median signal.
        If 'auto', the 95th percentile is used as a threshold.
        If None (default), the filter is not applied.

    Returns
    -------
    res : dict
        Dictionary containing the following:
        - 'diff_av': average time-resolved signals (one for each time-delay)
        - 'diff_err': errors on diff_av.
        - 't': unique time-delays
        - 'diffs': list of time-resolved signals (list of 2D numpy arrays)
        - 'red_chi2': list of reduced-chi2 (list of 1D numpy arrays)

     Notes
     -----
      - len(diffs) = len(t); each element in 'diffs' is a numpy array
        containing all shots taken at the same time-delay.

    """

    t_unique = np.unique(delays)
    t_unique = sort_string_delays(t_unique, digits=delay_lbl_digits)
    nt = len(t_unique)
    nq = diffs_all.shape[0]
    diff_av = np.empty((nq, nt))
    diff_err = np.empty((nq, nt))

    diffs = []
    red_chi2 = []
    pts_perc = []

    if verbose:
        print("\nCalculating average time-resolved signals (%d " % nt +
              "time-delays)...")

    for k, t in enumerate(t_unique):

        shot_idx = (delays == t)

        if shot_idx.sum() == 0:
            print("No data to average for scan point %s" % str(t))

        # select data for the scan point
        diffs_t = diffs_all[:, shot_idx]

        # estimate error on unaveraged time-resolved signal
        if err is None or np.all(err) == 0:
            noise = np.nanstd(diffs_t, axis=1)
        else:
            noise = np.nanmean(err[:, shot_idx], axis=1)

        # safety check
        np.place(noise, noise == 0, np.inf)  # 2022-11-30
        if not np.all(noise):  # 2022-11-30
            raise Exception("'noise' cannot be zero!")

        # if it is the reference take only every second ...
        # Magnus and Fredrik do not like this ...
        if t == ref_delay:
            diffs_t = diffs_t[:, ::2]

        # store the signal of all shots taken at the same t
        diffs.append(diffs_t)

        # calc and store average signal
        diff_av[:, k] = np.median(diffs_t, axis=1)
        # calc and store error of the mean sig/sqrt(N)
        diff_err[:, k] = noise/np.sqrt(shot_idx.sum())

        # calc chi2
        diff_av_t = diff_av[:, k].reshape(nq, 1)
        noise = noise.reshape(nq, 1)
        chi2_t = ((diffs_t - diff_av_t)/noise)**2
        chi2_t = np.nansum(chi2_t, axis=0)  # sum over q-axis
        # store reduced-chi2
        red_chi2.append(chi2_t/nq)

        # calc pts_perc
        res_abs = np.abs(diffs_t - diff_av_t)
        pts_t = (res_abs > 3*noise).sum(axis=0)
        # print(pts_t, noise.max())
        pts_perc_t = np.round(pts_t / nq * 100, 1)
        # store pts_perc
        pts_perc.append(pts_perc_t)

    res = dict(t=t_unique, diff_av=diff_av, diff_err=diff_err, diffs=diffs,
               red_chi2=red_chi2, pts_perc=pts_perc)

    return res


def filt_absolute_scattering():
    """
    Filter out absolute patterns.

    All patterns between nearest reference shots are also removed.

    """
    pass


def filt_time_resolved_signal(data, red_chi2_max='auto', pts_perc_max=None,
                              err=None, verbose=False):
    """
    Filter time-resolved difference patterns.

    filtered data: kept patterns
    outliers: filtered out patterns

    Parameters
    ----------
    data : dict
        Dictionary containing the following:
        - 'diff_av': average time-resolved signals (one for each time-delay)
        - 'diff_err': errors on diff_av.
        - 't': unique time-delays
        - 'diffs': list of time-resolved signals (list of 2D numpy arrays)
        - 'red_chi2': list of reduced-chi2 (list of 1D numpy arrays)
    red_chi2_max : float or string or None, optional
        Reduced-chi2 threshold for filtering.
        If 'auto' (default), the 95th-percentile is used as threshold.
    pts_perc_max : float or None, optional
        Thresholde for the percentage of points ...
    err : array_like (2D) or None, optional
        Errors associated to scattered intensities.

    Returns
    -------
    filt : dict
        Dictionary containing the following:
        - 'diffs': filtered time-resolved difference patterns
        - 'diff_av: average of filtered time-resolved difference patterns
        - 'diff_err': errors on diff_av.
        - 'red_chi2_filt': reduced-chi2 on filtered difference patterns
        - 'pts_perc_filt': percentage of points on filtered difference patterns
        - 'red_chi2_max': threshold value actually used for filtering or None
        - 'pts_perc_max': threshold value actually used for filtering or None
        - 'diffs_outliers': outlier time-resolved differnce patterns
        - 'outliers': mask selecting outlier time-resolved difference patterns

    """

    if red_chi2_max is not None and pts_perc_max is not None:
        raise ValueError("'red_chi2_max' and 'pts_perc_max' cannot be both" +
                         " not None.")

    if red_chi2_max is not None and red_chi2_max == 'auto':
        # take 95-th percentile as threshold
        red_chi2_max = np.percentile(np.concatenate(data['red_chi2']), 95)

    if verbose:
        print("\nFiltering time-resolved signals...")

    if red_chi2_max is not None:
        filt_par = 'red_chi2'
        filt_max = red_chi2_max
    elif pts_perc_max is not None:
        filt_par = 'pts_perc'
        filt_max = pts_perc_max
    else:
        filt_par = None
        filt_max = 0

    filt_mask = []
    diffs_filt = []
    red_chi2_filt = []
    pts_perc_filt = []
    diff_av_filt = np.empty_like(data['diff_av'])
    diff_err_filt = np.empty_like(data['diff_err'])
    diffs_outliers = []
    outliers = []

    for k, t in enumerate(data['t']):

        diffs_t = data['diffs'][k]
        nshots = diffs_t.shape[1]  # number of shots corresponding to 't'

        mask = data[filt_par][k] < filt_max
        filt_mask.append(mask)
        nout = (~mask).sum()  # number of outliers corresponding to 't'
        nkept = nshots-nout

        if verbose:
            print("Curves with %s >= threshold at delay=" % filt_par +
                  "'%s': %d/%d (%.2f%%)" % (t, nout, nshots, nout/nshots*100))

        if nshots == 1 or nkept == 0:

            if verbose:
                if nshots == 1:
                    print("--> Only one curve available. " +
                          "No filter will be applied.")
                else:
                    print("--> %s_max=%g is too low. " % (filt_par, filt_max) +
                          "No filter will be applied.")

            # store previous value (no filter is applied)
            diffs_filt.append(diffs_t)
            diff_av_filt[:, k] = data['diff_av'][:, k]
            diff_err_filt[:, k] = data['diff_err'][:, k]
            # store null filters data
            diffs_outliers.append(data['diffs'][k][:, mask])
            outliers.append(~mask)
            red_chi2_filt.append(data['red_chi2'][k])
            pts_perc_filt.append(data['pts_perc'][k])
            continue

        diffs_t = diffs_t[:, mask]
        diffs_filt.append(diffs_t)
        diff_av_filt[:, k] = np.median(diffs_t, axis=1)

        if nkept == 1 or nout == 0:
            # no need to re-calc anything
            diff_err_filt[:, k] = data['diff_err'][:, k]
            diffs_outliers.append(data['diffs'][k])
            if nkept == 1:
                outliers.append(~mask)
                red_chi2_filt.append(np.array([0]))
                pts_perc_filt.append(np.array([0]))
            else:
                diffs_outliers.append(data['diffs'][k][:, ~mask])
                outliers.append(~mask)
                red_chi2_filt.append(data['red_chi2'][k])
                pts_perc_filt.append(data['pts_perc'][k])
            continue

        diffs_outliers.append(data['diffs'][k][:, ~mask])
        outliers.append(~mask)
        # re-calc errors on diff_av pattern
        noise = np.nanstd(diffs_t, axis=1)
        diff_err_filt[:, k] = noise/np.sqrt(nshots)

        # re-calc and store red-chi2 (also when pts_perc filt was applied)
        nq = diffs_t.shape[0]
        diff_av_t = diff_av_filt[:, k].reshape(nq, 1)
        noise = noise.reshape(nq, 1)
        chi2_t = (diffs_t - diff_av_t)**2
        if np.all(chi2_t == 0) or np.all(noise == 0):
            raise Exception("All 'chi2_t' and/or 'noise' values are zero!")
        chi2_t /= noise**2
        chi2_t = np.nansum(chi2_t, axis=0)
        red_chi2_filt.append(chi2_t/nq)

        # re-calc and store pts_perc (also when red_chi2 filt was applied)
        res_abs = np.abs(diffs_t - diff_av_t)
        pts_t = (res_abs > 3*noise).sum(axis=0)
        pts_perc_t = np.round(pts_t / nq * 100, 1)
        pts_perc_filt.append(pts_perc_t)

    filt = dict(diffs=diffs_filt, diff_av=diff_av_filt, diff_err=diff_err_filt,
                red_chi2=red_chi2_filt, pts_perc=pts_perc_filt,
                red_chi2_max=red_chi2_max, pts_perc_max=pts_perc_max,
                diffs_outliers=diffs_outliers, outliers=outliers)

    nkept = len(np.concatenate(filt['red_chi2']))
    ntot = len(np.concatenate(data['red_chi2']))

    if verbose:
        print("--> Filtering result: " +
              "%d difference patterns out of %d kept." % (nkept, ntot))

    return filt
