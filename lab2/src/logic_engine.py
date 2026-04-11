from __future__ import annotations

from .analysis import AnalysisMixin
from .core import CoreEngine
from .minimization import MinimizationMixin


class LogicEngine(CoreEngine, AnalysisMixin, MinimizationMixin):
    pass
