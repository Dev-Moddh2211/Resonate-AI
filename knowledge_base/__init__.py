"""Local, traceable Category 2 knowledge-base pipeline."""

from .pipeline import build_index
from .retrieval import Retriever

__all__ = ["build_index", "Retriever"]
