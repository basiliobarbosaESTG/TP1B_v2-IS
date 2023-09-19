from xmlrpc.server import SimpleXMLRPCServer
from psycopg2 import Error
import datetime,json,psycopg2
from Database import querys
from Converters.xml_related.converterXML import converterXML
from Converters.xml_related.validatorXML import validateXML

f = open('config.json')
data = json.load(f).get('dbconfig')
connection = psycopg2.connect(
    host=data.get('host'),
    port=data.get('port'), 
    user=data.get('user'),
    password=data.get('password'),  
    database=data.get('database')) #Conecção a base de dados

cursor = connection.cursor()

# print("PostgreSQL server information")
# print(connection.get_dsn_parameters(), "\n")

cursor.execute("SELECT version();") #Verifcar coneção
record = cursor.fetchone()
print("You are connected to - ", record, "\n")

def convert(athlete_events_file,name_file): #Chama a classe que faz a conversao do ficheiro de CSV para XML
    c = converterXML(athlete_events_file,name_file)
    result = c.convert()
    print(result)

def validate(xml, xsd): #Chama a classe que faz a validação do XML com o XSD
    return validateXML(xml, xsd)

def get_date(): #Retorna a data atual
    return datetime.datetime.now()

def insert_file(name, file): #INSERIR FICHEIRO NA BD
    insert_data = (name, file, get_date())
    try:
        cursor.execute(querys.insert_sp, insert_data)
        connection.commit()
        cursor.execute(querys.get_last)
        result = cursor.fetchall()
        print("File saved\n")
        return str(result)
    except (Exception, Error) as error:
        connection.rollback()
        print("Error inserting new file", error)
        return(str(error))
        

#CONSULTAS
#PEDIDO A BD PARA EXECUTAR O SEGUINT XPATH/XQUERY QUE OBTEM OS DADOS DE UM ATLETA A PARTIR DO SEU NOME
def getAthleteByName(name, id): #, id
    try:
        cursor.execute("SELECT unnest(XPATH('/athletes/atlethe[@name[contains(text(),\""+name+"\")]]/*/text()', xml)) FROM xmldata where id="+id)
        #SELECT unnest(XPATH('/olympics/athletes/athlete[./athlete_full_name[contains(text(),\""+name+"\")]]/*/text()', xml)) FROM xmldata where id="+id)
        connection.commit()
        result = cursor.fetchall()
        return result     
    except (Exception, Error) as error:
        connection.rollback()
        print("Error executing: ", error)
        return(str(error))

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
print("Listening on port 8000...")

#REGISTO DAS FUNÇOES
server.register_function(convert, "convert")
server.register_function(validate, "validate")
server.register_function(insert_file, "insert_file")
server.register_function(getAthleteByName, "getAthleteByName")


server.serve_forever()
