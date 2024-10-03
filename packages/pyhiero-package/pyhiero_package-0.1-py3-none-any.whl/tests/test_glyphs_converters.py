import pytest
import pandas as pd
import datatest as dt

import glyphs_converters as gco
import mock_dataframe_strings as mds

@pytest.fixture
def pd_dataframe():
  return pd.DataFrame(data=mds.gsl_dataframe_dict)

@pytest.fixture
def short_gsl_string() :
   return mds.entry_gsl_A_list

def test_convert_short_gsl_to_hiero(pd_dataframe, short_gsl_string) :
    expected = mds.uni_out_gsl_A_list
    actual = gco.convert_short_gsl_to_hiero(pd_dataframe, short_gsl_string)
    message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected)
    assert actual == expected, message