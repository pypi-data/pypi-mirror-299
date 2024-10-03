"""Tests for `external_dependencies` package."""

import unittest


class Testexternaldependenciespy(unittest.TestCase):
    """Tests for `external_dependencies_py` package."""

    def test_empty(self):
        import external_dependencies.cli

        self.assertIsNotNone(external_dependencies.cli.app)
