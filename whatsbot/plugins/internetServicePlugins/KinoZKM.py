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

import re
import requests
from bs4 import BeautifulSoup
from plugins.GenericPlugin import GenericPlugin
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class KinoZKM(GenericPlugin):
    """
    The KinoZKM Class
    """

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        Defines parameters for the plugin.
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)
        self.mode = ""

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        if re.search(r"^/kinozkm summaries$", self.message):
            return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        if self.message == "/kinozkm summaries":
            self.mode = "summary"

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a WrappedTextMessageProtocolEntity
        """
        if self.mode == "summary":
            return WrappedTextMessageProtocolEntity(self.__get_all_summaries__(), to=self.sender)
        raise NotImplementedError()

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return the description as string
        """
        if language == "en":
            return "/kinozkm\tFetches current information regarding the cinema at the ZKM in Karlsruhe\n" \
                   "syntax: /kinozkm [summaries]"
        elif language == "de":
            return "/kinozkm\tZeigt Aktuelle Kinoinformationen für das Kino am ZKM in Karlsruhe an\n" \
                   "syntax: /kinozkm [summaries]"
        else:
            return "Help not available in this language"

    # Local Methods
    @staticmethod
    def __get_all_summaries__():
        """
        Returns all currently running movies and movie descriptions.
        :return: the movie titles and descriptions as formatted string.
        """

        html = requests.get("http://www.filmpalast.net/programm.html").text
        soup = BeautifulSoup(html, "html.parser")
        all_movie_descriptions = soup.select('.gwfilmdb-film-description')
        all_movie_titles = soup.select('.gwfilmdb-film-title')

        movie_titles = []

        skip = False
        for title in all_movie_titles:
            if not skip:
                movie_titles.append(title)
                skip = True
            else:
                skip = False

        all_descriptions = "Zusammenfassungen Aktuelle Filme:\n\n"

        i = 0
        while i < len(movie_titles):
            all_descriptions += movie_titles[i].text + "\n"
            all_descriptions += all_movie_descriptions[i].text + "\n\n"
            i += 1

        return all_descriptions