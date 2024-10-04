from colorsys import rgb_to_hls, hls_to_rgb
from io import BytesIO
from typing import Dict, Tuple, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap, ListedColormap


def palplot_continuous(cmap: LinearSegmentedColormap, title: str = None, ax: plt.Axes = None):
    """Plot the values in a color palette as a horizontal continuum.

    Args:
        cmap: sequence of matplotlib colors
        title: name for the graph
        ax: an axis object to attach the plot to
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 1))
    if title is None:
        title = cmap.name

    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    ax.imshow(gradient, interpolation="nearest", aspect="auto", cmap=cmap)
    ax.set_title(title, loc="left")
    ax.set_axis_off()

    return ax


def palplot_discrete(cmap: ListedColormap, title: str = None, size=1, ax: plt.Axes = None):
    """Plot the values in a color palette as a horizontal array.

    Args:
        cmap: sequence of matplotlib colors
        title: name for the graph
        size: scaling factor for size of plot
        ax: an axis object to attach the plot to
    """
    n = cmap.N
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(n * size, size))
    if title is None:
        title = cmap.name

    ax.imshow(
        np.arange(n).reshape(1, n),
        cmap=cmap,
        interpolation="nearest",
        aspect="auto",
    )
    ax.set_xticks(np.arange(n) - 0.5)
    ax.set_yticks([-0.5, 0.5])
    # Ensure nice border between colors
    ax.set_xticklabels(["" for _ in range(n)])
    # The proper way to set no ticks
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.set_title(title, loc="left")

    return ax


def norm_rgb(rgb: Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
    """Normalize RGB values"""
    return tuple(rgb[chan] / 255.0 for chan in range(3)) + ((rgb[3],) if len(rgb) == 4 else tuple())


def inv_norm_rgb(rgb: Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
    """Invert normalize RGB values"""
    return tuple(rgb[chan] * 255.0 for chan in range(3)) + ((rgb[3],) if len(rgb) == 4 else tuple())


def lighten_color(rgb: Tuple[int, int, int], factor: float = 0.1):
    """
    Increase the lightness of an rgb color similarly to what Powerpoint does (converting to HSL, then adjusting L).

    Args:
        rgb: the rgb (0-255 values) to be corrected
        factor:correction factor

    Returns:
        new_rgb: corrected color
    """
    r, g, b = rgb
    h, luminance, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    luminance = max(min(luminance + (1 - luminance) * factor, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, luminance, s)
    return int(r * 255), int(g * 255), int(b * 255)


def darken_color(rgb: Tuple[int, int, int], factor: float = 0.1):
    """
    Decrease the lightness of an rgb color similarly to what Powerpoint does (converting to HSL, then adjusting L).

    Args:
        rgb: the rgb (0-255 values) to be corrected
        factor:correction factor

    Returns:
        new_rgb: corrected color
    """
    r, g, b = rgb
    h, luminance, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    luminance = max(min(luminance - luminance * factor, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, luminance, s)
    return int(r * 255), int(g * 255), int(b * 255)


def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i / inch for i in tupl[0])
    else:
        return tuple(i / inch for i in tupl)


def to_clip(fig=None, dpi=92, tight_layout_kwargs: Dict = None, **savefigkwargs):
    """
    Copy current figure or fig to clipboard as png.
    Additional key word arguments can be passed to matplotlib's savefig function

    Args:
        fig (matplotlib figure): pass figure or get current via gcf()
        tight_layout_kwargs (Dict): kwargs for tight_layout()
        dpi (int): integer of dpi

    Warnings:

        This works on Windows only
    """
    import win32clipboard

    if fig is None:
        fig = plt.gcf()

    with BytesIO() as img_buffer:
        with BytesIO() as output:
            if tight_layout_kwargs is not None:
                fig.tight_layout(**tight_layout_kwargs)
            fig.savefig(img_buffer, format="png", dpi=dpi, transparent=True, **savefigkwargs)
            img_buffer.seek(0)
            im = Image.open(img_buffer)
            im.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)  # DIB = device independent bitmap
            win32clipboard.CloseClipboard()


def reverse_colormap(cmap: LinearSegmentedColormap, name=None) -> LinearSegmentedColormap:
    """
    Reverses the colormap cmap.

    Args:
        cmap: the colormap to reverse
        name: a name for the resulting map

    Returns:
        new_cmap: the cmap inverted

    Notes:
        Explanation::

            t[0] goes from 0 to 1

            row i:   x  y0  y1 -> t[0] t[1] t[2]
                           /
                          /
            row i+1: x  y0  y1 -> t[n] t[1] t[2]

            so the inverse should do the same:

            row i+1: x  y1  y0 -> 1-t[0] t[2] t[1]
                           /
                          /
            row i:   x  y1  y0 -> 1-t[n] t[2] t[1]
    """
    reverse = []
    k = []

    if name is None:
        name = cmap.name + "_r"

    for key in cmap._segmentdata:
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []
        for t in channel:
            data.append((1 - t[0], t[2], t[1]))
        reverse.append(sorted(data))

    return LinearSegmentedColormap(name, dict(zip(k, reverse)))


def get_n_colors(cmap: Union[str, LinearSegmentedColormap, ListedColormap], n: int):
    """
    Samples n colors from the matplotlib cmap. Particularly convenient when you need to do a plot with multiple
    series, each with one color, using a "for loop" and you want to use custom cmaps.
    """
    if isinstance(cmap, str):
        cmap = mpl.cm.get_cmap(cmap)

    return cmap.resampled(n)
