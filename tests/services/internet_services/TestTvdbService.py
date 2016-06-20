# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

from nose.tools import with_setup
from nose.tools import assert_false
from nose.tools import assert_true

from messengerbot.connection.generic.Message import Message
from messengerbot.services.internet_services.TvdbService import TvdbService


# noinspection PyMethodMayBeStatic
class TestTvdbService(object):
    """
    A Unit Test Class for a Service class
    """

    correct_messages = []
    incorrect_messages = []
    service = TvdbService

    @classmethod
    def setup_class(cls):
        """
        Sets up the test class
        """
        pass

    @classmethod
    def teardown_class(cls):
        """
        Tears down the test class
        """
        pass

    def setup(self):
        """
        Sets up a test
        """
        pass

    def teardown(self):
        """
        Tears down a test
        """
        pass

    @with_setup(setup, teardown)
    def test_regex(self):
        """
        Tests the service's regex check
        """
        for message in self.correct_messages:
            message_object = Message(message_body=message, address="")
            print("Testing correct Regex for: " + message)
            assert_true(self.service.regex_check(message_object))
        for message in self.incorrect_messages:
            message_object = Message(message_body=message, address="")
            assert_false(self.service.regex_check(message_object))
            print("Testing incorrect Regex for: " + message)