# hatch-external-dependencies

The package is a hatch plugin.

When building with hatchling this plugin will look in the project toml configuration for an external section and adds dependencies in the built package's metadata as a Requires-External entry.


# Usage

To use the plugin add `hatch-external-dependencies` as a build-system requirement in your pyproject.toml

    [build-system]
    requires = ["hatchling", "hatch-external-dependencies"]
    build-backend = "hatchling.build"

In order to activate the plugin you also need to declare the hook:
    
    [tool.hatch.build.hooks.external-dependencies]

In order to define external dependencies there are two supported syntax:

    [project]
    external-dependencies = ["pkg:generic/libsomething", ...]

or (based on https://peps.python.org/pep-0725/):

    [external]
    dependencies = ["pkg:generic/libsomething", ...]

