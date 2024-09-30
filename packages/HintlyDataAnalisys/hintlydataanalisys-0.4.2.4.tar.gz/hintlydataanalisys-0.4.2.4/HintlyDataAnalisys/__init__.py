# your_library/__init__.py

from .DataAnalisys import Math, Text, MatchMaker, FilterType, NormalizeType
from .plugins import timeLib

__all__ = ['Math', 'Text', 'MatchMaker', 'FilterType', 'NormalizeType', 'timeLib']

__version__ = '0.4.2.4'
__author__ = 'Franciszek Chmielewski'
__email__ = 'ferko2610@gmail.com'
