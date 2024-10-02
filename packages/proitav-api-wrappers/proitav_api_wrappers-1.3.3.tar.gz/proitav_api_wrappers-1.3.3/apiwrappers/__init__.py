try:
    from ._version import version as __version__
except ImportError:
    import warnings

    warnings.warn(
        "Version information not found. This package is likely not installed correctly."
    )
    __version__ = "unknown"
