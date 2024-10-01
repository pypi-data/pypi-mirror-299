"""Plotting functions to ease the analysis process.

.. warning::
    These functions make use of ipywidgets and are meant to be used within a
    Jupyter notebook with the 'magic' `%matplotlib widget`.

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from ipywidgets import widgets

from txs.heating import remove_heating
from txs.utils import str2t
from txs.analysis.utils import sort_delays
from txs.analysis.svd import SVD


def plot_dataset(
        data, 
        sample_names, 
        heating=None, 
        heating_qlim=(1.6, 2), 
        q_scaled=False
):
    """Plot the processed data for each time delays."""
    fig, ax = plt.subplots(figsize=(10, 6))

    incr = 0.001
    ylabel = 'q' if q_scaled else ''

    delays = {}
    for s_idx, sample in enumerate(data):
        for _, delay in enumerate(sample['t']):
            if delay not in delays:
                delays[delay] = []
            delays[delay].append(s_idx)

    delay_slider = widgets.IntSlider( 
        min=0, max=len(delays.keys()) - 1, value=0, step=1, description="delay" 
    )

    cmap = get_cmap('tab10')

    @widgets.interact(delay=delay_slider)
    def update_plot(delay):
        ax.clear()

        t_key = list(delays.keys())[delay]    

        for idx, s_idx in enumerate(delays[t_key]):
            q = data[s_idx]['q']
            q_scale = q if q_scaled else np.ones_like(q)

            t_idx = list(data[s_idx]['t']).index(t_key)
            ax.errorbar(
                q,
                q_scale * data[s_idx]['diff_av'][:, t_idx] + idx * incr,
                label=sample_names[s_idx],
                color=cmap(idx),
                alpha=0.4 if heating is not None else 1,
            )

            if heating is not None:
                red2 = remove_heating(
                    data[s_idx], heating, qlim=heating_qlim, verbose=False
                )
                ax.errorbar(
                    q,
                    q_scale * red2['diff_av'][:, t_idx] + idx * incr,
                    color=cmap(idx),
                )

            ax.axhline(idx * incr, ls=":", alpha=0.2)

        ax.set_xlabel("q [$\\rm \AA^{-1}$]")
        ax.set_ylabel(f"{ylabel}S(q)")
        ax.legend(loc=2, bbox_to_anchor=(1, 1))
        ax.set_title(
            f"$\\rm \Delta t$ = {t_key}\n" +
            "semi-transparent -> " if heating is not None else "" +
            "no heating removal" if heating is not None else ""
        )

        ax.relim()
        ax.autoscale_view()
        fig.tight_layout()

    update_plot(0)


def plot_svd_analysis(
        data, 
        heating=None, 
        heating_qlim=(1.8, 2), 
        q_scaled=False,
        include_ref=False,
        figsize=(10, 10),
        plot_grid=None,
        ref_delays=None,
):
    """Performs and plot a SVD analysis on the provided data."""
    if heating is not None:
        data = remove_heating(data, heating, qlim=heating_qlim, verbose=False)

    q = data['q']
    q_scale = q if q_scaled else np.ones_like(q)
    ylabel = "q" if q_scaled else ""

    data = sort_delays(data, ref_delays=ref_delays, include_ref=include_ref)

    t = str2t(data['t'])

    svd = SVD(data['diff_av']).run()

    fig = plt.figure(figsize=figsize)
    ax = []
    if plot_grid is None:
        gs = plt.GridSpec(3, 2, height_ratios=(1, 1, 1))
    else:
        gs = plot_grid
    ax.append(fig.add_subplot(gs[0, :]))
    ax.append(fig.add_subplot(gs[1, :], sharex=ax[0]))
    ax.append(fig.add_subplot(gs[2, 0]))
    ax.append(fig.add_subplot(gs[2, 1]))
    cursor = Cursor(ax[:2])
    cmap = get_cmap('gnuplot')

    svd_rank = widgets.IntSlider(
        min=0,
        max=10,
        step=1,
        value=0,
        description="svd rank",
    )

    incr_slider = widgets.FloatSlider( 
        min=0, max=0.01, value=0.0005, step=0.0002, description="increment" 
    )

    leg_lines = {}
    def on_pick(event):
        legline = event.artist
        for line in leg_lines[legline]:
            visible = not line.get_visible()
            line.set_visible(visible)
        legline.set_alpha(1.0 if visible else 0.2)

    @widgets.interact(rank=svd_rank, incr=incr_slider)
    def update_plot(rank, incr, keep_lims=True):
        ax0_lims = (ax[0].get_xlim(), ax[0].get_ylim())
        ax1_lims = (ax[1].get_xlim(), ax[1].get_ylim())
        ax[0].clear()
        
        correlations = svd.autocorr()
        if rank == 0:
            rank = np.arange(correlations[0].size)[correlations[0] > 0.5]

        lines = []
        leg_lines.clear()
        for idx, val in reversed(list(enumerate(data['diff_av'].T))):
            line_group = []
            line = ax[0].plot(
                data['q'],
                q_scale * val + incr * idx,
                # savgol_filter(val, 15, 3) + incr * idx,
                color=cmap(idx / data['diff_av'].shape[1]),
                alpha=0.4
            )
            line_group.append(line[0])

            line = ax[0].plot(
                data['q'],
                q_scale * svd.recompose(rank)[:, idx] + incr * idx,
                # savgol_filter(svd.recompose(rank)[:, idx], 15, 3) + incr * idx,
                color=cmap(idx / data['diff_av'].shape[1]),
                label=data['t'][idx],
                ls='--'
            )
            line_group.append(line[0])
            line = ax[0].axhline(incr * idx, color='black', ls=':', alpha=0.2)
            line_group.append(line)
        
            lines.append(line_group)

        ax[0].set_xlabel("q [$\\rm \AA^{-1}$]")
        ax[0].set_ylabel(f'$\\rm {ylabel}\Delta S(q)$ ')
        ax[0].grid(alpha=0.2)
        if keep_lims:
            ax[0].set_xlim(ax0_lims[0])
            ax[0].set_ylim(ax0_lims[1])
        leg = ax[0].legend(loc=2, bbox_to_anchor=(1, 1), fontsize=10)

        for legline, origlines in zip(leg.get_lines(), lines):
            legline.set_picker(True)
            legline.set_pickradius(10)
            leg_lines[legline] = origlines

        patterns = svd.patterns(rank)
        ax[1].clear()
        for idx, val in enumerate(patterns[0].T):
            ax[1].plot(
                data['q'],
                q_scale * val + incr * idx,
                # savgol_filter(val, 15, 3) + incr * idx
            )
            ax[1].axhline(incr * idx, color='black', ls=':', alpha=0.2)
        ax[1].set_xlabel("q [$\\rm \AA^{-1}$]")
        ax[1].set_ylabel(f'{ylabel}U vectors\n[arb. units]')
        ax[1].grid(alpha=0.2)
        if keep_lims:
            ax[1].set_xlim(ax1_lims[0])
            ax[1].set_ylim(ax1_lims[1])
        ax[1].autoscale_view()

        ax[2].clear()

        # patterns = patterns[1].T / np.max(np.abs(patterns[1])) + 0.5
        patterns = patterns[1].T
        ax[2].plot(
            t,
            patterns,
        )
        ax[2].set_xlabel('time')
        ax[2].set_ylabel('V vectors\n[arb. units]')
        # ax[2].set_xticklabels(delays, rotation=-45, ha='left')
        ax[2].grid(alpha=0.2)
        ax[2].axhline(0, color='black', ls=':')
        ax[2].relim()
        ax[2].autoscale_view()

        ax[3].clear()
        ax[3].plot(correlations[0], marker='o', label='U vectors')
        ax[3].plot(correlations[1], marker='^', label='V vectors')
        ax[3].axhline(0.5, color='black', ls=':')
        ax[3].set_xlabel('rank')
        ax[3].set_ylabel('autocorrelations\n[arb. units]')
        ax[3].grid(alpha=0.2)
        ax[3].relim()
        ax[3].autoscale_view()
        ax[3].legend(loc=2, bbox_to_anchor=(1, 1))

        cursor.drawline()

    update_plot(0, 0.0005, False)

    fig.tight_layout()
    fig.canvas.mpl_connect('motion_notify_event', cursor.on_mouse_move)
    fig.canvas.mpl_connect('button_press_event', cursor.on_mouse_press)
    fig.canvas.mpl_connect('pick_event', on_pick)

    return data, svd


class Cursor:
    """A vertical line cursor."""
    def __init__(self, ax):
        if not isinstance(ax, list):
            ax = [ax]
        self.ax = ax
        self.vertical_line = []
        self.persistent_lines = []

        self.drawline()

    def drawline(self):
        self.vertical_line = [
            val.axvline(color='k', lw=0.8, ls='--', alpha=0.6) 
            for val in self.ax
        ]

    def on_mouse_move(self, event):
        if not event.inaxes:
            for line in self.vertical_line:
                line.set_visible(False)
            pass
        else:
            for line in self.vertical_line:
                line.set_visible(True)
            x = event.xdata
            # update the line positions
            for idx, val in enumerate(self.ax):
                self.vertical_line[idx].set_xdata([x])
                # val.figure.canvas.draw()

    def on_mouse_press(self, event):
        if not event.inaxes:
            pass
        else:
            x = event.xdata
            side = event.button
            if side == 1:
                for val in self.ax:
                    line = val.axvline(x, color='k', lw=0.8, ls='--', alpha=0.6)
                    self.persistent_lines.append(line)
            if side == 3:
                for line in self.persistent_lines:
                    line.remove()
