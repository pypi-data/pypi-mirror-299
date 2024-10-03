"""Tests for `hatch_external_dependencies` package."""

import unittest


class TestHook(unittest.TestCase):
    """Tests for `external_dependencies_py` package."""

    def test_import(self):
        import hatch_external_dependencies.hooks

        self.assertIsNotNone(hatch_external_dependencies.hooks.ExternalDependenciesBuilder)
        self.assertIsNotNone(hatch_external_dependencies.hooks.hatch_register_build_hook)
