"""
    you may find all the unit tests here
"""
import os

import pytest
from flask_nsfw import NSFW

import tests.data.samples as samples



def test_base64_data_with_nudity():
    """
        Trys to send base64 data with nudity
    """
    assert not NSFW.test_base64_data([samples.NSFW_IMAGE_BASE64])

def test_base64_data_without_nudity():
    """
        Trys to send base64 data without nudity
    """
    assert NSFW.test_base64_data([samples.SFW_IMAGE_BASE64])

def test_file_data_with_nudity():
    """
        Trys to send file objects with nudity
    """
    assert not NSFW.test_files_against_api([samples.NSFW_IMAGE])

def test_file_data_without_nudity():
    """
        Trys to file objects without nudity
    """
    assert NSFW.test_files_against_api([samples.SFW_IMAGE])

def test_urls_with_nudity():
    """
        Trys to file objects with nudity
    """
    assert not NSFW.test_urls_against_api([samples.NSFW_IMAGE_URL])

def test_urls_without_nudity():
    """
        Trys to file objects without nudity
    """
    assert  NSFW.test_urls_against_api([samples.SFW_IMAGE_URL])
