"""Functions for heating signal subtraction."""

__author__ = "Kevin Pounot"
__contact__ = "kevin.pounot@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "27/09/2022"


import numpy as np
from copy import deepcopy

from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

import matplotlib.pyplot as plt


def remove_heating(data, ref, qlim=(1.5, 2.2), verbose=True):
    """Removes the water heating signal using a fit in the given q-range.

    Three cases are currently handled:
        - only one time delay is present in `ref`, then the curve is scaled
            and used for subtraction of all time delays in `data`.
        - two time delays are present in `ref`, then a linear combination of
            these two curves is used to fit the time delays in `data` and used
            for subtraction.
        - the number of time delays in `data` and `ref` matches exactly, then
            the time delays in `ref` are scaled to the corresponding curves in
            `data` and subtracted.

    Parameters
    ----------
    data : dict
        A dictionary as obtained from :py:func:`txs.datared.datared` function.
    ref : dict
        A dictionary as obtained from :py:func:`txs.datared.datared` function.
    qlim : 2-tuple, optional
        Defines the lower and upper limits of the momentum transfer q-region
        that is used to fit the reference on the data patterns.
        (default, (1.5, 2.2))
    verbose : bool, optional
        If True, prints information about the scaling factors used.
        (default, True)

    Returns
    -------
    out : dict
        A deep copy of the `data` where heating signal has been subtracted.

    """
    out = deepcopy(data)

    q = data['q']
    qmask = (q >= qlim[0]) & (q <= qlim[1])
    t = data['t']
    ref_t = ref['t']

    if len(ref_t) == 1:
        mode = 'single'
    elif len(ref_t) == 2:
        mode = 'pair'
    elif np.all(np.isin(t, ref_t)):
        mode = 'exact'
    else:
        raise ValueError(
            "The number of time delays in the heating signal data set should" +
            " either be 1, 2 or all delays from the sample should be " +
            "present in the heating reference data set."
        )

    ref_heating = interp1d(
        ref['q'],
        ref['diff_av'],
        axis=0,
        bounds_error=False,
        fill_value='extrapolate',
    )

    for d_idx, diff in enumerate(data['diff_av'].T):
        if mode == 'single':
            heating = ref['diff_av'][:, 0]
            heating = interp1d(
                ref['q'], heating, bounds_error=False, fill_value="extrapolate"
            )(q)
            fitfunc = lambda _, scale: scale * q[qmask] * heating[qmask]
        if mode == 'pair':
            heating1 = ref['diff_av'][:, 0]
            heating2 = ref['diff_av'][:, 1]
            heating1 = interp1d(
                ref['q'], heating1, bounds_error=False, fill_value="extrapolate"
            )(q)
            heating2 = interp1d(
                ref['q'], heating2, bounds_error=False, fill_value="extrapolate"
            )(q)
            fitfunc = lambda _, s1, s2: (
                s1 * q[qmask] * heating1[qmask] +
                s2 * q[qmask] * heating2[qmask]
            )
        if mode == 'exact':
            t_idx = ref_t.index(t[d_idx])
            heating = ref['diff_av'][:, t_idx]
            heating = interp1d(
                ref['q'], heating, bounds_error=False, fill_value="extrapolate"
            )(q)
            fitfunc = lambda _, scale: scale * q[qmask] * heating[qmask]

        # fit the reference amplitude to the pattern first
        popt, _ = curve_fit(
            fitfunc,
            q[qmask],
            q[qmask] * diff[qmask],
            bounds=(0., np.inf),
            ftol=1e-15,
            maxfev=10000,
        )
        if verbose:
            print(
                f"At time delay {t[d_idx]}, scale factor: {np.round(popt, 2)}."
            )

        # perform the subtraction
        if mode == 'pair':
            heating = popt[0] * heating1 + popt[1] * heating2
        else:
            heating = popt[0] * heating

        out['diff_av'][:, d_idx] = diff - heating

    return out


def generate_thermal_response_curves(data, delay_short, delay_long, cp, cv):
    """Generate the two curves of the thermal response of the solvent.

    The solvent heating signal is described using the following:

    .. math::

        \\Delta S(Q, t) =
        \\frac{\\partial S(Q, t)}{\\partial T}\\bigg\\lvert_{\\rho}\\Delta T(t) +
        \\frac{\\partial S(Q, t)}{\\partial \\rho}\\bigg\\lvert_T\\Delta \\rho(t)

    where S(Q, t) is the measured signal, T is the temperature in the heated
    volume and :math:`\\rho` is the solvent density [1]_.

    The provided curves corresponds to each term summed on the right-hand side.
    Typically,
    :math:`\\frac{\\partial S(Q, t)}{\\partial T}\\bigg\\lvert_{\\rho}\\Delta T(t)`
    is measured at short time scale (100 ps) before the density drop response
    to the temperature jump.
    The term
    :math:`\\frac{\\partial S(Q, t)}{\\partial \\rho}\\bigg\\lvert_T\\Delta \\rho(t)`
    is obtained using the following (assuming 100 ps delay for the first term):

    .. math::

        \\frac{\\partial S(Q, t)}{\\partial \\rho}\\bigg\\lvert_T\\Delta
        \\rho(t_{long}) =
            \\Delta S(t_{long}) - \\frac{C_V}{C_p} \\Delta S(100 ps)

    Parameters
    ----------
    data : dict-like
        A dataset of the type returned by :py:func:`txs.datared.datared`
        corresponding to the heating signal at short time delay
    delay_short : str
        The time delay for the heating signal during temperature jump
        (short one, typically 100 ps).
    delay_long : str
        The time delay for the heating signal during density drop
        (long one, typically 1 :math:`\mu` s).
    cp : float
        The constant-pressure heat capacity of the solvent.
    cv : float
        The constant-volume heat capacity of the solvent.

    References
    ----------
    .. [1] Kjær, K. S. et al. Phys. Chem. Chem. Phys. 15, 15003–15016 (2013)

    """
    out = deepcopy(data)

    delays = list(data['t'])
    diff_av = data['diff_av']
    diff_err = data['diff_err']

    short_idx = delays.index(delay_short)
    long_idx = delays.index(delay_long)

    short = diff_av[:, short_idx]
    short_err = diff_err[:, short_idx]
    long = diff_av[:, long_idx]
    long_err = diff_err[:, long_idx]

    long = long - cv / cp * short
    long_err = np.sqrt(
        long_err ** 2 +
        (cv / cp) ** 2 * short_err ** 2 -
        2 * long_err * short_err
    )

    out['diff_av'][:, short_idx] = short
    out['diff_av'][:, long_idx] = long
    out['diff_err'][:, long_idx] = long_err

    out['diff_av'] = out['diff_av'][:, [short_idx, long_idx]]
    out['diff_err'] = out['diff_err'][:, [short_idx, long_idx]]
    out['t'] = [delay_short, delay_long]

    return out


def generate_heating_reference(data, delays, plot=False):
    """Generate a reference curve for heating signal.

    Parameters
    ----------
    data : dict
        A dictionary as obtained from :py:func:`txs.datared.datared`.
    delays : str or list of str
        Time delay(s) to be used to create the reference curve.
    threshold : float
        Used to filter out data that are essentially noise. The integral is
        computed for each time delay and the data for which the integral is
        above the threshold are kept for averaging.

    Returns
    -------
    ref : array-like (1D)
        A 1D array containing the reference curve for the heating signal.

    """
    ref = deepcopy(data)
    q = data['q']

    if isinstance(delays, str):
        delays = [delays]

    keep_mask = np.array(
        [1 if val in delays else 0 for val in data['t']]
    ).astype(bool)

    ref['diff_av'] = np.mean(data['diff_av'][:, keep_mask], 1)[:, None]
    ref['diff_err'] = np.sqrt(
        np.mean(data['diff_err'][:, keep_mask] ** 2, 1)
    )[:, None]
    ref['t'] = [delays[0]]

    if plot:
        fig, ax = plt.subplots(2, 1)

        ax[0].plot(q, q[:, None] * data['diff_av'])
        ax[0].set_xlabel("momentum transfer q [$\\rm \AA^{-1}$]")
        ax[0].set_ylabel("S(q) [arb. units]")
        ax[0].legend(data['t'], loc=2, bbox_to_anchor=(1, 1))
        ax[0].grid(alpha=0.2)

        ax[1].plot(q, q * ref['diff_av'].squeeze())
        ax[1].set_xlabel("momentum transfer q [$\\rm \AA^{-1}$]")
        ax[1].set_ylabel("S(q) [arb. units]")
        ax[1].grid(alpha=0.2)

        ax[0].set_title("reference heating signal")
        fig.tight_layout()

    return ref
