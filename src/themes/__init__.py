from typing import Union

from src import log
from src.themes.green_generic import green_generic_theme
from src.themes.blue_generic import blue_generic_theme
from src.themes.common.template import Theme
from src.themes.common.colors import (
    Color,
    ColorManager,
    ThemeColors,
    CommonColors,
    CustomColors,
)


NAMES_TO_THEMES = {"mpl-themes-green": green_generic_theme, "mpl-themes-blue": blue_generic_theme}


def register_theme(theme: Union[str, Theme] = "mpl-themes-green"):
    """
    Method to register a theme within matplotlib's theme namespace.

    Args:
        theme: theme name or Theme object
    """
    log.info(f"Registering '{theme}' in matplotlib themes library")
    if isinstance(theme, str):
        try:
            theme = NAMES_TO_THEMES[theme]
        except KeyError:
            raise NotImplementedError(
                f"Could not find custom theme '{theme}'. Available themes are {NAMES_TO_THEMES.keys()}"
            )
        except Exception as e:
            raise Exception(e)
    theme.register()


def set_theme(theme: Union[str, Theme] = "mpl-themes-green"):
    """
    Main entry-point for setting a theme using visual utils.

    Args:
        theme: theme name or Theme object
    """
    log.info(f"Setting '{theme}' as the default matplotlib theme")
    if isinstance(theme, str):
        try:
            theme = NAMES_TO_THEMES[theme]
        except KeyError:
            raise NotImplementedError(
                f"Could not find custom theme '{theme}'. Available themes are {NAMES_TO_THEMES.keys()}"
            )
        except Exception as e:
            raise Exception(e)

    theme.set()
