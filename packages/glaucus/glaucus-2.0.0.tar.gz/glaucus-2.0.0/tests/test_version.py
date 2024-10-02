# Copyright 2023 The Aerospace Corporation
# This file is a part of Glaucus
# SPDX-License-Identifier: LGPL-3.0-or-later

"""version should be parsable"""

import unittest

from glaucus import __version__


class TestVersion(unittest.TestCase):
    def test_version(self):
        """
        Ensure the version string is valid.
        """
        major, minor, micro = tuple(int(x) for x in __version__.split("."))
        print(f"glaucus v{major}.{minor}.{micro}")
