from typing import List, Optional, Tuple

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from .stadium_base import StadiumBase


class Stadium3D(StadiumBase):
    """
    A class to represent a stadium-shaped track and facilitate plots of and on its surface in 3D.
    """

    def _init_ax(self, ax: Axes3D):
        self._ax = ax
        if self._ax is None:
            self._fig = plt.figure()
            self._ax = self._fig.add_subplot(111, projection="3d", computed_zorder=False)

    def draw(
        self,
        ax: plt.Axes = None,
        s_points: int = 250,
    ) -> Optional[Tuple[plt.Figure, Axes3D]]:
        """Plot the stadium in 3D.

        Parameters
        ----------
        ax : plt.Axes
            The axis to plot on.
        s_points : int
            The number of points to use in the tangential direction.

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
        s = np.linspace(0, self.length, s_points)
        d = np.linspace(0, self.width, 3)

        s, d = np.meshgrid(s, d)
        s, d = s.flatten(), d.flatten()

        tri = matplotlib.tri.Triangulation(s, d)

        x, y, z = self._transform_xyz(s, d)

        self._ax.plot_trisurf(
            x,
            y,
            z,
            triangles=tri.triangles,
            alpha=self.surface_alpha,
            color=self.surface_color,
            edgecolor=self.surface_color,
            zorder=-2,
        )

    def _draw_infield(self, s_points=250):
        s = np.linspace(0, self.length, s_points)
        if self.infield_width == "all":
            points = np.array(
                [
                    [(0, 0, 0) for _ in s],
                    [self._transform_xyz(s_, 0) for s_ in s],
                ]
            )
            self._ax.plot_surface(
                points[:, :, 0],
                points[:, :, 1],
                points[:, :, 2],
                color=self.infield_color,
                alpha=self.infield_alpha,
                edgecolors=matplotlib.colors.to_rgba(self.infield_color, self.infield_alpha),
            )
        else:
            d = np.linspace(-1 * self.infield_width, 0, 3)

            s, d = np.meshgrid(s, d)
            s, d = s.flatten(), d.flatten()
            tri = matplotlib.tri.Triangulation(s, d)

            x, y, z = self._transform_xyz(s, d)

            self._ax.plot_trisurf(
                x,
                y,
                z,
                triangles=tri.triangles,
                alpha=self.infield_alpha,
                color=self.infield_color,
                edgecolor=self.infield_color,
                zorder=-2,
            )

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
                line[:, 2],
                color=color,
                alpha=self.lane_alpha,
                linestyle=self.lane_linestyle,
                lw=self.lane_linewidth,
                zorder=-1,
            )

    def _draw_lines(self) -> List:
        for s, color in zip(self.line_distances, self.line_colors):
            line = np.array([self._transform_xyz(s, d) for d in [0, self.width]])
            self._ax.plot(
                line[:, 0],
                line[:, 1],
                line[:, 2],
                color=color,
                alpha=self.line_alpha,
                zorder=-1,
            )

    def trajectory(
        self,
        s_: np.ndarray,
        d: np.ndarray,
        *args,
        **kwargs,
    ) -> matplotlib.lines.Line2D:
        """Plot a trajectory on the stadium.

        Parameters
        ----------
        s : np.ndarray
            The tangential position of the trajectory.
        d : np.ndarray
            The radial of the trajectory.
        args : list
            Additional positional arguments to pass to the plot
            function.
        kwargs : dict
            Additional keyword arguments to pass to the plot
            function.

        """
        points = np.array([self._transform_xyz(s_i, d_i) for s_i, d_i in zip(s_, d)])

        return self._ax.plot(points[:, 0], points[:, 1], points[:, 2], *args, **kwargs)

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
        s : np.ndarray
            The tangential position of the points.
        d : np.ndarray
            The radial of the points.
        args : list
            Additional positional arguments to pass to the scatter
            function.
        kwargs : dict
            Additional keyword arguments to pass to the scatter
            function.

        """
        points = np.array([self._transform_xyz(s_i, d_i) for s_i, d_i in zip(s_, d_)])

        return self._ax.scatter(points[:, 0], points[:, 1], points[:, 2], *args, **kwargs)
