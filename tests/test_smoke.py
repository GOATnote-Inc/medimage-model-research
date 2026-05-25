"""Hermetic smoke tests."""

from __future__ import annotations

import medimage_model_research


def test_version_string():
    assert isinstance(medimage_model_research.__version__, str)
    assert medimage_model_research.__version__.count(".") >= 2


def test_subpackages_importable():
    from medimage_model_research import data, eval, models, receipts, training

    for mod in (data, eval, models, receipts, training):
        assert mod is not None
