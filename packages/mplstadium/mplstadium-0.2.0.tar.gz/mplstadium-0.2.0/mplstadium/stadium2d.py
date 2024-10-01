from typing import List, Optional, Tuple

import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from .stadium_base import StadiumBase


class Stadium2D(StadiumBase):
    """
    A class to represent a stadium-shaped track and facilitate plots of and on its surface in 2D.
    """

    def _init_ax(self, ax: plt.Axes):
        self._ax = ax
        if self._ax is None:
            self._fig = plt.figure()
            self._ax = self._fig.add_subplot(111)

    def draw(
        self,
        ax: plt.Axes = None,
        s_points: int = 250,
    ) -> Optional[Tuple[plt.Figure, plt.Axes]]:
        """Plot the stadium in 2D.

        Parameters
        ----------
        ax : plt.Axes
            The axis to plot on.
        s_points: int
            Number of points to plot in the tangential direction

        """

        self._init_ax(ax)

        self._draw_stadium(s_points)
        self._draw_infield(s_points)
        self._draw_lanes()
        self._draw_lines()

        if self._fig:
            return self._fig, self._ax

    def _draw_stadium(
        self,
        s_points=250,
    ):
        all_s = np.linspace(0, self.length, s_points)

        outer = np.array([self._transform_xyz(s, self.width) for s in all_s])
        inner = np.array([self._transform_xyz(s, 0) for s in all_s])

        self._ax.fill(outer[:, 0], outer[:, 1], color=self.surface_color, alpha=self.surface_alpha)
        self._ax.fill(inner[:, 0], inner[:, 1], color="white")

    def _draw_infield(self, s_points=250):
        all_s = np.linspace(0, self.length, s_points)

        outer = np.array([self._transform_xyz(s, 0) for s in all_s])
        self._ax.fill(outer[:, 0], outer[:, 1], color=self.infield_color, alpha=self.infield_alpha)

        if self.infield_width != "all":
            inner = np.array([self._transform_xyz(s, -1 * self.infield_width) for s in all_s])
            self._ax.fill(inner[:, 0], inner[:, 1], color="white")

    def _draw_lanes(self, s_points=250) -> List:
        all_s = np.linspace(0, self.length, s_points)

        lane_positions = [0]
        for w in self.lane_widths:
            lane_positions.append(lane_positions[-1] + w)

        for d, color in zip(lane_positions, self.lane_colors):
            line = np.array([self._transform_xyz(s, d) for s in all_s])
            self._ax.plot(
                line[:, 0],
                line[:, 1],
                color=color,
                alpha=self.lane_alpha,
                linestyle=self.lane_linestyle,
                lw=self.lane_linewidth,
            )

    def _draw_lines(self) -> List:
        for s, color in zip(self.line_distances, self.line_colors):
            line = np.array([self._transform_xyz(s, d) for d in [0, self.width]])
            self._ax.plot(
                line[:, 0],
                line[:, 1],
                color=color,
                alpha=self.line_alpha,
            )

    def trajectory(
        self,
        s_: np.ndarray,
        d_: np.ndarray,
        *args,
        **kwargs,
    ) -> matplotlib.lines.Line2D:
        """Plot a trajectory on the stadium.

        Parameters
        ----------
        s_ : np.ndarray
            The tangential position of the trajectory.
        d_ : np.ndarray
            The radial of the trajectory.
        args : list
            Additional positional arguments to pass to the plot
            function.
        kwargs : dict
            Additional keyword arguments to pass to the plot
            function.

        """
        points = np.array([self._transform_xyz(s_i, d_i) for s_i, d_i in zip(s_, d_)])

        return self._ax.plot(points[:, 0], points[:, 1], *args, **kwargs)

    def scatter(
        self,
        s_: np.ndarray,
        d_: np.ndarray,
        *args,
        **kwargs,
    ) -> matplotlib.collections.PathCollection:
        """Scatter points on the stadium.

        Parameters
        ----------
        s_ : np.ndarray
            The tangential position of the points.
        d_ : np.ndarray
            The radial of the points.
        args : list
            Additional positional arguments to pass to the scatter
            function.
        kwargs : dict
            Additional keyword arguments to pass to the scatter
            function.

        """
        points = np.array([self._transform_xyz(s_i, d_i) for s_i, d_i in zip(s_, d_)])

        return self._ax.scatter(points[:, 0], points[:, 1], *args, **kwargs)
