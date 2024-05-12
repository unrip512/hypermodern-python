"""Sphinx configuration."""
project = "hypermodern-python"
author = "Groza Nadezhda"
copyright = f"2024, {author}"
extensions=[
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "sphinx_autodoc_typehints",
        "sphinx_rtd_theme",
]

html_theme = "sphinx_rtd_theme"

