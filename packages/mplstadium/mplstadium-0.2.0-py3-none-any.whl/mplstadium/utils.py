from .stadium2d import Stadium2D
from .stadium3d import Stadium3D


class OlympicVelodrome2D(Stadium2D):
    """
    Wrapper class for an Olympic Velodrome in 2D.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            length=250,
            radius=24.37,
            width=8,
            straight_banking=12,
            curve_banking=45,
            lane_widths=[0.7, 3.3],
            lane_colors=["black", "red", "blue"],
            surface_color="peru",
            surface_alpha=0.5,
            infield_width=2,
            infield_color="blue",
            infield_alpha=0.3,
        )


class OlympicVelodrome3D(Stadium3D):
    """
    Wrapper class for an Olympic Velodrome in 3D.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            length=250,
            radius=24.37,
            width=8,
            straight_banking=12,
            curve_banking=45,
            lane_widths=[0.7, 3.3],
            lane_colors=["black", "red", "blue"],
            surface_color="peru",
            surface_alpha=0.5,
            infield_width=2,
            infield_color="blue",
            infield_alpha=0.3,
        )


class OutdoorAthleticsTrack2D(Stadium2D):
    """
    Wrapper class for an Outdoor Athletics Track in 2D.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            length=400,
            radius=36.5,
            width=10,
            straight_banking=0,
            curve_banking=0,
            lane_widths=[1.25] * 8,
            lane_colors=["white"] * 9,
            line_distances=[42.66, 242.66],
            line_colors=["white"] * 2,
        )


class OutdoorAthleticsTrack3D(Stadium3D):
    """
    Wrapper class for an Outdoor Athletics Track in 3D.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            length=400,
            radius=36.5,
            width=10,
            straight_banking=0,
            curve_banking=0,
            lane_widths=[1.25] * 8,
            lane_colors=["white"] * 9,
            line_distances=[42.66, 242.66],
            line_colors=["white"] * 2,
        )


class IndoorAthleticsTrack2D(Stadium2D):
    """
    Wrapper class for an Indoor Athletics Track in 2D.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            length=200,
            radius=18.5,
            width=7.5,
            straight_banking=0,
            curve_banking=10,
            lane_widths=[1.25] * 6,
            lane_colors=["white"] * 7,
        )


class IndoorAthleticsTrack3D(Stadium3D):
    """
    Wrapper class for an Indoor Athletics Track in 3D.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            length=200,
            radius=18.5,
            width=7.5,
            straight_banking=0,
            curve_banking=10,
            lane_widths=[1.25] * 6,
            lane_colors=["white"] * 7,
        )
