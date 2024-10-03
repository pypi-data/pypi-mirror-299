import pytest
import numpy as np

import mock_dataframe_strings as mds
import list_processors as lp

@pytest.fixture
def gsl_lists() :
   return [[["A001"], ["A002", "A003"]], [["B001", "B003"], ["B004"]]]

def test_merge_inner_arrays(gsl_lists) :
  expected = [["A001"], ["A002", "A003"], ["B001", "B003"], ["B004"]]
  actual = lp.merge_inner_arrays(gsl_lists)
  message = "The string:\n {0}\n was actually returned, but\n {1}\n was expected".format(actual, expected)
  # note the .all() syntax required for array comparison, see Obsidian pytest docs for details
  assert actual == expected, message

@pytest.fixture
def entry_strings_list() :
   return ["A001-A002-A003", "B001-B003-B004"]

def test_concat_gsl_entry_strings(entry_strings_list) :
  expected = "A001-A002-A003-B001-B003-B004"
  actual = lp.concat_gsl_entry_strings(entry_strings_list)
  message = "The string:\n {0}\n was actually returned, but\n {1}\n was expected".format(actual, expected)
  # note the .all() syntax required for array comparison, see Obsidian pytest docs for details
  assert actual == expected, message

@pytest.fixture
def unicode_strings_list() :
   return [["\U000131CD", "\U00013216", "\U00013191"], ["\U000133CE"]]

def test_concat_unicode_strings(unicode_strings_list) :
  expected = "\U000131CD\U00013216\U00013191\U000133CE"
  actual = lp.concat_unicode_strings(unicode_strings_list)
  message = "The string:\n {0}\n was actually returned, but\n {1}\n was expected".format(actual, expected)
  assert actual == expected, message