import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath('../..'))

project = 'Demand Forecast '
copyright = '2024, Eduard Poliakov'
author = 'Eduard Poliakov'
release = 'v1.0.5'

# Add Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",  # Adding viewcode extension to include [source]
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# For LaTeX output
latex_engine = 'pdflatex'
latex_documents = [
    ('index', 'demand_forecast.tex', 'Demand Forecast', 'Eduard Poliakov', 'manual'),
]

# Add mocks for problematic modules
class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

# Define specific mocks to include __all__
class AddFeaturesMock(Mock):
    __all__ = []

class AddTargetsMock(Mock):
    __all__ = []

MOCK_MODULES = {
    'src_demand_forecast.entities.train_pipeline_params': Mock(),
    'src_demand_forecast.features.AddFeatures': AddFeaturesMock(),
    'src_demand_forecast.features.AddTargets': AddTargetsMock()
}

sys.modules.update(MOCK_MODULES)

