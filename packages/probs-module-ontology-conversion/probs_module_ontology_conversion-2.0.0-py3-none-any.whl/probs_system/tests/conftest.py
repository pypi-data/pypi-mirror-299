"""Common configuration shared by all tests in this directory."""

import re
from contextlib import contextmanager
import pytest
from pathlib import Path


def pytest_addoption(parser):
   parser.addoption(
       "--working-dir", action="store", help="path to working directory, default temporary"
   )


@pytest.fixture(scope="function")
def working_dir(request, tmp_path):
    """Set working directory if specified or use tmp_path"""
    working_dir = request.config.getoption("--working-dir") or tmp_path
    if working_dir:
        working_dir = Path(working_dir)
    return working_dir

