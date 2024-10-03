import pytest

import mock_dataframe_strings as mds
import inscrip_splitters as ip

@pytest.fixture
def entry_gsl_A_list() :
   return mds.entry_gsl_list

def test_split_gsl_string(entry_gsl_A_list) :
  expected = mds.short_gsl_list
  actual = ip.split_gsl_string(entry_gsl_A_list)
  message = "The 2D array:\n {0}\n was actually returned, but\n {1}\n was expected".format(actual, expected)
  assert actual == expected, message