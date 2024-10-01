import abc
from typing import List, Tuple, Union

import matplotlib
import numpy as np
from matplotlib import pyplot as plt


class StadiumBase(abc.ABC):
    """

    An abstract base class to represent a stadium-shaped track and facilitate plots of and on its surface.

    Attributes:
    ----------
    length : float
        The length of the inner line of the stadium.
    radius : float
        The radius of the corners of the stadium.
    width : float
        The width of the stadium.
    straight_banking : float
        The banking angle (deg) of the straight sections of the stadium.
    curve_banking : float
        The banking angle (deg) of the curved sections of the stadium.
    lane_widths : Iterable[float] = [1]
        Optional. Widths for each lane of the stadium. Does not have to sum to the total width
    lane_colors : Iterable[str] = ["black", "black"],
        Optional. Lane line colours, including the inner and outer lane lines.
        Must have length equal to len(lane_widths) + 1
    lane_alpha : float = 1.0
        Optional. Alpha value of the lane lines.
    lane_linestyle : str = "-"
        Optional. Linestyle of the lane lines.
    lane_linewidth : float
        Optional. Linewidth of the lane lines.
    line_distances : Iterable[float] = []
        Optional. Distances of the radial lines on the stadium.
    line_colors : Iterable[str] = []
        Optional. Colors of the distance lines. Must be of equal length to line_distances.
    line_alpha : float = 1.0
        Optional. Alpha value of the radial distance lines
    surface_color : str = "blue"
        Optional. Surface color of the stadium
    surface_alpha : float = 0.5
        Optional. Surface alpha of the stadium.
        Note that alpha near one will mean lines and scatters are difficult to see.
    infield_color : str = "white"
        Optional. Color of the infield area within the stadium.
    infield_alpha : str
        Optional. Alpha of the infield area.
    infield_width : float | "all" = "all"
        Optional. Width of the infield, or "all" for full infield area.

    """

    def __init__(
        self,
        length: float,
        radius: float,
        width: float,
        straight_banking: float,
        curve_banking: float,
        lane_widths: tuple[float] = (1,),
        lane_colors: tuple[str] = ("black", "black"),
        lane_alpha: float = 1,
        lane_linestyle: str = "-",
        lane_linewidth: float = 1,
        line_distances: tuple[float] = (),
        line_colors: tuple[str] = (),
        line_alpha: float = 1,
        surface_color: str = "blue",
        surface_alpha: float = 1,
        infield_color: str = "white",
        infield_alpha: float = 1,
        infield_width: Union[float, str] = "all",
    ):
        assert len(lane_colors) == len(lane_widths) + 1, "Must have one more lane colors than lane widths"
        assert len(line_distances) == len(line_colors), "Must have same number of line distances and line colors"
        assert isinstance(infield_width, (float, int)) or infield_width == "all", 'Infield width must be float or "all"'

        self.length = length
        self.radius = radius
        self.width = width
        self.straight_banking = straight_banking
        self.curve_banking = curve_banking
        self.lane_widths = lane_widths
        self.lane_colors = lane_colors
        self.lane_alpha = lane_alpha
        self.lane_linestyle = lane_linestyle
        self.lane_linewidth = lane_linewidth
        self.line_distances = line_distances
        self.line_colors = line_colors
        self.line_alpha = line_alpha
        self.surface_color = surface_color
        self.surface_alpha = surface_alpha
        self.infield_color = infield_color
        self.infield_alpha = infield_alpha
        self.infield_width = infield_width

        self._q_straight: float = (self.length - 2 * np.pi * self.radius) / 4
        self._ax: plt.Axes = None
        self._fig: plt.Figure = None

    def _step_section(
        self,
        start: float,
        end: float,
        f: callable,
    ):
        def _step(s, d_xy, d_z):
            return np.heaviside(s - start, 1) * f(s, d_xy, d_z) - np.heaviside(s - end, 1) * f(s, d_xy, d_z)

        return _step

    def _banking(self, s, d) -> float:
        multiplier = np.heaviside(d, 1)
        return (
            multiplier
            * np.pi
            * (
                ((self.straight_banking + self.curve_banking) / 2)
                - (self.curve_banking - self.straight_banking) / 2 * np.cos(4 * (s / self.length) * np.pi)
            )
            / 180
        )

    def _straight_1(self, s, d_xy, d_z) -> Tuple[float, float, float]:
        return np.array([s, -1 * (self.radius + d_xy), d_z])

    def _curve_1(self, s, d_xy, d_z) -> Tuple[float, float, float]:
        angle = (s - self._q_straight) / self.radius
        return np.array(
            [self._q_straight + (self.radius + d_xy) * np.sin(angle), -1 * (self.radius + d_xy) * np.cos(angle), d_z]
        )

    def straight_2(self, s, d_xy, d_z) -> Tuple[float, float, float]:
        return np.array([2 * self._q_straight + np.pi * self.radius - s, self.radius + d_xy, d_z])

    def curve_2(self, s, d_xy, d_z) -> Tuple[float, float, float]:
        angle = (s - (3 * self._q_straight + np.pi * self.radius)) / self.radius
        return np.array(
            [-1 * self._q_straight - (self.radius + d_xy) * np.sin(angle), (self.radius + d_xy) * np.cos(angle), d_z]
        )

    def straight_3(self, s, d_xy, d_z) -> Tuple[float, float, float]:
        return np.array([s - 4 * self._q_straight - 2 * np.pi * self.radius, -1 * (self.radius + d_xy), d_z])

    def _transform_xyz(self, s, d):
        s = s % self.length
        banking_angle = self._banking(s, d)
        d_xy = d * np.cos(banking_angle)
        d_z = d * np.sin(banking_angle)

        steps = [
            0,
            self._q_straight,
            self._q_straight + np.pi * self.radius,
            3 * self._q_straight + np.pi * self.radius,
            3 * self._q_straight + 2 * np.pi * self.radius,
            self.length,
        ]

        section_functions = [self._straight_1, self._curve_1, self.straight_2, self.curve_2, self.straight_3]

        sections = [self._step_section(steps[i], steps[i + 1], section_functions[i]) for i, _ in enumerate(steps[:-1])]

        return np.sum([section(s, d_xy, d_z) for section in sections], axis=0)

    @abc.abstractmethod
    def _init_ax(self, ax: plt.Axes):
        pass

    @abc.abstractmethod
    def draw(self) -> Tuple[plt.Figure, plt.Axes]:
        pass

    @abc.abstractmethod
    def _draw_stadium(self):
        pass

    @abc.abstractmethod
    def _draw_lanes(self) -> List[matplotlib.lines.Line2D]:
        pass

    @abc.abstractmethod
    def _draw_infield(self) -> List[matplotlib.patches.Polygon]:
        pass

    @abc.abstractmethod
    def _draw_lines(self) -> List[matplotlib.lines.Line2D]:
        pass

    @abc.abstractmethod
    def trajectory(self) -> matplotlib.lines.Line2D:
        pass

    @abc.abstractmethod
    def scatter(self):
        pass
