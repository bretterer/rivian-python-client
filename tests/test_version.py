"""Test the module version."""

from rivian.__version__ import VERSION


def test_version() -> None:
    """Test version."""
    assert VERSION != "0.0.0"
