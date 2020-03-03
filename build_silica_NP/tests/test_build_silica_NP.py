"""
Unit and regression test for the build_silica_NP package.
"""

# Import package, test suite, and other packages as needed
import build_silica_NP
import pytest
import sys
import mbuild as mb

def test_build_silica_NP_imported():
    """ Sample test, will always pass so long as import statement worked """
    assert "build_silica_NP" in sys.modules

def test_import():
    """ Test that mBuild recipe import works """
    assert "build_silica_NP" in vars(mb.recipes).keys()
