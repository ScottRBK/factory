"""Locate the role resources bundled inside the package."""
from pathlib import Path


def resource_root() -> Path:
    return Path(__file__).resolve().parents[1] / 'resources'
