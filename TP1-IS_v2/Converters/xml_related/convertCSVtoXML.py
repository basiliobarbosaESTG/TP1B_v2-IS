from Converters.Classes.athelet import athletes
from Converters.Classes.hosts import hosts
from Converters.Classes.country import Country
from Converters.Classes.olympic_results import olympic_results
import csv

class convertCSVtoXML:
    def __init__(self, file1, file2, file3, file4):
        self.host_file =file1
        self.medals_file=file2
        self.atleta_file = file3
        self.name_file = file4
        self.array_pais = []
        self.array_atletas = []
        self.array_hosts = []
        self.pais =  {}
        self.data = []
        self.ateletas = []

    #Files
    def convert(self):
        try:
            def saveCSV(data):
                info = []
                for row in data:
                    info.append(row)
                return info
#ABERTURA DOS FICHEIROS
            with open(self.atleta_file, 'r', encoding="UTF8") as file:
                reader = csv.reader(file, delimiter=";")
                next(reader)
                ateletas = saveCSV(reader)
                
            with open(self.host_file, 'r', encoding="UTF8")as file:
                reader = csv.reader(file, delimiter=";")
                next(reader)
                game_hosts = saveCSV(reader)

            with open(self.medals_file, 'r', encoding="UTF8")as file:
                reader = csv.reader(file, delimiter=";")
                next(reader)
                data = saveCSV(reader)

#RETORNA DAODS SEM REPETIÇOES
            def export_single_data(data, pos):
                info = []
                for d in data:
                    if d[pos] not in info:
                        info.append(d[pos])
                return info

            #Countries
            cod_pais = export_single_data(data, 11)
            for d in data:
                for p in cod_pais:
                    if d[11] == p:
                        dados = [d[9],d[10]]
                        self.pais.update({p: dados })

            # #Exrever os iniciais
            # #Guarsar em dicionario o Host e as diciplçinas
            dis = {}
            for h in game_hosts: #Para os hosts
                help = []
                for d in data: #para a informação
                    if h[0] == d[1]: #se o host for igual ao host da informação
                        if d[0] not in help:
                            help.append(d[0])             
                dis.update({h[0]: help})


            #Escrever ficheiro xml
            with open("Output\\"+self.name_file+".xml", "w", encoding="UTF8") as file:
                file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                file.write("<olympics>\n")
                file.write("\t<olympic_results>\n")
                for h in dis:
                    file.write("\t\t<local_event id=\""+h+"\">\n")
                    for disc in dis.get(h):
                        file.write("\t\t\t<discipline id=\""+disc+"\">")
                        for line in data:
                            if line[0] == disc and line[1] == h:
                                local = olympic_results(line)
                                file.write(local.toXML())
                        file.write("\n\t\t\t</discipline>\n")
                    file.write("\t\t</local_event>\n")
                file.write("\t</olympic_results>\n")
                file.write("\t<athletes>\n")
                for a in ateletas:
                    ateleta =  athletes(a)
                    file.write(ateleta.toXML())
                file.write("\n\t</athletes>\n")
                file.write("\t<countries>\n")
                for p in self.pais:
                    ct = Country(p, self.pais.get(p))
                    file.write(ct.toXML())
                file.write("\n\t</countries>\n")
                file.write("\t<hosts>\n")
                for h in game_hosts:
                    host =  hosts(h)
                    file.write(host.toXML())
                file.write("\n\t</hosts>\n")
                file.write("</olympics>\n")
        except(Exception) as error:
            print("Error: ", error)
        
