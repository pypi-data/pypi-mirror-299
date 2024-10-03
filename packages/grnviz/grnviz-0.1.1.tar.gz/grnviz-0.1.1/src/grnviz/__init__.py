"""
GRNviz
======

Visualization of gene co-expression and regulatory networks
"""
from importlib.metadata import version as _version

try:
    __version__ = _version('grnviz')
except Exception:
    __version__ = 'unknown version'
