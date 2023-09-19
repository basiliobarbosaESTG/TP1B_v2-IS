class athletes(object):
    # default constructor
    def __init__(self,line_csv):
        unico = line_csv[0].split("/")
        self.id_unico = unico[len(unico)-1]
        self.full_name = line_csv[1]
        self.year_birth = line_csv[3]
        self.url = line_csv[0]
        self.first_game = line_csv[2]
        self.medals = line_csv[4]
        self.n_participations = line_csv[5]
#EXREVE OS DADOS DE UM ATLETA
    def toXML(self):
        return """
        <athlete ref="%s">
            <athlete_full_name>%s</athlete_full_name>
            <athlete_year_birth>%s</athlete_year_birth>
            <athlete_url>%s</athlete_url>
            <first_game>%s</first_game>
            <medals>%s</medals>
            <n_participations>%s</n_participations>
        </athlete>"""%(self.id_unico,self.full_name,self.year_birth,self.url,self.first_game,self.medals,self.n_participations)
