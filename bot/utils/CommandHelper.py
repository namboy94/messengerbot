class CommandHelper(object):

    def __init__(self, userInput):
        self.language = "en"
        if userInput == "hilfe": self.language = "de"

    def generateHelp(self):

        if self.language == "en":
            return "Commands:\n\n\n" \
                   "/help\tSends this help message\n\n" \
                   "/(wetter|weather)\tSends weather information\n" \
                   "syntax:\t/<wetter|weather>[options;] cityname, [region,] [country]\n" \
                   "options: text,verbose\n\n" \
                   "/mensa\tSends Mensa Information\n" \
                   "syntax: /mensa [linie] [morgen]\n\n" \
                   "/tvdb\tSends episode name of an episode from TVDB\n" \
                   "syntax: /tvdb <show> s<season> e<episode>\n\n" \
                   "/(table|tabelle)\tSends football table information\n" \
                   "syntax: /<table/tabeller> [country], [league]\n\n" \
                   "/(matchday|spieltag)\tSends football matchday information\n" \
                   "syntax: /<matchday|spieltag> [country], [league]"

        elif self.language == "de":
            return "Befehle:\n\n\n" \
                   "/help\tSchickt diese Hilfsnachricht\n\n" \
                   "/(wetter|weather)\tSchickt Wetterinformationen\n" \
                   "syntax:\t/<wetter|weather>[options;] cityname, [region,] [country]\n" \
                   "options: text,verbose\n\n" \
                   "/mensa\tSchickt den Mensa Plan\n" \
                   "syntax: /mensa [linie] [morgen]\n\n" \
                   "/tvdb\tSchickt den Episodennamen einer Episode auf TVDB\n" \
                   "syntax: /tvdb <show> s<season> e<episode>\n\n" \
                   "/(table|tabelle)\tSchcikt Fußball Tabelleninformationen\n" \
                   "syntax: /<table/tabeller> [country], [league]\n\n" \
                   "/(matchday|spieltag)\tSchickt Fußball Spieltaginformationen\n" \
                   "syntax: /<matchday|spieltag> [country], [league]"