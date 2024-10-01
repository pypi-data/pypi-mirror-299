import pytest

from bantam.http import WebApplication


def test_preprocess_module_errors():
    with pytest.raises(ValueError):
        WebApplication.preprocess_module('class_rest_errors')
