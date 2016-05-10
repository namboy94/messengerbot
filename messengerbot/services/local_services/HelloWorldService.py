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

# imports
import re

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message


class HelloWorldService(Service):
    """
    The HelloWorldService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = "hello_world"
    """
    The identifier for this service
    """

    help_description = {"en": "/helloworld\tSends a message containing how to write a 'Hello World'"
                              "Program in a specific language\n"
                              "syntax:\n"
                              "/helloworld <language|list>",
                        "de": "/helloworld\tSchickt eine Nachricht mit einem 'Hello World' Codeschnipsel für eine"
                              "spezifische Programmiersprache\n"
                              "synatx:\n"
                              "/helloworld <sprache|liste>"}
    """
    Help description for this service.
    """

    implementations = {"python": "print(\"Hello World!\")",
                       "python2": "print \"Hello World!\"",
                       "python3": "print(\"Hello World!\")",
                       "java": "pubic class Main {\n"
                               "    public static void main(String[] args) {\n"
                               "        System.out.println(\"Hello World!\");\n"
                               "    }\n"
                               "}",
                       "c": "#include <stdio.h>\n\n"
                            "int main() {\n"
                            "    printf(\"Hello World!\\n\");\n"
                            "    return 0;\n"
                            "}",
                       "c++": "#include <iostream>\n\n"
                              "int main() {\n"
                              "    std::cout << \"Hello World!\";\n"
                              "    return 0;\n"
                              "}",
                       "bash": "echo \"Hello World\"",
                       "rust": "fn main() {\n"
                               "    println!(\"Hello World!\");\n"
                               "}",
                       "ruby": "puts 'Hello, world!'",
                       "perl": "print \"Hello World!\\n\";",
                       "c#": "using System;\n"
                             "namespace HelloWorldApplication{\n"
                             "    class HelloWorld {\n"
                             "        Console.WriteLine(\"Hello World!\");\n"
                             "        Console.ReadKey();\n"
                             "    }\n"
                             "}",
                       "basic": "10 PRINT \"Hello World!\"",
                       "visual basic": "Module HelloWorld\n"
                                       "    Sub Main()\n"
                                       "        System.Console.WriteLine(\"Hello World!\")\n"
                                       "        System.Console.ReadLine()\n"
                                       "        End\n"
                                       "    End Sub\n"
                                       "End Module\n",
                       "brainfuck": "++++++++++\n"
                                    "[\n"
                                    " >+++++++>++++++++++>+++>+<<<<-\n"
                                    "]\n"
                                    ">++.\n"
                                    ">+.\n"
                                    "+++++++.\n"
                                    ".\n"
                                    "+++.\n"
                                    ">++.\n"
                                    "<<+++++++++++++++.\n"
                                    ">.\n"
                                    "+++.\n"
                                    "------.\n"
                                    "--------.\n"
                                    ">+.\n"
                                    ">.\n"
                                    "+++.",
                       "haskell": "main = putStrLn \"Hello World!\"",
                       "erlang": "-module(hello).\n"
                                 "-export([hello_world/0]).\n\n"
                                 "hello_world() -> io:fwrite(\"Hello World!\n\").",
                       "x86 assembly": "section .data\n"
                                       "str:     db 'Hello World!', 0Ah\n"
                                       "str_len: equ $ - str\n\n\n"
                                       "section .text\n"
                                       "global _start\n\n"
                                       "_start:\n"
                                       "	mov	eax, 4\n"
                                       "	mov	ebx, 1\n\n"
                                       "    mov	ecx, str\n"
                                       "    mov	edx, str_len\n"
                                       "    int	80h\n\n"
                                       "    mov	eax, 1\n"
                                       "    mov	ebx, 0\n"
                                       "    int	80h"}
    """
    The actual implementations of hello world in the different languages
    """

    language_not_found_error = {"en": "Programming Language not found",
                                "de": "Programmiersprache nicht gefunden"}
    """
    Error message sent when the programming language could not be found.
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        prog_language = message.message_body.lower().split(" ", 1)[1]
        if prog_language.startswith("list"):
            reply = self.list_languages()
        else:
            reply = self.implementations[prog_language]

        reply_message = self.generate_reply_message(message, "Hello World", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/helloworld (list(e)?|" \
                + Service.regex_string_from_dictionary_keys([HelloWorldService.implementations]) + ")$"
        regex = regex.replace("+", "\+")
        return re.search(re.compile(regex), message.message_body.lower())

    def list_languages(self) -> str:
        """
        Creates a list of implemented languages

        :return: the list of implemented languages
        """
        list_string = ""
        for language in self.implementations:
            list_string += language + "\n"
        return list_string.rstrip("\n")
