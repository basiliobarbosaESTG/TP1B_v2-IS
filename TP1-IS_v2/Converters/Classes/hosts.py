class hosts:
    # default constructor
    def __init__(self, line_csv):
        self.id_unico = line_csv[0]
        self.name = line_csv[4]
        self.location = line_csv[3]
        self.season = line_csv[0]
        self.year = line_csv[2]
#ESCRVEE ODS DADOS DOS HOST DOS JOGOS
    def toXML(self):
        return """
        <host id="%s">
            <game_name>%s</game_name>
            <game_location>%s</game_location>
            <game_season>%s</game_season>
            <game_year>%s</game_year>
        </host>"""%(self.id_unico,self.name,self.location, self.season, self.year)