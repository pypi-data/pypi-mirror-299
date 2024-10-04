#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Full license can be found in License.md
# Full author list can be found in .zenodo.json file
# DOI:10.5281/zenodo.3986131
#
# DISTRIBUTION STATEMENT A: Approved for public release. Distribution is
# unlimited.
# ----------------------------------------------------------------------------
"""Core library for pysatNASA.

This is a library of `pysat` instrument modules and methods designed to support
NASA instruments and missions archived at the Community Data Analysis Web
portal.

"""

try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

import os

from pysatNASA import constellations  # noqa F401
from pysatNASA import instruments  # noqa F401

__version__ = metadata.version('pysatNASA')

# Set directory for test data
here = os.path.abspath(os.path.dirname(__file__))
test_data_path = os.path.join(here, 'tests', 'test_data')
