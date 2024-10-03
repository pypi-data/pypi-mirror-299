# # -*- coding: utf_8 -*-
import pytest
import datatest as dt
# import pandas as pd

import glyphs_csv as pc

@pytest.fixture
@dt.working_directory(__file__)
def csv_file() :
  ccv_df = pc.hiero_dataframe_from_csv('../hiero_v9.csv')
  return ccv_df

def test_validate_csv_columns(csv_file) :
  dt.validate(
    csv_file.columns, {"Unicode", "GSL", "Transliteration", "Glyph", "Definitions", "Determines", "References", "Tags"},
  )

def test_validate_csv_unicode(csv_file) :
  # unicode code points are 5-character alphanumerics
  dt.validate.regex(csv_file["Unicode"], r"[A-F0-9]{5}")
  
def test_validate_csv_gsl(csv_file) :
  # valid GSL codes have 1-2 letters in the range A-Z
  # or AA, followed by 3 digits
  dt.validate.regex(csv_file["GSL"], r"^[A-Z]{1}\d{3}|AA\d{3}")

def test_validate_csv_transliteration(csv_file) :
  # valid transliterations can be blank ("-") or alphanumerics
  dt.validate.regex(csv_file["Transliteration"], r"\w+|-")

def test_validate_unicode_glyph_range(csv_file) :
  # valid hiero glyphs are in the range from 𓀀 (A001) to 𓐫 (AA029)
  dt.validate.regex(csv_file["Glyph"], r"[\U00013000-\U000AA029]")

def test_validate_definitions(csv_file) :
  # valid definitions are of chars in the range a-z or A-Z, or blank ("-")
  dt.validate.regex(csv_file["Definitions"], r"[a-zA-Z,]|-")

def test_validate_determines(csv_file) :
  # valid definitions are of chars in the range a-z or A-Z, or blank ("-")
  dt.validate.regex(csv_file["Determines"], r"[a-zA-Z,]|-")

def test_validate_csv_references(csv_file) :
  # valid references including a citation of "Gardiner, Grammar, p. " 
  # followed by a 2-3 digit number, or blank ("-")
  dt.validate.regex(csv_file["References"], r"Gardiner, Grammar, p.\s\d{2,3}|-")