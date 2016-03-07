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


class Unicoder(object):
    """
    The Unicoder class
    """

    @staticmethod
    def fix_incoming_unicode(broken_emoji):
        """
        Fixes a broken incoming Unicode string
        :param broken_emoji: The broken unicode string
        :return: the fixed string
        """

        byte_emoji = bytes(broken_emoji, 'utf-8')
        good_byte_emoji = []
        i = 0

        while i < len(byte_emoji):
            if not byte_emoji[i] == 194:
                if byte_emoji[i] == 195:
                    i += 1
                    good_byte_emoji.append(byte_emoji[i] + 64)
                else:
                    good_byte_emoji.append(byte_emoji[i])
            i += 1

        good_byte_emoji = bytes(good_byte_emoji)
        return good_byte_emoji.decode()

    @staticmethod
    def fix_outgoing_unicode(good_unicode):
        """
        Fixes a broken outgoing Unicode string
        :param good_unicode: the outgoing unicode string
        :return: the fixed string
        """

        new_word = ""

        for char in good_unicode:

            byte_unicode = list(bytes(char, 'utf-8'))
            if len(byte_unicode) == 1:
                new_word += char
                continue

            broken_byte_unicode = []
            i = 0
            has195 = False
            last_is_194 = False
            last_is_195 = False

            while i < len(byte_unicode):

                if not has195:
                    broken_byte_unicode.append(195)
                    has195 = True
                    last_is_195 = True

                else:
                    if last_is_195:
                        broken_byte_unicode.append(byte_unicode[i] - 64)
                        last_is_195 = False
                        i += 1
                    elif last_is_194:
                        broken_byte_unicode.append(byte_unicode[i])
                        last_is_194 = False
                        i += 1
                    else:
                        broken_byte_unicode.append(194)
                        last_is_194 = True

            new_word += bytes(broken_byte_unicode).decode()

        return new_word