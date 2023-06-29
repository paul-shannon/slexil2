import os
import sys
# Add the directory of this package to the path, so that
# imports can find other modules in site-packages/<package>.
sys.path.append(os.path.dirname(__file__))
from .version import __version__
