# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

from nose.tools import with_setup
from nose.tools import assert_equal
from plugins.internetServicePlugins.Weather import Weather
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class TestWeather(object):
    """
    Unit Test Class that tests the Weather Plugin
    """

    def __init__(self):
        """
        Constructor
        """
        self.message = None
        self.layer = None

    @classmethod
    def setup_class(cls):
        """
        Sets up the test class
        """
        print()

    @classmethod
    def teardown_class(cls):
        """
        Tears down the test class
        """
        print()

    def setup(self):
        """
        Sets up a test
        """
        self.message = None

    def teardown(self):
        """
        Tears down a test
        """
        self.message = None

    @with_setup(setup, teardown)
    def test(self):
        """
        basic test
        """
        self.message = WrappedTextMessageProtocolEntity(_from="23323232@2121212.com", body="/wetter karlsruhe")
        plugin = Weather(self.layer, self.message)
        assert_equal(plugin.regex_check(), True)