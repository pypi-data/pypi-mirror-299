#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Full license can be found in License.md
# Full author list can be found in .zenodo.json file
# DOI:10.5281/zenodo.3986131
#
# DISTRIBUTION STATEMENT A: Approved for public release. Distribution is
# unlimited.
# ----------------------------------------------------------------------------
"""Collection of instruments for the pysatNASA library.

Each instrument is contained within a subpackage of this set.

"""
from pysatNASA.instruments import methods  # noqa F401

__all__ = ['ace_epam_l2', 'ace_mag_l2', 'ace_sis_l2', 'ace_swepam_l2',
           'cnofs_ivm', 'cnofs_plp', 'cnofs_vefi', 'de2_fpi', 'de2_lang',
           'de2_nacs', 'de2_rpa', 'de2_vefi', 'de2_vefimagb', 'de2_wats',
           'dmsp_ssusi', 'formosat1_ivm',
           'icon_euv', 'icon_fuv', 'icon_ivm', 'icon_mighti',
           'igs_gps', 'iss_fpmu', 'jpl_gps', 'maven_insitu_kp',
           'maven_mag', 'maven_sep', 'omni_hro', 'reach_dosimeter',
           'ses14_gold', 'timed_guvi', 'timed_saber', 'timed_see']

for inst in __all__:
    exec("from pysatNASA.instruments import {x}".format(x=inst))

# Remove dummy variable
del inst
