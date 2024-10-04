import functools
from typing import Dict, List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib as mpl
from matplotlib import colors as mcolors
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.font_manager import FontManager

from src import log
from src.constants.sizes import SIZES
from src.themes.common.colors import (
    Color,
    CommonColors,
    ThemeColors,
    CustomColors,
)
from src.utils.plot import (
    lighten_color,
    norm_rgb,
    darken_color,
    reverse_colormap,
    palplot_discrete,
    palplot_continuous,
)


class Theme:
    """
    A class generating a complete Matplotlib theme from basic color inputs. A Theme is defined by a couple of mandatory
    colors like `text1` or `accent3` used in PowerPoint presentations and a font. From that, the Theme objects
    automatically constructs colormaps that can then be used in plots.

    Args:
        name: a name for the theme, e.g. "green"
        background1: mandatory theme color
        background2: mandatory theme color
        text1: mandatory theme color
        text2: mandatory theme color
        accent1: mandatory theme color
        accent2: mandatory theme color
        accent3: mandatory theme color
        accent4: mandatory theme color
        accent5: mandatory theme color
        accent6: mandatory theme color
        default_red: mandatory theme color (usually equal to one of the accent colors listed before)
        default_green: mandatory theme color (usually equal to one of the accent colors listed before)
        default_blue: mandatory theme color (usually equal to one of the accent colors listed before)
        default_yellow: mandatory theme color (usually equal to one of the accent colors listed before)
        font: Font to use for the plots, default="Trebuchet MS"

    Returns:
        self: an instance of self

    Examples:

        To create a new theme, use the following syntax:

        .. code-block:: python
            :linenos:

            from src.themes.template import Color, Theme

            default_red = Color("magenta", 231, 28, 87)
            default_green = Color("bright_green", 41, 186, 116)
            default_blue = Color("true_blue", 41, 94, 126)
            default_yellow = Color("yellow", 212, 223, 51)

            my_theme = Theme(
                name="my-theme",
                background1=Color("white", 255, 255, 255),
                background2=Color("off_white", 242, 242, 242),
                text1=Color("dark_gray", 87, 87, 87),
                text2=default_green,
                accent1=Color("forest_green", 3, 82, 45),
                accent2=Color("jade_green", 25, 122, 86),
                accent3=default_yellow,
                accent4=Color("mint_green", 62, 173, 146),
                accent5=Color("medium_gray", 110, 111, 115),
                accent6=default_blue,
                default_blue=default_blue,
                default_green=default_green,
                default_yellow=default_yellow,
                default_red=default_red,
                font="Trebuchet MS",
            )

            my_theme.set()

        Once `set()` as been called, all the colors and colormaps in the theme will become available as regular
        Matplotlib colors and cmaps. To list all the colors and colormaps contained in the theme, one can simply do:

        .. code-block:: python
            :linenos:

            my_theme.show()
    """

    def __init__(
        self,
        name: str,
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
        default_red: Color,
        default_green: Color,
        default_blue: Color,
        default_yellow: Color,
        font: str = "Trebuchet MS",
        custom_colors=None,
    ):
        self.name = name
        self._theme_colors = ThemeColors(
            background1,
            background2,
            text1,
            text2,
            accent1,
            accent2,
            accent3,
            accent4,
            accent5,
            accent6,
        )
        self._custom_colors = CustomColors([]) if custom_colors is None else CustomColors(custom_colors)
        self.default_red = default_red
        self.default_green = default_green
        self.default_blue = default_blue
        self.default_yellow = default_yellow
        self.font = font

    @property
    @functools.lru_cache()
    def theme_colors(self) -> ThemeColors:
        """
        A color manager holding "theme" colors. Theme colors are (regardless of chosen theme):
        - background1 = colors["white"]
        - background2 = colors["off_white"]
        - text1 = colors["dark_gray"]
        - text2 = colors["bright_green"]
        - accent1 = colors["forest_green"]
        - accent2 = colors["jade_green"]
        - accent3 = colors["yellow"]
        - accent4 = colors["mint_green"]
        - accent5 = colors["medium_gray"]
        - accent6 = colors["true_blue"]

        Returns:
            theme_colors: the aforementioned manager
        """
        return self._theme_colors

    @property
    @functools.lru_cache()
    def custom_colors(self) -> CustomColors:
        """
        A color manager holding other "custom" theme colors.

        Returns:
            theme_colors: the aforementioned manager
        """
        return self._custom_colors

    @property
    @functools.lru_cache()
    def common_colors(self) -> CommonColors:
        """
        A color manager holding the colors that are common to all themes.

        Returns:
            common_colors: the aforementioned manager
        """
        return CommonColors()

    @property
    @functools.lru_cache()
    def discrete_cmaps(self) -> Dict[str, ListedColormap]:
        """
        A list of discrete color maps. These maps can be applied to any kind of plot, with any kind of dimensions to
        represent: if you have n dimensions to plot, matplotlib will sample n colors from the discrete map. If n is
        larger than the number of colors in the map, colors will be repeated.

        Returns:
            discrete_cmaps: a dictionary of {name: cmap}. Note that to encode the cmap, we use matplotlib
                            ListedColormap object.

        Notes:
            By convention, discrete cmaps names follow this pattern `<theme_name>:d_<map_name>`. In this context,
            "d" stands for "discrete".
        """
        colors_default = ListedColormap(
            [norm_rgb(c.rgb) for c in self.theme_colors.get(["text", "accent"])],
            name=f"{self.name}:d_default",
        )
        colors_highlight = ListedColormap(
            [norm_rgb(c.rgb) for c in (self.default_green, self.default_yellow, self.default_red)],
            name=f"{self.name}:d_highlight",
        )
        return {
            **{
                f"{self.name}:d_default": colors_default,
                f"{self.name}:d_highlight": colors_highlight,
                f"{self.name}:d_gray": self._create_discrete_cmap(
                    name=f"{self.name}:d_gray", rgb=self.theme_colors.text1.rgb
                ),
                f"{self.name}:d_green": self._create_discrete_cmap(
                    name=f"{self.name}:d_green", rgb=self.theme_colors.text2.rgb
                ),
            },
            **{
                f"{self.name}:d_{c.name}": self._create_discrete_cmap(name=f"{self.name}:d_{c.name}", rgb=c.rgb)
                for c in self.theme_colors.get(types=["accent"])
            },
        }

    @property
    @functools.lru_cache()
    def continuous_cmaps(self) -> Dict[str, LinearSegmentedColormap]:
        """
        A list of "continuous" colormaps. These maps can be applied to any kind of plot, with any kind of dimensions to
        represent: if you have n dimensions to plot, matplotlib will sample n colors from the continuum for you.

        Returns:
            continuous_cmaps: a dictionary of {name: cmap}. Note that to encode the cmap, we use matplotlib
                              LinearSegmentedColormap object.

        Notes:
            By convention, continuous cmaps names follow this pattern `<theme_name>:c_<map_name>`. In this context,
            "c" stands for "continuous".
        """
        light_gray = Color("light_gray", *self.discrete_cmaps[f"{self.name}:d_gray"].colors[0])
        return {
            cmap.name: cmap
            for cmap in (
                self._create_linear_cmap(
                    f"{self.name}:c_default",
                    [
                        norm_rgb(self.default_green.rgb),
                        light_gray.rgb,
                        norm_rgb(self.default_yellow.rgb),
                    ],
                    [0, 0.5, 1],
                ),
                self._create_linear_cmap(
                    f"{self.name}:c_gray",
                    [norm_rgb(self.theme_colors.text1.rgb), light_gray.rgb],
                    [0.0, 1.0],
                ),
                self._create_linear_cmap(
                    f"{self.name}:c_highlight",
                    self.discrete_cmaps[f"{self.name}:d_highlight"].colors,
                    [0.0, 0.5, 1.0],
                ),
                self._create_linear_cmap(
                    f"{self.name}:c_red_yellow",
                    [
                        norm_rgb(self.default_red.rgb),
                        light_gray.rgb,
                        norm_rgb(self.default_yellow.rgb),
                    ],
                    [0, 0.5, 1],
                ),
                self._create_linear_cmap(
                    f"{self.name}:c_red_blue",
                    [
                        norm_rgb(self.default_red.rgb),
                        light_gray.rgb,
                        norm_rgb(self.default_blue.rgb),
                    ],
                    [0, 0.5, 1],
                ),
                self._create_linear_cmap(
                    f"{self.name}:c_green_yellow",
                    [
                        norm_rgb(self.default_green.rgb),
                        light_gray.rgb,
                        norm_rgb(self.default_yellow.rgb),
                    ],
                    [0, 0.5, 1],
                ),
                self._create_linear_cmap(
                    f"{self.name}:c_green_red",
                    [
                        norm_rgb(self.default_green.rgb),
                        light_gray.rgb,
                        norm_rgb(self.default_red.rgb),
                    ],
                    [0, 0.5, 1],
                ),
                self._create_linear_cmap(
                    f"{self.name}:c_green_blue",
                    [
                        norm_rgb(self.default_green.rgb),
                        light_gray.rgb,
                        norm_rgb(self.default_blue.rgb),
                    ],
                    [0, 0.5, 1],
                ),
                self._create_linear_cmap(
                    f"{self.name}:c_blue_yellow",
                    [
                        norm_rgb(self.default_blue.rgb),
                        light_gray.rgb,
                        norm_rgb(self.default_yellow.rgb),
                    ],
                    [0, 0.5, 1],
                ),
            )
        }

    @property
    @functools.lru_cache()
    def continuous_cmaps_reversed(self) -> Dict[str, LinearSegmentedColormap]:
        """
        Same as continuous but the order of colors is reversed.
        """
        return {f"{name}_r": reverse_colormap(cmap, f"{name}_r") for name, cmap in self.continuous_cmaps.items()}

    @property
    @functools.lru_cache()
    def rc(self) -> Dict:
        """
        A Matplotlib "RC" dictionary containing default values for all matplotlib objects

        Returns:
            rc: the dictionary of all defaults
        """
        return {
            # FONT ------------------
            "font.size": 12,
            "font.family": self.font,
            "font.sans-serif": self.font,
            # LEGEND ------------------
            "legend.fontsize": 12,
            # LINES ------------------
            "lines.color": norm_rgb(self.theme_colors.text2.rgba),
            "lines.linewidth": 1.4,
            "lines.markerfacecolor": norm_rgb(self.theme_colors.text2.rgba),
            "lines.markeredgewidth": 0.0,
            "lines.markersize": 5.6,
            "lines.solid_capstyle": "round",
            "patch.linewidth": 0.75,
            # TICKS ------------------
            "xtick.labelsize": 10.0,
            "xtick.major.pad": 5.6,
            "xtick.major.width": 0.75,
            "xtick.minor.width": 0.75,
            "ytick.labelsize": 10.0,
            "ytick.major.pad": 5.6,
            "ytick.major.width": 0.75,
            "ytick.minor.width": 0.75,
            # AXES ------------------
            "axes.labelsize": 16,
            "axes.titlesize": 16,
            "axes.axisbelow": True,
            "axes.edgecolor": norm_rgb(self.theme_colors.text1.rgba),
            "axes.labelcolor": norm_rgb(self.theme_colors.text1.rgba),
            "axes.facecolor": "white",
            "axes.grid": True,
            "axes.grid.axis": "both",
            "axes.grid.which": "both",
            "axes.linewidth": 0.0,
            # FIGURE ------------------
            "figure.facecolor": "white",
            "figure.figsize": SIZES["large"],
            "figure.dpi": 100,
            "figure.autolayout": False,
            # SAVE ------------------
            "savefig.dpi": 100,
            "savefig.format": "png",
            "savefig.bbox": "standard",
            "savefig.transparent": True,
            # IMAGE ------------------
            "image.cmap": f"{self.name}:d_default",
            # LEGEND ------------------
            "legend.numpoints": 1,
            "legend.scatterpoints": 1,
            "legend.fancybox": False,
            "legend.loc": "best",
            "legend.frameon": True,
            "legend.framealpha": 0.7,
            "legend.facecolor": norm_rgb(self.theme_colors.background1.rgba),
            "legend.edgecolor": "none",
            # TEXT ------------------
            "text.color": norm_rgb(self.theme_colors.text1.rgba),
            # TICKS ------------------
            "xtick.color": norm_rgb(self.theme_colors.text1.rgba),
            "xtick.direction": "out",
            "xtick.major.size": 1,
            "xtick.minor.size": 0.5,
            "ytick.color": norm_rgb(self.theme_colors.text1.rgba),
            "ytick.direction": "out",
            "ytick.major.size": 0.0,
            "ytick.minor.size": 0.0,
        }

    @staticmethod
    def _create_discrete_cmap(
        name: str, rgb: Tuple[int, int, int], cuts: List[float] = None, n: int = None
    ) -> ListedColormap:
        """
        Methodology to generate discrete camp, powerpoint style (i.e. by applying increases or decreases to the
        luminance of RGB colors).

        Args:
            name: the name for the map
            rgb: color to use as a reference point
            cuts: the different brightness corrections to be applied

        Returns:
            cmap: the generated cmap
        """
        if cuts is None:
            if n is None:
                # use default PowerPoint cuts (cf color panel)
                cuts = [
                    0.8,
                    0.6,
                    0.4,
                    -0.25,
                    -0.5,
                ]
            else:
                # we generate n evenly spaced cuts between the max PowerPoint cuts (included)
                cuts = list(reversed(list(np.round(np.linspace(-50, 80, n) / 100, 2))))

        return ListedColormap(
            colors=[norm_rgb(lighten_color(rgb, scale)) for scale in [c for c in cuts if c >= 0]]
            + [norm_rgb(darken_color(rgb, scale)) for scale in [-c for c in cuts if c < 0]],
            name=name,
        )

    @staticmethod
    def _create_linear_cmap(
        name: str,
        color_list: List[Union[Tuple[int, int, int], Tuple[int, int, int, float]]],
        stops,
    ) -> LinearSegmentedColormap:
        """
        Method to generate a matplotlib continuous colormap from a list of colors.

        Args:
            name: the name for the map
            color_list: the list of rgb colors
            stops: the list of stops (between 0 and 1) to position the colors on the map

        Returns:
            cmap: the generated cmap
        """
        red, green, blue = [], [], []
        for s, c in zip(stops, color_list):
            red.append((s, c[0], c[0]))
            green.append((s, c[1], c[1]))
            blue.append((s, c[2], c[2]))

        return LinearSegmentedColormap(name, {"red": red, "green": green, "blue": blue})

    def _register_cmaps(self):
        """Registers created cmap into matplotlib environment, making them accessible for plotting"""
        log.debug(f"Registering cmaps...")
        all_cmaps_dict = {
            **self.discrete_cmaps,
            **self.continuous_cmaps,
            **self.continuous_cmaps_reversed,
        }
        for cmap_name, cmap in all_cmaps_dict.items():
            if cmap_name in mpl.colormaps:
                continue
            else:
                mpl.colormaps.register(cmap, name=cmap_name)

    def _register_font(self):
        """Rgisters the font in seaborn"""
        log.debug(f"Registering font {self.font}...")
        manager = FontManager()
        available_fonts_names = [v.name for v in manager.ttflist]
        if self.font in available_fonts_names:
            sns.set(font=self.font, font_scale=1)
        else:
            log.warning(
                f'could find font "{self.font}". Using default. Available fonts names are : '
                f'{", ".join(sorted(available_fonts_names))}'
            )
            sns.set(font_scale=1)

    def _register_rc_theme(self):
        """Registers the matplotlib RcParams"""
        log.debug(f"Registering RC params...")
        # reset the RC
        mpl.rcParams.update(mpl.rcParamsDefault)

        # Set it
        sns.set(
            context="paper",
            style="whitegrid",
            palette=tuple(tuple(c) for c in self.discrete_cmaps[f"{self.name}:d_default"].colors),
            rc=self.rc,
        )

        # Register it as an available style
        plt.style.library[self.name] = self.rc
        plt.style.available[:] = sorted(plt.style.library.keys())

    def _register_colors(self):
        """Registers the colors into matplotlib environment"""
        log.debug(f"Registering colors...")
        for c in self.theme_colors:
            mcolors._colors_full_map[c.name] = norm_rgb(c.rgb)
        for c in self.custom_colors:
            mcolors._colors_full_map[c.name] = norm_rgb(c.rgb)
        for c in self.common_colors:
            mcolors._colors_full_map[c.name] = norm_rgb(c.rgb)

    def show(self):
        """Prints a detailed visual summary of the theme for inspection"""
        largest = max([cmap.N for cmap in self.discrete_cmaps.values()])

        # Colors
        f1, ax = plt.subplots(figsize=(largest, 2))
        f1.suptitle("Theme Colors")
        self.theme_colors.show(fig=f1, ax=ax)
        f2, ax = plt.subplots(figsize=(largest, 1))
        f2.suptitle("Custom Colors")
        self.custom_colors.show(fig=f2, ax=ax)
        f3, ax = plt.subplots(figsize=(largest, 1))
        f3.suptitle("Common Colors", size=16)
        self.common_colors.show(fig=f3, ax=ax)

        # discrete CMAPS
        n_rows = len(self.discrete_cmaps)
        f4, axs = plt.subplots(nrows=n_rows, figsize=(largest, n_rows))
        f4.suptitle("Discrete Color Maps", size=16)
        f4.tight_layout(pad=1.0)
        for i, (name, cmap) in enumerate(self.discrete_cmaps.items()):
            palplot_discrete(cmap=cmap, title=name, ax=axs[i])

        # continuous CMAPS
        n_rows = len(self.continuous_cmaps)
        f5, axs = plt.subplots(nrows=n_rows, figsize=(largest, n_rows))
        f5.suptitle("Continuous Color Maps", size=16)
        f5.tight_layout(pad=1.0)
        for i, (name, cmap) in enumerate(self.continuous_cmaps.items()):
            palplot_continuous(cmap, title=name, ax=axs[i])

        plt.show()

        return [f1, f2, f3, f4, f5]

    def set(self):
        """Sets all the components of the theme (font, colors, cmaps, rc_params) in matplotlib environment"""
        self._register_font()
        self._register_colors()
        self._register_cmaps()
        self._register_rc_theme()

    def register(self):
        """Register the theme within matplotlib's library of available themes"""
        plt.style.library[self.name] = self.rc
        plt.style.available[:] = sorted(plt.style.library.keys())
