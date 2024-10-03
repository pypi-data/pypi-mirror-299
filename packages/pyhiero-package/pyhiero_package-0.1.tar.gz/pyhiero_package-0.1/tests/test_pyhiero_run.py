import pytest
import pandas as pd
import datatest as dt
from io import StringIO

import glyphs_list_loops as pl
import glyphs_csv as pc

import pyhiero_run as pr

""" def test_pyhiero_input(monkeypatch) :
  monkeypatch.setattr('sys.stdin', StringIO("1"))
  expected = "foo"
  actual = pr.pyhiero_input()
  message = "expected: {0} actual: {1}".format(expected, actual)
  assert actual == expected, message """