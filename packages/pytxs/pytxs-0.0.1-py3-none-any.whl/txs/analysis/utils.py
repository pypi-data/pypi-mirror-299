"""Helper functions for the analysis of TR-WAXS data."""


from copy import deepcopy
from dateutil.parser import parse
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

from txs.utils import t2str, str2t


def get_time_delta(data, delay, return_abs=False):
    """Measurement time of difference patterns for given delay.
    
    Parameters
    ----------
    data : dict
        Assumes a dictionary output from `txs.datared.datared`.
    delay : str or int
        Either a string corresponding to the time delay to be used
        or an integer giving the index of this time delay in the
        `data['t']` value.
    return_abs : bool, optional
        If True, the absolute patterns and errors are also returned 
        for the corresponding measurement time deltas.
    
    """
    if isinstance(delay, str):
        delay = data['t'].index(delay)

    if "elapsed_time" not in data['log']:
        datetime = np.array(
            [
                parse(' '.join(val)) for val in 
                zip(data['log']['date'], data['log']['time'])
            ]
        )
        tdelta = np.array(
            [np.round((val - datetime[0]).seconds / 60, 1) for val in datetime]
        )
        to_keep = data['log']['delay'] == data['t'][delay]

    else:
        tdelta = data['log']['elapsed_time'] / 60
        to_keep = np.array(t2str(data['log']['delay'], 3)) == data['t'][delay]

    outliers = data['outliers'][delay]

    tdelta = tdelta[to_keep]

    if len(outliers) > 0:
        step = int(np.ceil(len(tdelta) / len(outliers)))

    tdelta = tdelta[::step][~outliers]

    if not return_abs:
        return tdelta
    else:
        out = (
            tdelta, 
            data['i'][:, to_keep][:, ::step][:, ~outliers], 
            data['e'][:, to_keep][:, ::step][:, ~outliers]
        )
        return out


def common_delay_rescale(data, delay="1ms", ref=0, loss='linear'):
    """Rescale the data sets to minimize the differences on common delay.
    
    Parameters
    ----------
    data : list of dict
        Assumes a list of dictionary output from `txs.datared.datared` each
        corresponding to a measurement run with multiple time delays.
    delay : str, optional
        Delay label to be used. It should present in each data set in `data` 
        argument. 
        (default, '1ms')
    ref : int, optional
        Index of a reference data set to be used for rescaling.
        (default, 0)
    loss : str, {'linear', 'cauchy', 'soft_l1', 'huber', 'arctan'}
        Loss function to be used for the least-square problem.
        (default, 'linear', standard least-square)

    """
    data = deepcopy(data)
    avgs = []
    for s_idx, sample in enumerate(data):
        try:
            delay_idx = list(sample['t']).index(delay)
            avgs.append(sample['diff_av'][:, delay_idx])
        except ValueError as err:
            print(f"Error for data at index {s_idx}: {err}")

    q_ref = data[ref]['q']
    for sidx, sample in enumerate(data):
        interp = interp1d(
            sample['q'], 
            avgs[sidx], 
            bounds_error=False, 
            fill_value="extrapolate"
        )
        avgs[sidx] = interp(q_ref)
        
    avgs = np.array(avgs)
    res = []
    for _, val in enumerate(avgs):
        popt, _ = curve_fit(
            lambda x, p: p * val,
            val,
            avgs[ref],
            p0=1,
            bounds=(0., np.inf),
            ftol=1e-15,
            maxfev=10000,
            loss=loss,
        )
        res.append(popt[0])
    
    for s_idx, sample in enumerate(data):
        data[s_idx]['diff_av'] = sample['diff_av'] * res[s_idx]
        data[s_idx]['diff_err'] = sample['diff_err'] * res[s_idx]
        data[s_idx]['i'] = sample['i'] * res[s_idx]
        data[s_idx]['e'] = sample['e'] * res[s_idx]
        for t_idx, delay in enumerate(sample['t']):
            data[s_idx]['diffs'][t_idx] = sample['diffs'][t_idx] * res[s_idx]

    print(f"Using following factors to rescale provided data: {res}")

    return data


def qrange_rescale(data, qrange=(1.4, 1.5), ref=0, loss='linear'):
    """Rescale the data sets to minimize the differences on a given q-range.
    
    Parameters
    ----------
    data : list of dict
        Assumes a list of dictionary output from `txs.datared.datared` each
        corresponding to a measurement run with multiple time delays.
    qrange : tuple, optional
        Range of q-values to be used.
        (default, (1.4, 1.5))
    ref : int, optional
        Index of a reference data set to be used for rescaling.
        (default, 0)
    loss : str, {'linear', 'cauchy', 'soft_l1', 'huber', 'arctan'}
        Loss function to be used for the least-square problem.
        (default, 'linear', standard least-square)

    """
    data = deepcopy(data)
    avgs = []
    for s_idx, sample in enumerate(data):
        try:
            qmask = (sample['q'] > qrange[0]) & (sample['q'] < qrange[1])
            avgs.append(sample['diff_av'][qmask].mean(1))
        except ValueError as err:
            print(f"Error for data at index {s_idx}: {err}")
        
    avgs = np.array(avgs)
    res = []
    for _, val in enumerate(avgs):
        popt, _ = curve_fit(
            lambda x, p: p * val,
            val,
            avgs[ref],
            p0=1,
            bounds=(0., np.inf),
            ftol=1e-15,
            maxfev=10000,
            loss=loss,
        )
        res.append(popt[0])
    
    for s_idx, sample in enumerate(data):
        data[s_idx]['diff_av'] = sample['diff_av'] * res[s_idx]
        data[s_idx]['diff_err'] = sample['diff_err'] * res[s_idx]
        data[s_idx]['i'] = sample['i'] * res[s_idx]
        data[s_idx]['e'] = sample['e'] * res[s_idx]
        for t_idx, delay in enumerate(sample['t']):
            data[s_idx]['diffs'][t_idx] = sample['diffs'][t_idx] * res[s_idx]

    print(f"Using following factors to rescale provided data: {res}")

    return data


def manual_merging_selection(data, labels=None, invert=False):
    """Group data with common time delays and ask user which are to be kept.
    
    The data are copied and a new list is returned where the unwanted time 
    delays for each sample has been removed.

    Parameters
    ----------
    data : list of dict
        Assumes a list of dictionary output from `txs.datared.datared` each
        corresponding to a measurement run with multiple time delays.
    labels : list of str, optional
        The names corresponding to each sample in `data` for easier 
        identification.
        (default, None, numbers are used instead of names)
    invert : bool
        If True, selected data are discarded instead of being kept.
    
    """
    out = deepcopy(data)

    delays = {}
    for s_idx, sample in enumerate(data):
        for _, delay in enumerate(sample['t']):
            if delay not in delays:
                delays[delay] = []
            delays[delay].append(s_idx)

    print(
        f"Select which samples are to be {'kept' if not invert else 'discarded'} for each time delay:\n"
        "Example use: \n"
            "'-20us: 1+3, 3ms: 1'\n"
        "If a time delay is not given, all samples are kept, unless "
        "`invert` argument is set to True.\n\n"
        "Samples are:\n"
    )

    for key, val in delays.items():
        if labels is not None:
            val = [f"{label}: {labels[label]}" for label in val]
        print(f"{key} -> {val}")

    sel = input("Type your selection: ")
    if sel == '':
        return out
    sel = {
        val.split(":")[0].strip(): val.split(":")[1].split("+")
        for val in sel.split(",")
    }

    for key, val in sel.items():
        val = np.array([int(label) for label in val])            
        samples_at_t = np.array(delays[key])
        mask = np.isin(samples_at_t, val)
        mask = mask if invert else ~mask
        for s_idx in samples_at_t[mask]:
            t_idx = list(out[s_idx]['t']).index(key)
            out[s_idx]['diffs'] = [
                val for idx, val in enumerate(out[s_idx]['diffs']) 
                if idx != t_idx
            ]
            out[s_idx]['diff_av'] =  np.delete(out[s_idx]['diff_av'], t_idx, 1)
            out[s_idx]['diff_err'] =  np.delete(out[s_idx]['diff_err'], t_idx, 1)
            out[s_idx]['red_chi2'] = [
                val for idx, val in enumerate(out[s_idx]['red_chi2']) 
                if idx != t_idx
            ]
            out[s_idx]['pts_perc'] = [
                val for idx, val in enumerate(out[s_idx]['pts_perc']) 
                if idx != t_idx
            ]
            out[s_idx]['diffs_outliers'] = [
                val for idx, val in enumerate(out[s_idx]['diffs_outliers']) 
                if idx != t_idx
            ]
            out[s_idx]['outliers'] = [
                val for idx, val in enumerate(out[s_idx]['outliers']) 
                if idx != t_idx
            ]
            out[s_idx]['diffs_unfilt'] = [
                val for idx, val in enumerate(out[s_idx]['diffs_unfilt']) 
                if idx != t_idx
            ]
            out[s_idx]['diff_av_unfilt'] =  np.delete(
                out[s_idx]['diff_av_unfilt'], t_idx, 1
            )
            out[s_idx]['diff_err_unfilt'] =  np.delete(
                out[s_idx]['diff_err_unfilt'], t_idx, 1
            )
            out[s_idx]['red_chi2_unfilt'] = [
                val for idx, val in enumerate(out[s_idx]['red_chi2_unfilt']) 
                if idx != t_idx
            ]
            out[s_idx]['pts_perc_unfilt'] = [
                val for idx, val in enumerate(out[s_idx]['pts_perc_unfilt']) 
                if idx != t_idx
            ]
            out[s_idx]['filt_res'] = [
                val for idx, val in enumerate(out[s_idx]['filt_res']) 
                if idx != t_idx
            ]
            out[s_idx]['signoise_av'] = [
                val for idx, val in enumerate(out[s_idx]['signoise_av']) 
                if idx != t_idx
            ]
            out[s_idx]['t'] = [
                val for idx, val in enumerate(out[s_idx]['t']) 
                if idx != t_idx
            ]

    return out


def merge_same_delays(
        data, 
        max_chi_square=10, 
        cutoff=None, 
        verbose=True, 
):
    """Average data corresponding to the same time delay.
    
    Parameters
    ----------
    data : list of dict
        Assumes a list of dictionary output from `txs.datared.datared` each
        corresponding to a measurement run with multiple time delays.
    max_chi_square : float, optional
        Maximum value for the chi-square computed between the average of the 
        data and the individual data sets. The chi-square is averaged over
        matching time delays. Each data set that has a chi-square
        value bigger that provided argument is discarded.
        (default, 10)
    cutoff : float or None, optional
        Time in minute where the data should be cut. The average is computed
        up to this point for all measurement in `data`.
    verbose : bool, optional
        Whether or not report on the number of shots kept for each time delay.
        (optional, True)

    Returns
    -------
    out_av : 2D array
        The averaged difference patterns for each time delay (columns).
    out_err : 2D array
        The standard deviation for each time delay (columns).
    delays : list of str
        The time delays corresponding to each column in `out_av` and `out_err`.

    """
    out = deepcopy(data[0])
    diffs = {}
    diff_av = {}
    diff_err = {}
    chi_square = {}
    outliers = {}

    # Get the minimum q vector
    qlist = [val['q'] for val in data]
    q_min_idx = np.argmin([len(val) for val in qlist])
    q_out = qlist[q_min_idx]

    # First, regroup all same time delays together in diffs
    for _, val in enumerate(data):
        for idx, delay in enumerate(val['t']):
            diffs_t = interp1d(
                val['q'], 
                val['diffs'][idx].T, 
                bounds_error=False, 
                fill_value='extrapolate'
            )
            diffs_t = diffs_t(q_out).T

            if cutoff is not None:
                tdelta = get_time_delta(val, delay)
                diffs_t = diffs_t[:, tdelta <= cutoff]

            if delay not in diffs:
                diffs[delay] = diffs_t
            else:
                diffs[delay] = np.column_stack((diffs[delay], diffs_t))

    # Second, perform averages and compute errors
    for key, val in diffs.items():
        err = np.nanstd(val, 1)
        avg = np.median(val, 1)
        diff_av[key] = avg
        diff_err[key] = err / np.sqrt(len(avg))
        chi_square[key] = np.sum(
            (val - avg[:, None]) ** 2 / err[:, None] ** 2,
            0
        ) / avg.size
    
    outliers = {
        key: np.zeros(val.shape[1]).astype(bool) for key, val in diffs.items()
    }
    out['diff_av_unfilt'] = np.column_stack([val for val in diff_av.values()])
    out['diff_err_unfilt'] = np.column_stack([val for val in diff_err.values()])
    out['red_chi2'] = [val for val in chi_square.values()]

    # Third, filter diffs based on chi-square
    if max_chi_square is not None:
        for key, val in diffs.items():
            mask = chi_square[key] <= max_chi_square
            outliers[key] = ~mask
            filt_diffs = val[:, mask]
            err = np.nanstd(filt_diffs, 1)
            avg = np.median(filt_diffs, 1)
            diff_av[key] = avg
            diff_err[key] = err / np.sqrt(len(avg))
            if verbose:
                print(
                    f"delay: {key}, keeping {np.sum(mask)} " 
                    f"out of {val.shape[1]}"
                )

    out['q'] = q_out
    out['t'] = np.array(list(diff_av.keys()))
    out['diffs'] = [val[:, ~outliers[key]] for key, val in diffs.items()]
    out['diffs_unfilt'] = [val for val in diffs.values()]
    out['diff_av'] = np.column_stack([val for val in diff_av.values()])
    out['diff_err'] = np.column_stack([val for val in diff_err.values()])
    out['outliers'] = [val for val in outliers.values()]

    return out

def sort_delays(data, ref_delays=None, include_ref=True):
    """Sort the data according to the time delays
    
    Parameters
    ----------
    data : `txs.datared.datared`
        A `txs.datared.datared` instance.
    ref_delays : list of str
        The delays corresponding to the reference dark measurements.
    include_ref : bool
        If False, the reference delays given in `ref_delays` are removed 
        from the data.
    
    """
    delays = np.array(data['t'])
    if not include_ref:
        if ref_delays is None:
            raise ValueError(
                "'ref_delay' cannot be None if 'include_ref' is False."
            )
        delays = []
        diff_av = []
        for idx, val in enumerate(data['t']):
            if val not in ref_delays:
                delays.append(val)
                diff_av.append(data['diff_av'][:, idx])

        delays = np.array(delays)
        data['diff_av'] = np.column_stack(diff_av)

    # to avoid bad dorting due to 'off' in the entry
    has_off = False
    if 'off' in delays:
        has_off = True
        off_index = list(delays).index('off')
        delays = np.delete(delays, off_index)
        data['diff_av'] = np.delete(data['diff_av'], off_index, 1) 
        data['diff_err'] = np.delete(data['diff_err'], off_index, 1) 
        off_diffs = data['diffs'].pop(off_index)

    indices = np.argsort([str2t(val) for val in delays])
    delays = delays[indices]
    diff_av = data['diff_av'][:, indices]
    diff_err = data['diff_err'][:, indices]
    diffs = [data['diffs'][idx] for idx in indices]

    if has_off:
        delays = ['off'] + list(delays)
        diff_av = np.column_stack((data['diff_av'][:, off_index], diff_av))
        diff_err = np.column_stack((data['diff_err'][:, off_index], diff_err))
        diffs = [off_diffs] + diffs

    data['t'] = list(delays)
    data['diff_av'] = diff_av
    data['diff_err'] = diff_err
    data['diffs'] = diffs

    return data