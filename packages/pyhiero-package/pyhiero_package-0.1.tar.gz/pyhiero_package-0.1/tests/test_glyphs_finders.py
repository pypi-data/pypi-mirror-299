import pytest
import pandas as pd
# import pandas.util.testing as pdt

import glyphs_finders as pgf

@pytest.fixture
def pd_dataframe():
  # The codepoint \U00013000 corresponds to the glyph 𓐙
  return pd.DataFrame(data={
    "GSL": ["AA011", "S034", "X008"], 
    "Glyph": ["\U00013419", "\U000132F9", "\U000133D9"],
    "Unicode": ["13419", "132F9", "133D9"],
  })

# todo - add messages
@pytest.fixture
def gsl_from_dataframe(pd_dataframe) :
  return pgf.get_gsl_from_hiero(pd_dataframe, "\U00013419")

def test_get_gsl_from_hiero(gsl_from_dataframe) :
  assert gsl_from_dataframe == "AA011"

@pytest.fixture
def hiero_from_dataframe(pd_dataframe) :
  return pgf.get_hiero_from_gsl(pd_dataframe, "AA011")

def test_get_hiero_from_gsl(hiero_from_dataframe) :
  # tests for the glyph 𓐙 which has the codepoint \U00013000
  assert hiero_from_dataframe == "\U00013419"

@pytest.fixture
def unicode_from_gsl(pd_dataframe) :
  return pgf.get_unicode_from_gsl(pd_dataframe, "AA011")

def test_get_unicode_from_gsl(unicode_from_gsl) :
  actual = unicode_from_gsl
  expected = "13419"
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected)
  assert actual == expected, message

def test_get_unicode_from_gsl(unicode_from_gsl) :
  actual = unicode_from_gsl
  expected = "13419"
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected)
  assert actual == expected, message

# todo - test coverage for is_hiero_present method

@pytest.fixture
def parsed_unicode(pd_dataframe) :
  return pgf.parse_unicode(pd_dataframe, "S034")

def test_parse_unicode(pd_dataframe, parsed_unicode) :
  actual = parsed_unicode
  expected = "\U000132F9"
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected)
  assert actual == expected, message

@pytest.fixture
def gsl_array():
  return ['S034', ':', 'X008']

def test_run_gsl_to_unicode_loop(pd_dataframe, gsl_array) :
  expected = "\U000132F9\U000133D9"
  actual = pgf.run_gsl_to_unicode_loop(pd_dataframe, gsl_array)
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected)
  assert actual == expected, message

# ================= convert_long_gsl_to_short tests =================

def test_convert_long_gsl_to_short_F23() :
  expected = "F23"
  actual = pgf.convert_long_gsl_to_short("F023")
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

def test_convert_long_gsl_to_short_G100_v2() :
  expected = "G100"
  actual = pgf.convert_long_gsl_to_short("G100")
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

def test_convert_long_gsl_to_short_Aa11() :
  expected = "Aa11"
  actual = pgf.convert_long_gsl_to_short("AA011")
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

# ================= convert_short_gsl_to_long tests =================

def test_convert_short_gsl_to_long_G4() :
  expected = "G004"
  actual = pgf.convert_short_gsl_to_long("G4")
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

def test_convert_short_gsl_to_long_F23() :
  expected = "F023"
  actual = pgf.convert_short_gsl_to_long("F23")
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

def test_convert_short_gsl_to_long_A100() :
  expected = "A100"
  actual = pgf.convert_short_gsl_to_long("A100")
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

def test_convert_short_gsl_to_long_Aa1() :
  expected = "AA001"
  actual = pgf.convert_short_gsl_to_long("Aa1")
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message