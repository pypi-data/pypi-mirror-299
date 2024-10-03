import pandas as pd

import glyphs_xml as gx

def test_output_xml() :
  expected = "gsl_signs"
  actual = gx.output_xml()
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message

#todo - this isn't working, need to read XML's better
def test_get_determines() :
  expected = "borked"
  actual = gx.get_determines()
  message = "\nActual: {0}\nExpected: {1}\n".format(actual, expected) 
  assert actual == expected, message