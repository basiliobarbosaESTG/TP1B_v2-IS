class olympic_results(object):
    # default constructor
    def __init__(self, line):
        self.eventos = line[2]
        self.genero = line[3]
        self.medal = line[4]
        unico = line[7].split("/")
        self.atleta = unico[len(unico)-1]
        self.pais = line[11]
#ESCREVE OS DADAOS DOS RESULTADOS OLYMPICOS A PARTIR DO EVENTO
    def toXML(self):
        return """
                <event_title id="%s">
                    <event_gender id="%s">
                        <medal_type id="%s">
                            <athlete ref="%s" country_id="%s"></athlete>
                        </medal_type>
                    </event_gender>
                </event_title>"""%(self.eventos, self.genero,self.medal,self.atleta,self.pais)

        
