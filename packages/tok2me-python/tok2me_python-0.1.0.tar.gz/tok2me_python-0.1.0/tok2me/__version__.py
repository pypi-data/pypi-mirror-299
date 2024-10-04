import importlib.metadata

try:
    __version__ = importlib.metadata.version("tok2me-pythom")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0 (unknown)"
