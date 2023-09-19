class Country:
    #country_name, country_code, country_3_letter_code   (country_name,country_code,country_3_letter_code)
    def __init__(self,id,line_cvs):
        self.id_unico= id
        self.country_name= line_cvs[0]
        self.country_2_letter_code= line_cvs[1]
#ESCRVE OS DAODS DE UM PAIS
    def toXML(self):
        return """
        <country country_id="%s">
            <country_name>%s</country_name>
            <country_2_letter_code>%s</country_2_letter_code>
        </country>"""%(self.id_unico, self.country_name, self.country_2_letter_code)

