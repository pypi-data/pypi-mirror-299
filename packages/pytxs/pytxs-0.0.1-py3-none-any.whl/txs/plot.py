# -*- coding: utf-8 -*-
"""Plotting functions."""

__author__ = "Matteo Levantino"
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "01/09/2021"


import numpy as np
import matplotlib.pyplot as plt
from math import ceil, floor
from matplotlib.colors import SymLogNorm  # not available in matplotlib 3.1
from pathlib import Path
from txs.utils import t2str

plt.ion()

qlabel = r"q ($\AA^{-1}$)"


def plot_raw_diffs():
    pass


def plot_raw_abs():
    pass


def plot_diffs_and_abs():
    pass


def plot_diffs(data, sel=None, every=None, hide_lines=False, cmap=None,
               yscale='diff', lbls=None, error_bars=False, title='short',
               plot_ref=True, plot_abs_mean=False, diff_plus_ref=False,
               tpause=None, tdigits=2, legend_ncols='auto', legend_nlines=None,
               xlabel=qlabel, xlim=(0, None), ylim=None, figsize=None,
               fig=None, ax=None, return_fig=False, return_ax=False,
               return_lines=False):
    """
    Plot time-resolved difference patterns (averaged over different delays).

    Difference patterns can be hidden or shown upon a click on the
    corresponding legend entry.

    Parameters
    ------------
    data : dict or tuple
        Data reduction result obtained from the txs.datared.datared().
    sel : list or slice or None, optional
        List of time-delays (strings) for the plot. Only difference patterns
        corresponding to the time-delays list will be displayed in the plot.
        If None (default), all difference patterns will be displayed.
    every : int or None, optional
        Spacing at which time-delays for the plot will be selected. If 'sel'
        is not None, 'every' will be applied to 'sel' rather than to the whole
        list of time-delays.
        If None (default), all difference patterns will be displayed.
    hide_lines : bool, optional
        If True, all selected curves are hidden. Default is False.
    cmap : str or None, optional
        Name of matplotlib colormap.
    yscale : str, optional
        If 'diff' (default), scattering intensity differences are plotted.
        If 'qdiff', scattering intensity difference times q-values are plotted.
    lbls : list or None, optional
        List of labels to be used for the plot legend. Default is None.
    error_bars : bool, optional
        If True, patterns are plotted with error bars. Default is False.
    title : str or None, optional
        Figure title.
        If None, the full data folder is used as title.
        If 'short' (default), the data folder is used as title, but only the
        last 2 subfolders are kept and the other parent subfolders are removed.
    remove_folder_parent
    plot_ref : bool, optional
        If True (default), the difference pattern corresponding to the
        reference time-delay is plotted.
    plot_abs_mean : bool, optional
        If True, the average absolute pattern (average over all data,
        irrespective of the time-delay) is plotted on a separate (top) panel.
        Default is False.
    diff_plus_ref : bool, optional
        If True, will plot the absolute patterns for each time delay
        calculated as average of ref patterns + differential patterns
    tpause : float or None, optional
        Interval time after which the figure is updated.
    tdigits : int, optional
        Number of digits used for time-delay labels. Default is 2.
    legend_ncols : int or 'auto' or None
        If 'auto' (default), the number of columns in the legend is modified
        automatically and optimized on the basis of the total number of curves.
        (if nlines is Nones, the legend will use default matplotlib settings)
        If int, the legend will have 'ncols' columns.
        If None, the legend will use default matplotlib settings.
        (same as ncols=1).
    legend_nlines : int or None
        If 'auto' (default), the number of lines in the legend is modified
        automatically and optimized to fit figure height.
        If None (default), the legend will use default matplotlib settings
        (no limitations on the number of lines is applied).
        If int, the legend will have 'nlines' lines.

    """

    if isinstance(data, dict):
        x = data['q']
        t = data['t']
        y = data['diff_av']
        e = data.get('diff_err', None)
        if 'azav' in data.keys():
            folder = data['azav'].get('folder', None)
        if 'filt_res' in data.keys():
            filt_res = data['filt_res']
        else:
            filt_res = None
    elif isinstance(data, (list, tuple)):
        folder = None
        filt_res = None
        if len(data) == 3:
            x, y, t = data
        elif len(data) == 4:
            x, y, t, e = data
        else:
            raise ValueError("'data' must have length 3 or 4 if array-like.")
    else:
        raise TypeError("'data' must be dict or array-like.")

    if yscale in ['qdiff', 'qdeltai', 'qdi', 'q*deltai']:
        for k in range(y.shape[1]):
            y[:, k] = x*y[:, k]
        ylabel = r'q*$\Delta$I'
    else:
        ylabel = r'$\Delta$I'

    if title is None:
        title = folder
    elif title == 'short':
        title = Path(*Path(folder).parts[-2:])
    else:
        if not isinstance(title, 'str'):
            raise TypeError("'title' must be None or str.")

    if lbls is None:
        lbls = [t2str(tt, digits=tdigits) for tt in t]

    if filt_res is not None:
        filt_lbls = ["(%d/%d)" % res for res in filt_res]
        lbls = ["%s %s" % (l1, l2) for (l1, l2) in zip(lbls, filt_lbls)]

    if ax is None:

        if fig is None:
            fig = plt.figure()
        else:
            fig.clear()

        if plot_abs_mean:
            ax0, ax = fig.subplots(2, 1, sharex=True)
            ax0.plot(x, np.median(data['i'], axis=1))
            ax0.set_ylabel("Scattering intensity (a.u.)")
            ax0.set_ylim(0, )
            ax0.grid(alpha=0.7)
            ax0.legend(['median'], loc='upper right')
        else:
            ax = fig.subplots(1, 1)

    elif fig is None:
        fig = ax.figure()
    else:
        ax = fig.gca()

    if diff_plus_ref:
        y = y.T + _ref_average(data)
        y = y.T

    ret = _plot(x, y, t, e=e, sel=sel, every=every, hide_lines=hide_lines,
                cmap=cmap, lbls=lbls, error_bars=error_bars, title=title,
                xlabel=xlabel, ylabel=ylabel, xlim=xlim, ylim=ylim,
                tpause=tpause, figsize=figsize, fig=fig, ax=ax,
                return_fig=return_fig, return_ax=return_ax,
                return_lines=return_lines, legend_ncols=legend_ncols,
                legend_nlines=legend_nlines)

    return ret


def plot_abs(data, sel=None, every=None, hide_lines=False, cmap=None,
             lbls=None, error_bars=False, title='short', tpause=None,
             folder_parent=None, xlabel=qlabel, ylabel=None, xlim=(0, None),
             ylim=(0, None), fig=None, ax=None, return_fig=False,
             return_ax=False, legend_ncols='auto', legend_nlines=None,
             figsize=None, map2D=False, map_clim=None, return_lines=False):
    """
    Plot absolute patterns.

    TO DO: should plot averages absolute patterns
           diff_av(q, t) + <abs(q, tref)>

    TO DO: map2D should go to plot_raw_abs and plot_raw_diffs

    Patterns can be hidden or shown upon a click on the
    corresponding legend entry.

    Parameters
    ----------
    data : dict or tuple
        Data reduction result obtained from the txs.datared.datared().
    sel : list or slice or None, optional
        List of time-delays (strings) for the plot. Only patterns
        corresponding to the time-delays list will be displayed in the plot.
        If None (default), all patterns will be displayed.
    every : int or None, optional
        Spacing at which time-delays for the plot will be selected. If 'sel'
        is not None, 'every' will be applied to 'sel' rather than to the whole
        list of time-delays.
        If None (default), all patterns will be displayed.
    hide_lines : bool, optional
        If True, all selected curves are hidden. Default is False.
    cmap : str or None, optional
        Name of matplotlib colormap.
    lbls : list or None, optional
        List of labels to be used for the plot legend. Default is None.
    error_bars : bool, optional
        If True, patterns are plotted with error bars. Default is False.
    title : str or None, optional
        Figure title.
        If None, the full data folder is used as title.
        If 'short' (default), the data folder is used as title, but only the
        last 2 subfolders are kept and the other parent subfolders are removed.
    tpause : float or None, optional
        Interval time after which the figure is updated.
    legend_ncols : int or 'auto' or None
        If 'auto' (default), the number of columns in the legend is modified
        automatically and optimized on the basis of the total number of curves.
        (if nlines is Nones, the legend will use default matplotlib settings)
        If int, the legend will have 'ncols' columns.
        If None, the legend will use default matplotlib settings.
        (same as ncols=1).
    legend_nlines : int or None
        If 'auto' (default), the number of lines in the legend is modified
        automatically and optimized to fit figure height.
        If None (default), the legend will use default matplotlib settings
        (no limitations on the number of lines is applied).
        If int, the legend will have 'nlines' lines.
    map2D : bool, optionnal
        If True, will display the patterns as a 2D map (image_number,q)
    map_clim : tupple or None
        Ignored if map2D is False

    """

    if isinstance(data, dict):
        x = data['q']
        t = data['delays']
        y = data['i']
        e = data.get('e', None)
        folder = data['azav'].get('folder', None)
    elif isinstance(data, (list, tuple)):
        folder = None
        if len(data) == 3:
            x, y, t = data
        elif len(data) == 4:
            x, y, t, e = data
        else:
            raise ValueError("'data' must have length 3 or 4 if array-like.")

    ylabel = 'Scattered intensity (a.u.)'

    if title is None:
        title = folder
    elif title == 'short':
        title = Path(*Path(folder).parts[-2:])
    else:
        if not isinstance(title, 'str'):
            raise TypeError("'title' must be None or str.")

    if lbls is None:
        lbls = range(y.shape[1])

    if ax is None:
        if fig is None:
            fig = plt.figure()
        ax = fig.subplots(1, 1)
    elif fig is None:
        fig = ax.figure()

    ret = _plot(x, y, t, e=e, sel=sel, every=every, hide_lines=hide_lines,
                cmap=cmap, lbls=lbls, error_bars=error_bars, title=title,
                xlabel=xlabel, ylabel=ylabel, xlim=xlim, ylim=ylim,
                tpause=tpause, fig=fig, ax=ax, return_fig=return_fig,
                return_ax=return_ax, return_lines=return_lines,
                figsize=figsize, legend_ncols=legend_ncols,
                legend_nlines=legend_nlines, map2D=map2D, map_clim=map_clim)

    return ret


def plot_filt_hist(res, filt='red_chi2', bins=None, fig=None, ax=None):
    """Plot histogram of filtering parameter ('red_chi2' or 'pts_perc')."""

    if filt not in ['red_chi2', 'pts_perc']:
        raise ValueError("'filt' must be 'red_chi2' or 'pts_perc'.")

    if fig is None:
        fig = plt.figure()

    if ax is None:
        fig.add_subplot(111)
        ax = plt.gca()

    y = np.concatenate(res[filt])
    ny = len(y)
    if bins is None:
        if int(ny/5) > 10:
            bins = int(ny/5)
        else:
            bins = 10  # default for plt.hist()
    ax.hist(y, bins=bins)
    ax.set_xlabel(filt)
    ax.set_ylabel("number of occurrences")
    ax.set_title("histogram over %d curves (%d bins)" % (ny, bins))
    ax.grid(alpha=0.7)
    if filt+"_max" in res.keys():
        if res[filt+"_max"] is not None:
            ax.legend(["%s = %g" % (filt+"_max", res[filt+"_max"])])
    else:
        ax.legend([filt+"_max"])


def plot_motor_scan(res, qrange, td, abs_value=True, min_max=False,
                    xscale=1, yscale=1, xlabel='scan motor position',
                    title='auto', fig=None, ax=None):
    """
    Plot average difference signal (averaged over a given q-range)
    as a function of a scanned motor position.

    The motor position corresponding to the max value of the 
    averaged difference signal is automatically calculated.

    Parameters
    ----------
    res : dict
        Result of txs.datared.datared() with 'scan_motor' != None.
    qrange : array-like
        Range of q-values (min, max) to use for signal averaging.
    td : str, optional
        Time-delay label corresponding to the data to use for the plot.
    abs_value : bool, optional
        If True, the absolute value of difference patterns is used
        to calculate the best motor position.
        Default is True.
    min_max : bool, optional
        If True, the difference between the max difference signal
        and the min difference signal is used to calculate the position
        (NO AVERAGED IS DONE!!!). Default is False.
    xscale : float, optional
        Scaling factor for motor position values. Default is 1.
    yscale : float, optional
        Scaling factor for signal. Default is 1.
    xlabel : str, optional
        Label for signal plot x-axis. Default is "scan motor position".BaseException
    title : str or None, optional
        If None, the full data folder is used.
        If 'auto', the dataset name is used.

    """

    pos = list(res.keys())
    res0 = res[pos[0]]
    tds = np.array(res0['t'])
    if td not in tds:
        raise ValueError("'td' must be in: ", tds)

    td_idx = (tds == td)
    t = tds[td_idx][0]
    q = res0['q']
            
    if abs_value and min_max:
        raise ValueError("'abs_value' and 'min_max' cannot be both True.")

    sig = []
    for p in pos:
        diff_av = res[p]['diff_av'][:, td_idx][:, 0]
        qidx = (q >= qrange[0]) & (q <= qrange[1])
        if abs_value:
            sk = np.mean(np.abs(diff_av[qidx]), axis=0)
        elif min_max:
            diff_max = np.max(diff_av[qidx], axis=0)
            diff_min = np.min(diff_av[qidx], axis=0)
            sk = abs(diff_max - diff_min)
        else:
            sk = np.mean(diff_av[qidx], axis=0)
        sig.append(sk)

    pos_max = np.array(pos)[sig == max(sig)][0]
    diff_av_max = res[pos_max]['diff_av'][:, td_idx][:, 0]

    pos = xscale*np.array(pos)
    sig = yscale*np.array(sig)
    pos_max *= xscale
    diff_av_max *= yscale

    fig, ax = plt.subplots(2, 1)

    folder = res0['azav']['folder']

    if title is None:
        title = folder
    elif title == 'auto':
        title = Path(*Path(folder).parts[-2:])
    else:
        if not isinstance(title, str):
            raise TypeError("'title' must be None or str.")

    fig.suptitle(title)
    
    ax[1].plot(pos, sig, '.-')
    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel(r"Average over q=(%.2f, %.2f) $\AA^{-1}$"
                     % (qrange[0], qrange[1]))
    ax[1].grid(alpha=0.7)
    ax[1].legend([t])

    ax[0].plot(q, diff_av_max)
    ymin, ymax = ax[0].get_ylim()
    ax[0].vlines(x=qrange[0], ymin=ymin, ymax=ymax, ls='--', color='k')
    ax[0].vlines(x=qrange[1], ymin=ymin, ymax=ymax, ls='--', color='k')
    ax[0].set_xlabel(qlabel)
    ax[0].set_ylabel(r'$\Delta$I')
    ax[0].grid(alpha=0.7)
    ax[0].legend(["pos=%g" % pos_max])

    plt.tight_layout()


def plot_azim_regroup(img, ai, N=600, M=360, center=None, vline=None,
                      label=None, ax=None, return_ax=False,
                      cmap="inferno", clim=None):
    """
    Perform and plot azimuthal 2d regrouping ("caking") of an image

    Azimuthal regrouping is performed over N radian bins and M angular steps.

    Parameters
    ----------
    img : array_like
        Image.
    ai : pyFAI ...
        pyFAI azimuthal integrator obj.
    N : int, optional
        Number of radial bins. Default is 600.
    M : int, optional
        Number of angular steps. Default is 360.
    cmap : str, optional
        Figure colormap.
        Default is 'inferno'.
    clim : tuple or None, optional
        Figure color limits.
        Default is None.

    """

    if center is not None:
        ai.setFit2D(centerX=center[0], centerY=center[1],
                    directDist=ai.dist*1e3,
                    tilt=ai.tilt[0], tiltPlanRotation=ai.tilt[1])

    res = ai.integrate2d(img, N, M, unit="2th_deg")

    rad = res.radial  # 2th in deg
    azm = res.azimuthal  # phi in ??

    if ax is None:
        fig, ax = plt.subplots()

    ax.clear()

    colornorm = SymLogNorm(
        1, base=10, vmin=np.nanmin(img), vmax=np.nanmax(img))

    ax.imshow(
        res.intensity, origin='lower',
        extent=[0, rad.max(), azm.min(), azm.max()],
        aspect='auto',
        cmap=cmap,
        clim=clim,
        norm=colornorm)

    if label:
        ax.set_title("2D regrouping")
    else:
        ax.set_title(label)

    ax.set_xlabel(r"Scattering angle $2\theta$ ($^{o}$)")
    ax.set_ylabel(r"Azimuthal angle $\varphi$ ($^{o}$)")

    # if center is not None:
    #     xc = center[0]*ai.pixel1 - ai.poni1  # m
    #     yc = center[1]*ai.pixel2 - ai.poni2  # m
    #     r = np.sqrt(xc**2 + yc**2)  # m
    #     phi = np.rad2deg(np.arccos(xc/r))
    #     tth = np.rad2deg(np.arctan(r/ai.dist))
    #     ax.vlines(x=phi, ymin=azm.min(), ymax=azm.max(), ls='--')
    #     ax.hlines(y=tth, xmin=rad.min(), xmax=rad.max(), ls='--')

    ax.vlines(x=0, ymin=azm.min(), ymax=azm.max(), ls='--')
    ax.hlines(y=0, xmin=0, xmax=rad.max(), ls='--')

    if vline:
        ax.vlines(x=vline, ymin=azm.min(), ymax=azm.max())

    if return_ax:
        return res, ax
    
    return res


def _track_init(qmon=None):
    """
    Prepare new figure to monitor scattering patterns and track specific the
    signal in specific qrange(s).

    Parameters
    ----------
    data : output of txs.azav.integrate1d_dataset()
        Input data
    qmon : tuple or list or None, optional
        Monitor q-range(s). If tuple, monitoring q-range is (qmon[0], qmon[1]).
        If list, each element of the list is a monitoring q-range.
        If None (default), only absolute patterns are tracked.

    Returns
    -------
    ...

    """
    if qmon is None:
        fig, ax0 = plt.subplots(1, 1)
        ax1 = None
        ax2 = None
    elif isinstance(qmon, tuple):
        qmon1 = qmon
        qmon2 = None
        fig, (ax0, ax1) = plt.subplots(1, 2)
        ax2 = None
    elif isinstance(qmon, list):
        qmon1 = qmon[0]
        qmon2 = qmon[1]
        fig = plt.figure()
        ax0 = fig.add_subplot(121)
        ax1 = fig.add_subplot(222)
        ax2 = fig.add_subplot(224)
    else:
        raise TypeError("'qmon' must be tuple, list or None.")

    ax = (ax0, ax1, ax2)
    qmon = (qmon1, qmon2)

    return fig, ax, qmon


def track_abs_init(data, qmon=None, qnorm=None, title='short'):
    """
    Prepare new figure to monitor absolute scattering patterns and specific
    qrange(s).

    Parameters
    ----------
    data : output of txs.azav.integrate1d_dataset()
        Input data
    qmon : tuple or list or None, optional
        Monitor q-range(s). If tuple, monitoring q-range is (qmon[0], qmon[1]).
        If list, each element of the list is a monitoring q-range.
        If None (default), only absolute patterns are tracked.

    Returns
    -------
    ...

    """

    fig, ax, qmon = _track_init(qmon)

    ln, sig = _track_abs_plot(data, fig, ax, qmon, init=True, qnorm=qnorm)

    folder = data['folder']

    if title is None:
        title = folder
    elif title == 'short':
        title = Path(*Path(folder).parts[-2:])
    else:
        if not isinstance(title, 'str'):
            raise TypeError("'title' must be None or str.")

    fig.suptitle(title)

    plt.tight_layout()

    return fig, ax, ln, sig


def track_diff_init(data, qmon=None, qnorm=None, track_t=None, title='short'):
    """
    Prepare new figure to monitor difference scattering patterns and specific
    qrange(s).

    Parameters
    ----------
    data : output of txs.azav.integrate1d_dataset()
        Input data
    qmon : tuple or list or None, optional
        Monitor q-range(s). If tuple, monitoring q-range is (qmon[0], qmon[1]).
        If list, each element of the list is a monitoring q-range.
        If None (default), only absolute patterns are tracked.

    Returns
    -------
    ...

    """

    fig, ax, qmon = _track_init(qmon)

    fig.set_size_inches(12, 6)

    ln, sig = _track_diff_plot(data, fig, ax, qmon, init=True, qnorm=qnorm,
                               track_t=track_t)

    folder = data['azav']['folder']

    if title is None:
        title = folder
    elif title == 'short':
        title = Path(*Path(folder).parts[-2:])
    else:
        if not isinstance(title, 'str'):
            raise TypeError("'title' must be None or str.")

    fig.suptitle(title)

    plt.tight_layout()

    plt.pause(0.1)

    return fig, ax, ln, sig


def _track_update(fig, qmon=None):
    """
    Update figure for absolute patterns tracking.
    """

    plt.figure(fig.number)

    if qmon is None:
        qmon1, qmon2 = None, None
    elif isinstance(qmon, tuple):
        qmon1, qmon2 = qmon, None
    elif isinstance(qmon, list):
        qmon1, qmon2 = qmon[0], qmon[1]
    else:
        raise TypeError("'qmon' must be tuple, list or None.")

    qmon = (qmon1, qmon2)

    return qmon


def track_abs_update(data, fig, ax, ln, sig=None, qmon=None, qnorm=None):
    """
    Update figure for absolute patterns tracking.
    """

    qmon = _track_update(fig, qmon)

    ln, sig = _track_abs_plot(
        data, fig, ax, qmon, init=False, ln=ln, qnorm=qnorm)

    return ln, sig


def track_diff_update(data, fig, ax, ln, sig=None, qmon=None, qnorm=None,
                      track_t=None):
    """
    Update figure for difference patterns tracking.
    """

    qmon = _track_update(fig, qmon)

    ln, sig = _track_diff_plot(
        data, fig, ax, qmon, init=False, ln=ln, qnorm=qnorm, track_t=track_t)

    return ln, sig


def _track_abs_plot(data, fig, ax, qmon=None, sig=None, qnorm=None, init=False,
                    ln=None, tpause=0.25):
    """

    Returns
    -------
    ln : list
        Lines to be updated.
    sig : list
        Signals calculated so far.

    """

    q = data['q']
    i = data['i']

    if qnorm is not None:
        idx = (q >= qnorm[0]) & (q <= qnorm[1])
        i = i/np.mean(i[idx, :], axis=0)

    if init:
        ln = [None, None, None]
    elif ln is None:
        raise ValueError("'l' can be None only if 'init' is True.")

    if init:
        ln[0], = ax[0].plot(q, i[:, -1])
        ax[0].set_xlabel(qlabel)
        ax[0].set_ylabel("Scattered intensity (a.u.)")
        ax[0].grid(alpha=0.7)
        ax[0].set_title("image_no=%d" % data['i'].shape[1])
        ax[0].set_xlim(0, )
        ax[0].set_ylim(0, )
    else:
        ln[0].set_xdata(q)
        ln[0].set_ydata(i[:, -1])
        ax[0].set_title("image_no=%d" % data['i'].shape[1])
        ax[0].set_xlim(0, )
        ax[0].set_ylim(0, )

    if sig is None:
        sig = (None, None)

    if qmon[0] is not None:
        sig1 = _get_qrange_sum(q, i, qmon[0], sig[0])
        if init:
            ln[1], = ax[1].plot(sig1, '.-')
            ax[1].set_xlabel('image #')
            ax[1].set_ylabel(r'sum over (%g, %g) [$\AA^{-1}$]'
                             % (qmon[0][0], qmon[0][1]))
            ax[1].grid(alpha=0.7)
        else:
            ln[1].set_xdata(range(len(sig1)))
            ln[1].set_ydata(sig1)
            ax[1].relim()  # to recompute ax.dataLim
            ax[1].autoscale_view()  # to update ax.viewLim
    else:
        sig1 = None

    if qmon[1] is not None:
        sig2 = _get_qrange_sum(q, i, qmon[1], sig[1])
        if init:
            ln[2], = ax[2].plot(sig2, '.-')
            ax[2].set_ylabel(r'sum over (%g, %g) [$\AA^{-1}$]'
                             % (qmon[1][0], qmon[1][1]))
            ax[2].grid(alpha=0.7)
        else:
            ln[2].set_xdata(range(len(sig2)))
            ln[2].set_ydata(sig2)
            ax[2].relim()  # to recompute ax.dataLim
            ax[2].autoscale_view()  # to update ax.viewLim
    else:
        sig2 = None

    sig = [sig1, sig2]

    plt.pause(tpause)

    return ln, sig


def _track_diff_plot(data, fig, ax, qmon=None, sig=None, qnorm=None,
                     track_t=None, init=False, ln=None, tpause=0.25):
    """

    Returns
    -------
    ln : list
        Lines to be updated.
    sig : list
        Signals calculated so far.

    """

    q = data['q']

    if track_t is None or track_t == 'last':
        t_idx = -1
    elif track_t == 'first':
        t_idx = 0
    else:
        if not isinstance(track_t, str):
            raise TypeError("'track_t' must be str.")
        if track_t not in data['t']:
            raise ValueError("'track_t' is not in available time-delays: " +
                             data['t'])
        t_idx = np.where(np.array(data['t']) == track_t)[0][0]

    diffs_t = data['diffs'][t_idx]

    if qnorm is not None:
        idx = (q >= qnorm[0]) & (q <= qnorm[1])
        diffs_t = diffs_t/np.mean(diffs_t[idx, :], axis=0)

    if init:
        ln = [None, None, None]
    elif ln is None:
        raise ValueError("'l' can be None only if 'init' is True.")

    if init:
        ln[0], = ax[0].plot(q, diffs_t[:, -1])
        ax[0].set_xlabel(qlabel)
        ax[0].set_ylabel("Scattering difference (a.u.)")
        ax[0].grid(alpha=0.7)
        rep_t = diffs_t.shape[1]
        ax[0].set_title("%s, rep=%d" % (data['t'][t_idx], rep_t))
        # ax[0].set_xlim(0, )
        # ax[0].set_ylim(0, )
    else:
        ln[0].set_xdata(q)
        ln[0].set_ydata(diffs_t[:, -1])
        rep_t = diffs_t.shape[1]
        ax[0].set_title("%s, rep=%d" % (data['t'][t_idx], rep_t))
        # ax[0].set_xlim(0, )
        # ax[0].set_ylim(0, )

    if sig is None:
        sig = (None, None)

    if qmon[0] is not None:
        # sig1 = _get_qrange_sum(q, diffs_t, qmon[0], sig[0])
        sig1 = _get_qrange_max(q, diffs_t, qmon[0], sig[0], abs_value=True)
        if init:
            ln[1], = ax[1].plot(sig1, '.-')
            ax[1].set_xlabel('rep #')
            ax[1].set_ylabel(r'abs(signal) (%.2g, %.2g) $\AA^{-1}$'
                             % (qmon[0][0], qmon[0][1]))
            ax[1].grid(alpha=0.7)
        else:
            ln[1].set_xdata(range(1, len(sig1)+1))
            ln[1].set_ydata(sig1)
            ax[1].relim()
            ax[1].autoscale_view()
    else:
        sig1 = None

    if qmon[1] is not None:
        # sig2 = _get_qrange_sum(q, diffs_t, qmon[1], sig[1])
        sig2 = _get_qrange_max(q, diffs_t, qmon[1], sig[1], abs_value=True)
        if init:
            ln[2], = ax[2].plot(sig2, '.-')
            ax[2].set_ylabel(r'abs(signal) (%.2g, %.2g) $\AA^{-1}$'
                             % (qmon[1][0], qmon[1][1]))
            ax[2].grid(alpha=0.7)
        else:
            ln[2].set_xdata(range(1, len(sig2)+1))
            ln[2].set_ydata(sig2)
            ax[2].relim()
            ax[2].autoscale_view()
    else:
        sig2 = None

    sig = [sig1, sig2]

    plt.pause(tpause)

    return ln, sig


def _get_qrange_sum(q, i, qrange, sig=None, sum_abs=False):
    idx = (q >= qrange[0]) & (q <= qrange[1])
    i_arr = np.array(i)
    i_arr_idx = i_arr[idx, :]
    if sum_abs:
        i_arr_idx = np.abs(i_arr_idx)
    if sig is None:
        sig = np.sum(i_arr_idx, axis=0)
    else:
        sig = np.concatenate((sig, np.sum(i_arr_idx, axis=1)))
    return sig


def _get_qrange_max(q, i, qrange, sig=None, abs_value=False):
    idx = (q >= qrange[0]) & (q <= qrange[1])
    i_arr = np.array(i)
    i_arr_idx = i_arr[idx, :]
    if abs_value:
        i_arr_idx = np.abs(i_arr_idx)
    if sig is None:
        sig = np.max(i_arr_idx, axis=0)
    else:
        sig = np.concatenate((sig, np.max(i_arr_idx, axis=1)))
    return sig


def get_qrange_mean():
    pass


def _onpick(event, fig, lines_dict):
    """Toggle visibility of legend line and corresponding plotted line."""

    legend_line = event.artist

    original_line = lines_dict[legend_line]

    visible = not original_line.get_visible()

    original_line.set_visible(visible)

    if visible:
        legend_line.set_alpha(1.0)
    else:
        legend_line.set_alpha(0.2)

    fig.canvas.draw()

    return True


def _plot(x, y, t, e=None, sel=None, every=None, hide_lines=False, cmap=None,
          lbls=None, error_bars=False, title=None, xlabel=None, ylabel=None,
          xlim=None, ylim=None, tpause=None, figsize=None, fig=None, ax=None,
          legend_ncols='auto', legend_nlines=None, map2D=False, map_clim=None,
          return_fig=False, return_ax=True, return_lines=False):
    """
    Plot time-resolved patterns.

    Patterns can be hidden or shown upon a click on the corresponding
    legend entry.

    Parameters
    ----------
    ...
    legend_ncols : int or 'auto' or None
        If 'auto' (default), the number of columns in the legend is modified
        automatically and optimized on the basis of the total number of curves.
        (if nlines is Nones, the legend will use default matplotlib settings)
        If int, the legend will have 'ncols' columns.
        If None, the legend will use default matplotlib settings.
        (same as ncols=1).
    legend_nlines : int or None
        If 'auto' (default), the number of lines in the legend is modified
        automatically and optimized to fit figure height.
        If None (default), the legend will use default matplotlib settings
        (no limitations on the number of lines is applied).
        If int, the legend will have 'nlines' lines.
    map2D : bool, optionnal
        If True, will display the patterns as a 2D map (image_number,q)
    map_clim : tupple or None
        Ignored if map2D is False
    """

    # for plot_diffs: len(t) = number of unique time-delays
    # for plot_abs: len(t) = number of time-delays (including repetitions)
    if len(t) != y.shape[1]:
        raise ValueError("'t' length must be equal to the number of " +
                         " columns of 'y'.")

    if sel is None:
        idx = range(len(t))
        if every is not None:
            idx = idx[::every]
    elif isinstance(sel, list):
        # 'sel' is a list of time-delays labels
        idx = []
        sub = [np.where(np.array(t) == s)[0] for s in sel]
        # sub is a list of arrays
        # each array contains all indeces corresponding to an element of 'sel'
        if every is not None:
            sub = [s[::every] for s in sub]
        for s in sub:
            idx.extend(s)
        add_title = ', '.join(sel)
        if title is not None:
            title += ': ' + add_title
        else:
            title = add_title
    elif isinstance(sel, slice):
        if every is not None and sel.step is None:
            sel = slice(sel.start, sel.stop, every)
        idx = range(len(t))[sel]

    if map2D:
        plt.imshow(y[:, idx], aspect="auto", clim=map_clim,
                   extent=[0, len(idx), x[-1], x[0]])
        ax.set_ylabel(xlabel)
        ax.set_xlabel("image_number")
        return

    lines = []

    if isinstance(cmap, str):
        try:
            cmap = getattr(plt.cm, cmap)
        except KeyError:
            cmap = plt.cm.prism
            print("WARNING : colormap could not be found, using default " +
                  "colormap ('prism') instead")

    for linenum, k in enumerate(idx):

        if cmap is not None:
            color = cmap(k/(len(idx)-1))
            kw = dict(color=color, label=lbls[k])
        else:
            kw = dict(label=lbls[k])

        if e is not None and error_bars:
            line = ax.errorbar(x, y[:, k], e[:, k], **kw)[0]
        else:
            line = ax.plot(x, y[:, k], **kw)[0]

        lines.append(line)

    _adjust_legend(ax, ncols=legend_ncols, nlines=legend_nlines,
                   figsize=figsize)

    if hide_lines:
        ax = plt.gca()
        for ln in ax.get_lines():
            ln.set_visible(False)
        for ln in ax.legend_.get_lines():
            ln.set_alpha(0.7)

    ax.grid(alpha=0.7)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax.set_title(title)

    _clickable_legend(ax)

    # fig.suptitle(title)

    if tpause is not None:
        plt.pause(tpause)
    else:
        plt.tight_layout()

    if return_fig:
        if return_ax:
            if return_lines:
                return fig, ax, lines
            else:
                return fig, ax
        else:
            if return_lines:
                return fig, lines
            else:
                return fig
    elif return_ax:
        if return_lines:
            return ax, lines
        else:
            return ax
    elif return_lines:
        return lines
    else:
        return None


def _clickable_legend(ax):
    """
    Makes the legend clickable.

    One click on the legend line toogles the line plot from visible to hidden.
    """

    fig = ax.figure
    lines_dict = dict()

    for legend_line, orig_line in zip(ax.legend_.get_lines(), ax.get_lines()):
        legend_line.set_picker(True)
        legend_line.set_pickradius(5)
        lines_dict[legend_line] = orig_line

    fig.canvas.mpl_connect(
        'pick_event', lambda event: _onpick(event, fig, lines_dict))


def _adjust_legend(ax, ncols=None, nlines=None, figsize=None):
    """
    Modify the horizontal size of a plot to add the legend sideways.

    Parameters
    ----------
    ax : ...
        ...
    ncols : int or 'auto' or None
        If 'auto' (default), the number of columns in the legend is modified
        automatically and optimized on the basis of the total number of curves.
        (if nlines is Nones, the legend will use default matplotlib settings)
        If int, the legend will have 'ncols' columns.
        If None, the legend will use default matplotlib settings.
    nlines : int or 'auto' or None
        If 'auto' (default), the number of lines in the legend is modified
        automatically and optimized to fit figure height.
        If None (default), the legend will use default matplotlib settings
        (no limitations on the number of lines is applied).
        If int, the legend will have 'nlines' lines.
    figsize : tuple
        (Hor, Ver) size of the figure in inches.

    """

    if nlines is not None and not isinstance(nlines, (int, str)):
        raise TypeError("'nlines' must be int or None.")

    if ncols is not None and not isinstance(ncols, (int, str)):
        raise TypeError("'ncols' must be int, str or  None.")

    def get_plot_labels(ax):

        lab = []
        for h in ax.get_lines():
            lab.append(h.get_label())

        return lab

    ncurves = len(ax.get_lines())

    labels = get_plot_labels(ax)

    fig = ax.figure

    if figsize is not None:
        fig.set_size_inches(figsize)

    def fig_height():

        return fig.get_size_inches()[1]

    def get_legend_height(nlines):

        return get_line_height() * nlines

    def get_max_lines_from_height(height):

        return floor(height / get_line_height())

    def get_line_height():

        fontsize = get_legend_fontsize()
        spacing = plt.rcParams["legend.labelspacing"]
        points_to_inches = 1 / 72

        return fontsize * points_to_inches * (1 + spacing)

    def get_legend_fontsize():

        if isinstance(plt.rcParams["legend.fontsize"], int):
            return plt.rcParams["legend.fontsize"]

        sizes = np.array(['xx-small', 'x-small', 'small',
                          'medium', 'large', 'x-large', 'xx-large'])

        scales = np.array([1/1.2**3, 1/1.2**2, 1/1.2, 1, 1.2, 1.2**2, 1.2**3])

        if isinstance(plt.rcParams["legend.fontsize"], str):

            default_size = plt.rcParams["font.size"]
            idx = np.where(sizes == plt.rcParams["legend.fontsize"])
            scale = scales[idx][0]

            return default_size * scale

    hshrink = 0.15  # factor by which the plot is shrink per legend col

    def _do_adjust(labels, ncols):

        x0, y0, width, height = ax.get_position(original=False).bounds
        fig.subplots_adjust(left=x0, right=x0+width*(1-ncols*hshrink))
        ax.legend(labels, loc=6,
                  bbox_to_anchor=(1.01, 0.5), ncol=ncols)

    if nlines is None and (ncols is None or ncols == 'auto'):
        # default location should be 'upper right'
        # to avoid covering TR-WAXS water heating in LS experiments
        ax.legend(labels, loc='upper right')
        return

    if isinstance(nlines, int):

        if ncols == 'auto':
            ncols = int(ceil(ncurves/nlines))
        elif ncols is None:
            ncols = 1
            labels = labels[:ncols*nlines]
        elif isinstance(ncols, int):
            labels = labels[:ncols*nlines]

    if nlines == 'auto':

        if ncols == 'auto':
            nlines = get_max_lines_from_height(fig_height() * 0.9)
            ncols = ceil(ncurves/nlines)

        elif isinstance(ncols, int):

            nlines = ncurves / ncols
            if get_legend_height(nlines) > fig.get_size_inches()[1] * 0.9:
                print("WARNING : Figure height is too small, number of " +
                      "entry in legend will be adjusted")
                nlines = get_max_lines_from_height(fig_height() * 0.9)
                labels = labels[:ncols*nlines]

        elif ncols is None:
            ncols = 1

    if ncols * hshrink > 0.8:
        print("""WARNING : Two many columns, custom layout not applied""")
        ax.legend(labels, loc=4)
        return

    _do_adjust(labels, ncols)


def _ref_average(diffs):
    """ Returns average of reference patterns """
    ref_i = diffs["i"][:, np.where(diffs["delays"] == diffs["ref_delay"])]
    return np.squeeze(ref_i).mean(axis=1)
