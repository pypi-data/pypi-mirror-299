#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring

import importlib_metadata

from .base import INJECTION_POINTS

from .base import Glitch
from .math import FunctionGlitch
from .math import StepGlitch
from .math import RectangleGlitch
from .read import TimeSeriesGlitch
from .read import HDF5Glitch
from .lpf import OneSidedDoubleExpGlitch
from .lpf import IntegratedOneSidedDoubleExpGlitch
from .lpf import TwoSidedDoubleExpGlitch
from .lpf import IntegratedTwoSidedDoubleExpGlitch
from .lpf import ShapeletGlitch
from .lpf import IntegratedShapeletGlitch
from .lpf import LPFLibraryGlitch
from .lpf import LPFLibraryModelGlitch

try:
    metadata = importlib_metadata.metadata('lisaglitch').json
    __version__ = importlib_metadata.version('lisaglitch')
    __author__ = metadata['author']
    __email__ = metadata['author_email']
except importlib_metadata.PackageNotFoundError:
    pass
