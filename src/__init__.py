import logging

# General information about the project.
from pathlib import Path

__project__ = "mpl_themes_utils"
__name__ = "mpl_themes_utils"
__description__ = "A library containing visualization utilities, to make styling your matplotlib plots easier."
__copyright__ = None
__author__ = "Vallet Hugo"
__author_email__ = None
__version__ = "0.0.1"
__release__ = __version__
__repo__ = None

log = logging.getLogger(name=__project__)

SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent
