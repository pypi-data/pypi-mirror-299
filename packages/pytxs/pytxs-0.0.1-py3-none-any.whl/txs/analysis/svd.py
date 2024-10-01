"""Singular value decomposition (SVD) of the TR-WAXS data."""


from copy import deepcopy
import numpy as np
from scipy.optimize import curve_fit

from txs.analysis.utils import get_time_delta


class SVD:
    """Compute the SVD and store results for analysis and plotting.
    
    Parameters
    ----------
    data : np.ndarray
        Assumes an array where lines correspond to q-values and columns
        correspond to measured delays.

    Examples
    --------
    Assuming `res` is the result dict from `txs.datared.datared`:

    >>> svd = SVD(res['diff_av']).run()

    """
    def __init__(self, data):
        self._data = deepcopy(data)

        # outputs
        self._result = None
        self._autocorr = None
        self._fit = None

    # make self.data read only and hide the actual data under self._data
    @property
    def data(self):
        return self._data

    def run(self):
        """Run the SVD calculation and stores result.
        
        The **result** can be obtained using the :py:func:`result` method.

        **Left and right singular vectors** can be obtained using
        the :py:func:`autocorr` method.

        The **basis patterns** can be obtained using the :py:func:`patterns`
        method.

        The **recomposed signal** can be obtained by using the 
        :py:func:`recompose` method.
        
        """
        u, s, v = np.linalg.svd(self.data, False)
        self._result = (u, s, v)
        self._compute_autocorr()

        return self

    def result(self, rank=None):
        """Returns the singular values and vectors up to `rank`.
        
        Returns
        -------
        u : 2D array
            The left-singular vectors (column-wise)
        s : 1D array
            The computed singular values arranged on the diagonal
        v : 2D array
            The right-singular vectors (row-wise)
        
        """
        rank = self._get_rank_slice(rank)
        u = self._result[0][:, rank]
        s = self._result[1][rank]
        v = self._result[2][rank]

        return u, s, v

    def autocorr(self):
        """Returns the autocorrelation of U and V singular vectors."""
        return self._autocorr

    def patterns(self, rank=None):
        """Returns the left and right basis patterns obtained from the SVD."""
        u, s, v = self.result(rank)
        out = (u @ np.diag(s), v)
        return out[0], out[1]

    def recompose(self, rank=None):
        """Recomposes the signal by computing the matrix product USV."""
        u, s, v = self.result(rank)
        return u @ np.diag(s) @ v

    def get_distance(self, other, rank=None):
        """Computes the distance from vector dot product with another SVD.
        
        For the matrices Ua and Va of this SVD, the dot products with the 
        corresponding singular vectors in matrices Ub and Vb of `other` are
        computed. Then averages are computed for dot products obtained from 
        U and V singular vectors separately.

        Parameters
        ----------
        other : :py:class:`SVD`
            Another instance of SVD.
        rank : int, optional
            The maximum rank of singular vector to be used.
            (default, None, all are used)

        Returns
        -------
        dU : float
            The average inner product value for the U singular vectors.
        dV : float
            The average inner product value for the V singular vectors.

        """
        rank = self._get_rank_slice(rank)
        dU = np.sum(self._result[0] * other._result[0], 0)
        dV = np.sum(self._result[2] * other._result[2], 1)

        dU = np.mean(dU[rank])
        dV = np.mean(dV[rank])

        return dU, dV

    def fit(self, f, xdata, vectors="v", rank=None, **kwargs):
        """Fit the selected vectors up to given rank.
        
        The `scipy.optimize.curve_fit` function is used with the provided 
        function.
        This can be used to exctract a time evolution of the sample during
        an experiment.

        Parameters
        ----------
        f : callable
            A fit function to be used (typically a decaying exponential).
        xdata : array-like
            An array containing the values for the x-axis (typically either
            q-values or experimental time).
        vectors : {'u', 'v'}, optional
            Which vectors to use. Should be either 'u' for left-singular
            vectors or 'v' for right-singular vectors.
            (default, 'v')
        rank : int, optional
            The maximum rank, or number of vectors, to fit.
            (default, None, all are used)
        kwargs : dict-like
            Additional arguments to be passed to the `scipy.optimize.curve_fit`
            method.

        Returns
        -------
        result : list of tuples (popt, perr)
            A list of outputs from `scipy.optimize.curve_fit` as tuples of 
            the form (popt, perr) for each vector in vectors.
            The covariance matrix is directly converted to errors using
            `perr = np.sqrt(np.diag(pcov))`.

        """
        u, _, v = self.result(rank)
        if vectors not in ["u", "v"]:
            raise ValueError("Argument 'vectors' should be 'u' or 'v'.")
        vectors = u.T if vectors == "u" else v

        result = [
            curve_fit(f, xdata, vector, **kwargs) for vector in vectors
        ]

        return result
    
    def maximize_autocorrelations(self, rank=(2, 10), side="left"):
        """Rotation of the SVD left or right matrix to maximize autocorrelation.

        Parameters
        ----------
        rank : {int, list, slice}, optional
            Selection of singular vectors to include in the rotation procedure.
            If an integer, it will select all vectors up to rank.
            If a 2-tuple, it will select vectors in the range defined by the 
            tuple of the form (min, max).
            If a list or slice, it will select the ranks given.
            (default, (2, 10))
        side : {'left', 'right'}, optional
            Which singular vectors to use, should be either "left" or  "right".
            (default, "left")

        """
        u, s, v = self.result()

        rank = self._get_rank_slice(rank)
        vectors = u[:, rank] if side == "left" else v[rank].T

        autocorr = []
        for vec in vectors.T:
            autocorr.append([
                np.sum(vec[1:] * other_vec[:-1]) for other_vec in vectors.T
            ])

        corr = np.array(autocorr).T
        sym_corr = (corr + corr.T) / 2
        _, eigvec = np.linalg.eigh(sym_corr)
        eigvec = eigvec[:, ::-1]

        u[:, rank] = u[:, rank] @ eigvec
        v[rank] = (v[rank].T @ eigvec).T

        self._result = (u, s, v)
        self._compute_autocorr()

        return self

    def _compute_autocorr(self):
        """Compute the autocorrelation of basis patterns and amplitude."""
        u, _, v = self.result()
        u_autocorr = np.array([
            np.sum(val[1:] * val[:-1]) for val in u.T
        ])
        v_autocorr = np.array([
            np.sum(val[1:] * val[:-1]) for val in v
        ])

        self._autocorr = (u_autocorr, v_autocorr)

    def _get_rank_slice(self, rank):
        """Helper function to process the rank argument"""
        if isinstance(rank, int):
            return slice(0, rank, 1)
        if isinstance(rank, (np.ndarray, list, set, slice)):
            return rank
        if isinstance(rank, tuple):
            return slice(rank[0], rank[1], 1)
        if rank is None:
            return slice(0, self._result[1].shape[0], 1)
        else:
            raise ValueError("Requested rank has invalid value.")


def reconstruct_corrected_signal(
    data, 
    threshold=0.6, 
    max_rank_rescale=1,
    maximize_autocorrelations=None,
    exclude=None,
):
    """Use SVD to apply corrections on data and recontruct them.
    
    Parameters
    ----------
    data : dict-like or list of dict
        A data set or a list of data set obtained from txs `datared` routine.
    threshold : float in [0, 1], optional
        Value of autocorrelation below which singular vectors are discarded.
        After a first crossing of the threshold, all subsequent vectors are
        discarded, whatever the value of their autocorrelation.
        (default, 0.6)
    max_rank_rescale : int, optional
        The maximum rank of singular vectors for which a rescaling will be done.
        The time evolution of the right-singular vectors is fitted. The fitted 
        model is then normalized and the corresponding patterns are divided
        by the normalized model.
        (default, 1)
    maximize_autocorrelation : 2-tuple, optional
        If not None, a 2-tuple giving the range of singular vector rank to be 
        rotated such that the autocorrelation is maximized in increaing order.
        (default, None)
    exclude : list of int
        If `data` is a list, `exclude` should contains the indices of data that
        should not be corrected for the kinetics.

    Returns
    -------
    corr_data : dict or list of dict
        The corrected data in the same format as the input `data`.

    """
    if not isinstance(data, list):
        data = [data]
    corr_data = [deepcopy(val) for val in data]

    if exclude is None:
        exclude = []

    for s_idx, sample in enumerate(corr_data):
        if s_idx not in exclude:
            for t_idx, delay in enumerate(sample['t']):
                tdelta = get_time_delta(sample, t_idx)
                svd = SVD(sample['diffs'][t_idx]).run()

                if maximize_autocorrelations is not None:
                    svd = svd.maximize_autocorrelations(
                        maximize_autocorrelations
                    )

                autocorr = svd.autocorr()
                keep = np.arange(autocorr[0].size)[autocorr[0] > threshold]
                print(
                    f"Keeping {keep.size} of {len(autocorr[0])} patterns "
                    f"at time delay {delay}."
                )
                u, s, v = svd.result(keep)

                if max_rank_rescale > 0:
                    f = lambda t, a, b, tau: a * np.exp(-t / tau) + b
                    fit_res = svd.fit(
                        f, 
                        tdelta, 
                        "v", 
                        rank=max_rank_rescale, 
                        p0=[1, 0, 30], 
                        maxfev=10000,
                    )
                    print(
                        f"Decay v0 at time delay {delay} -> "
                        f"{fit_res[0][0][-1]:.1f}."
                    )
                    for idx, res in enumerate(fit_res):
                        norm = f(tdelta, *res[0])
                        v[idx] /= (norm / norm[0])

                new_diffs = u @ np.diag(s) @ v
                corr_data[s_idx]['diffs'][t_idx] = new_diffs
                corr_data[s_idx]['diff_av'][:, t_idx] = np.median(new_diffs, 1)
                corr_data[s_idx]['diff_err'][:, t_idx] = (
                    np.nanstd(new_diffs, 1) / np.sqrt(new_diffs.shape[1])
                )

    return corr_data
