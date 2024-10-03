import pytest
import pandas as pd

import mock_dataframe_strings as mds
import list_processors as lp
import glyphs_list_loops as gll

# ================= GSL List Fixtures

# --- Mock Dataframe:
# Ex: {"GSL": "AA011", "Glyph": "𓐙", "Unicode": "13419"},
# Used for conversion by test_long_gsl_to_unicode
@pytest.fixture
def gsl_hiero_dict():
  df_data = mds.gsl_dataframe_dict
  dataframe =  pd.DataFrame(data=df_data)
  return dataframe

# --- Short GSL Code Lists:
# Ex: "M18-N35:I9-.-W25"
# Input to test_short_gsl_to_long
@pytest.fixture
def short_gsl_list():
  merged_lists = [
    mds.short_gsl_A_list, 
    mds.short_gsl_B_list,
    mds.short_gsl_D_list,
    mds.short_gsl_E_list,
    mds.short_gsl_F_list,
    mds.short_gsl_G_list,
    mds.short_gsl_H_list,
    mds.short_gsl_I_list,
    mds.short_gsl_K_list,
    mds.short_gsl_L_list,
    mds.short_gsl_M_list,
    mds.short_gsl_N_list,
    mds.short_gsl_O_list,
    mds.short_gsl_P_list,
    mds.short_gsl_Q_list,
    mds.short_gsl_R_list,
    mds.short_gsl_S_list,
    mds.short_gsl_T_list,
    mds.short_gsl_U_list,
    mds.short_gsl_V_list,
    mds.short_gsl_W_list,
    mds.short_gsl_X_list,
    mds.short_gsl_Y_list,
    mds.short_gsl_list,
    # new strings can be added here
  ]
  return lp.merge_inner_arrays(merged_lists)

# --- Long GSL Code Lists:
# Ex: [["M018", "N035", "I009"], ["W025"]]
# Input to test_long_gsl_to_unicode
# Expected output from test_short_gsl_to_long
@pytest.fixture
def long_gsl_list():
  merged_lists = [
    mds.long_gsl_A_list,
    mds.long_gsl_B_list,
    mds.long_gsl_D_list,
    mds.long_gsl_E_list,
    mds.long_gsl_F_list,
    mds.long_gsl_G_list,
    mds.long_gsl_H_list,
    mds.long_gsl_I_list,
    mds.long_gsl_K_list,
    mds.long_gsl_L_list,
    mds.long_gsl_M_list,
    mds.long_gsl_N_list,
    mds.long_gsl_O_list,
    mds.long_gsl_P_list,
    mds.long_gsl_Q_list,
    mds.long_gsl_R_list,
    mds.long_gsl_S_list,
    mds.long_gsl_T_list,
    mds.long_gsl_U_list,
    mds.long_gsl_V_list,
    mds.long_gsl_W_list,
    mds.long_gsl_X_list,
    mds.long_gsl_Y_list,
    mds.long_gsl_list,
    # new 2D lists can be added here
  ]
  return lp.merge_inner_arrays(merged_lists)

# --- Unicode Array Lists:
# Ex: [["\U00013000", "\U00013001", "\U00013009", "\U0001300B"]]
# Input to test_unicode_array_to_string
# Expected output from short_gsl_to_long
@pytest.fixture
def uni_list():
  merged_lists = [
    mds.uni_array_gsl_A_list,
    mds.uni_array_gsl_B_list,
    mds.uni_array_gsl_D_list,
    mds.uni_array_gsl_E_list,
    mds.uni_array_gsl_F_list,
    mds.uni_array_gsl_G_list,
    mds.uni_array_gsl_H_list,
    mds.uni_array_gsl_I_list,
    mds.uni_array_gsl_K_list,
    mds.uni_array_gsl_L_list,
    mds.uni_array_gsl_M_list,
    mds.uni_array_gsl_N_list,
    mds.uni_array_gsl_O_list,
    mds.uni_array_gsl_P_list,
    mds.uni_array_gsl_Q_list,
    mds.uni_array_gsl_R_list,
    mds.uni_array_gsl_S_list,
    mds.uni_array_gsl_T_list,
    mds.uni_array_gsl_U_list,
    mds.uni_array_gsl_V_list,
    mds.uni_array_gsl_W_list,
    mds.uni_array_gsl_X_list,
    mds.uni_array_gsl_Y_list,
    mds.uni_array_gsl_list,
    # new 2D lists can be added here
  ]
  return lp.merge_inner_arrays(merged_lists)

# --- Unicode Strings:
# Ex: "\U00013000\U00013001\U00013009\U0001300B"
# Expected output from to test_unicode_array_to_string
@pytest.fixture
def uni_strings():
  merged_lists = [
    mds.uni_out_gsl_A_list,
    mds.uni_out_gsl_B_list,
    mds.uni_out_gsl_D_list,
    mds.uni_out_gsl_E_list,
    mds.uni_out_gsl_F_list,
    mds.uni_out_gsl_G_list,
    mds.uni_out_gsl_H_list,
    mds.uni_out_gsl_I_list,
    mds.uni_out_gsl_K_list,
    mds.uni_out_gsl_L_list,
    mds.uni_out_gsl_M_list,
    mds.uni_out_gsl_N_list,
    mds.uni_out_gsl_O_list,
    mds.uni_out_gsl_P_list,
    mds.uni_out_gsl_Q_list,
    mds.uni_out_gsl_R_list,
    mds.uni_out_gsl_S_list,
    mds.uni_out_gsl_T_list,
    mds.uni_out_gsl_U_list,
    mds.uni_out_gsl_V_list,
    mds.uni_out_gsl_W_list,
    mds.uni_out_gsl_X_list,
    mds.uni_out_gsl_Y_list,
    mds.uni_out_gsl_list,
    # new strings can be added here
  ]
  return lp.concat_unicode_strings(merged_lists)

# ============ Converter Function Tests

def test_short_gsl_to_long(short_gsl_list, long_gsl_list):
  expected = long_gsl_list
  actual = gll.short_gsl_to_long(short_gsl_list)
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

def test_long_gsl_to_unicode(gsl_hiero_dict, long_gsl_list, uni_list):
  expected = uni_list
  actual = gll.long_gsl_to_unicode(gsl_hiero_dict, long_gsl_list)
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

def test_unicode_array_to_string(uni_list, uni_strings):
  expected = uni_strings
  actual = gll.unicode_array_to_string(uni_list)
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

# --- Other Tests

@pytest.fixture
def gsl_hiero_df(gsl_hiero_dict):
  return gll.list_glyph_gsl_info(gsl_hiero_dict)

def test_list_glyph_gsl_info_first(gsl_hiero_df):
  assert gsl_hiero_df[0] == "The GSL for the sign 𓀀 is A001" 

def test_list_glyph_gsl_info_last(gsl_hiero_df):
  assert gsl_hiero_df[-1] == "The GSL for the sign 𓐙 is AA011"