"""
Convenience classes and functions for RGB color manipulations
"""
import abc
from typing import Tuple, List

from matplotlib import pyplot as plt

from src.utils.plot import norm_rgb


class Color:
    """
    Convenient data structure to store colors.
    """

    def __init__(self, name: str, r: int, g: int, b: int, a: float = 1.0):
        self.name: str = name
        self.rgb: Tuple[int, int, int] = (r, g, b)
        self.rgba: Tuple[int, int, int, float] = (r, g, b, a)


class ColorManager:
    """
    A base class for all color managers.
    """

    @abc.abstractmethod
    def get(self):
        """
        A getter to the object (colors) managed by the manager.
        """
        pass

    def __iter__(self):
        """
        Make the managers iterable
        """
        return iter(self.get())

    def show(self, fig: plt.Figure = None, ax: plt.Axes = None):
        """
        Plot all the colors contained in the manager.
        """
        n = len(self.get())
        ncols = 4
        nrows = n // ncols + 1

        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(8, 1))

        # Get height and width
        X, Y = fig.get_dpi() * fig.get_size_inches()
        h = Y / (nrows + 1)
        w = X / ncols

        for i, color in enumerate(self.get()):
            col = i % ncols
            row = i // ncols
            y = Y - (row * h) - h

            xi_line = w * (col + 0.05)
            xf_line = w * (col + 0.25)
            xi_text = w * (col + 0.3)

            ax.text(
                xi_text,
                y,
                color.name,
                fontsize=12,
                horizontalalignment="left",
                verticalalignment="center",
            )

            ax.hlines(
                y + h * 0.1,
                xi_line,
                xf_line,
                color=norm_rgb(color.rgb),
                linewidth=(h * 0.6),
            )

        ax.set_xlim(0, X)
        ax.set_ylim(0, Y)
        ax.set_axis_off()

        fig.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)

        return ax


class CommonColors(ColorManager):
    """
    Colors that are common to any Theme. Common colors are constants (regardless of chosen theme):

    - `traffic_light_green`
    - `traffic_light_orange`
    - `traffic_light_red`
    """

    traffic_light_green = Color(name="traffic_light_green", r=41, g=186, b=116)
    traffic_light_orange = Color(name="traffic_light_orange", r=212, g=223, b=51)
    traffic_light_red = Color(name="traffic_light_red", r=231, g=28, b=87)

    def get(self):
        return [
            self.traffic_light_green,
            self.traffic_light_orange,
            self.traffic_light_red,
        ]


class ThemeColors(ColorManager):
    """
    A convenient data structure  holding "theme" colors. Theme colors are (regardless of chosen theme).

    Args:
        background1: for ex in the generic green theme this is mapped to color "white"
        background2: for ex in the generic green theme this is mapped to color = "off_white"
        text1: for ex in the generic green theme this is mapped to color = "dark_gray"
        text2: for ex in the generic green theme this is mapped to color = "bright_green"
        accent1: for ex in the generic green theme this is mapped to color "forest_green"
        accent2: for ex in the generic green theme this is mapped to color "jade_green"
        accent3: for ex in the generic green theme this is mapped to color "yellow"
        accent4: for ex in the generic green theme this is mapped to color "mint_green"
        accent5: for ex in the generic green theme this is mapped to color "medium_gray"
        accent6: for ex in the generic green theme this is mapped to color "true_blue"
        custom_colors: list of additional color objects to be registered in the theme. They are not mandatory.
    """

    def __init__(
        self,
        background1: Color,
        background2: Color,
        text1: Color,
        text2: Color,
        accent1: Color,
        accent2: Color,
        accent3: Color,
        accent4: Color,
        accent5: Color,
        accent6: Color,
        custom_colors: List[Color] = None,
    ):
        self.background1: Color = background1
        self.background2: Color = background2
        self.text1: Color = text1
        self.text2: Color = text2
        self.accent1: Color = accent1
        self.accent2: Color = accent2
        self.accent3: Color = accent3
        self.accent4: Color = accent4
        self.accent5: Color = accent5
        self.accent6: Color = accent6
        self.custom_colors = custom_colors

    def get(self, types: List[str] = None) -> List[Color]:
        background = [self.background1, self.background2]
        text = [self.text1, self.text2]
        accent = [
            self.accent1,
            self.accent2,
            self.accent3,
            self.accent4,
            self.accent5,
            self.accent6,
        ]
        if types is None:
            types = ["background", "text", "accent"]
        result = []
        if "background" in types:
            result += background
        if "text" in types:
            result += text
        if "accent" in types:
            result += accent

        return result


class CustomColors(ColorManager):
    def __init__(self, colors: List[Color]):
        self.colors = colors

    def get(self):
        return self.colors
