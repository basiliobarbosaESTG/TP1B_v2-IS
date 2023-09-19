from xmlrpc.server import SimpleXMLRPCServer
from psycopg2 import Error
import datetime,json,psycopg2
from Database import querys
from Converters.xml_related.convertCSVtoXML import convertCSVtoXML
from Converters.xml_related.validatorXML import validateXML

f = open('config.json')
data = json.load(f).get('dbconfig')
connection = psycopg2.connect(user=data.get('user'),password=data.get('password'), host=data.get('host'), port=data.get('port'), database=data.get('database')) #Conecção a base de dados

cursor = connection.cursor()

# print("PostgreSQL server information")
# print(connection.get_dsn_parameters(), "\n")

cursor.execute("SELECT version();") #Verifcar coneção
record = cursor.fetchone()
print("You are connected to - ", record, "\n")

def convert(host_file,medals_file,atleta_file,name_file): #Chama a classe que faz a conversao do ficheiro de CSV para XML
    c = convertCSVtoXML(host_file,medals_file,atleta_file,name_file)
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

# def update_file(id, new_name, new_file): #Update FICHEIRO
#     ficheiro = open(new_file).read()  
#     updated_data = (id,new_name, ficheiro, get_date())
#     try:
#         cursor.execute(querys.update_sp, updated_data)
#         connection.commit()
#         cursor.execute(querys.get_row, [id])
#         # result = cursor.fetchall()
#         # print(result)
#         print("File Updated")
#         return "File saved\n"
#     except (Exception, Error) as error:
#         connection.rollback()
#         print("Error updating file", error)
#         return(str(error))


def delete_file(id): #Delete FICHEIRO
    try:
        cursor.execute(querys.delete_sp, [id])
        connection.commit()
        cursor.execute(querys.get_row, [id])
        result = cursor.fetchall()
        print(result)
        print("File deleted\n Outout: " + str(result))
        return str(result)
    except (Exception, Error) as error:
        connection.rollback()
        print("Error deleting file", error)
        return(str(error))

def get_athlete_data(loca, dis, env, gender, medal, id): #PEDIDO A BD PARA EXECUTAR O SEGUINT XPATH/XQUERY QUE OBTEM OS DADOS DE UM ATLETA A PARTIR DA SUA POSIÇÃO NUM DADO EVENTO
    try:
        cursor.execute("SELECT unnest(XPATH('/olympics/athletes/athlete[@ref=/olympics/olympic_results/local_event[@id=\""+loca+"\"]/discipline[@id=\""
                        +dis+"\"]/event_title[@id=\""+env+"\"]/event_gender[@id=\""+gender+"\"]/medal_type[@id=\""
                        +medal+"\"]/athlete/@ref]/*/text()', xml))from xmldata where id ="+id)
        connection.commit()
        result = cursor.fetchall()
        return result     
    except (Exception, Error) as error:
        connection.rollback()
        print("Error executing: ", error)
        return(str(error))

def order_games(order, id):#PEDIDO A BD PARA EXECUTAR O SEGUINT XPATH/XQUERY QUE OBTEM OS HOSTS ORDENADOS POR ORDEM ALFABEITCA ASC OU DESC
    #hosts por ordem alfabetica
    try:
        cursor.execute("SELECT unnest(CAST(xpath('olympics/hosts/host/game_name/text()',xml) AS text)::text[]) AS hosts FROM xmldata where id ="+id+" Order by hosts "+order)
        connection.commit()
        result = cursor.fetchall()
        return result     
    except (Exception, Error) as error:
        connection.rollback()
        print("Error executing: ", error)
        return(str(error))

def count_medals_country_game(local, medal, pais, id):#PEDIDO A BD PARA EXECUTAR O SEGUINT XPATH/XQUERY QUE OBTEM OS O NUMERO DE MEDALHAS POR PAIS NUM DADO JOGO ATRAVESZ DO 3LETTER CODE
     #Contar medalhas por pais
    try:
        cursor.execute("SELECT unnest(CAST(xpath('olympics/olympic_results/local_event[@id=\""
        +local+"\"]/discipline/event_title/event_gender/medal_type[@id=\""
        +medal+"\"]/athlete[@country_id=\""
        +pais+"\"]/@country_id', xml)as TEXT)::text[]) as pais, count(*)  FROM xmldata where id="+id+"Group by pais")
        connection.commit()
        result = cursor.fetchall()
        return result     
    except (Exception, Error) as error:
        connection.rollback()
        print("Error executing: ", error)
        return(str(error))

def country_gold_medals(local, id): #PEDIDO A BD PARA EXECUTAR O SEGUINT XPATH/XQUERY QUE OBTEM TODAS AS MEDALHAS DE OURO DE UM PAIS ORDENADOS DO MAIOR PARA O MENOR NUM DETERMIDADO JOGO
    try:
        cursor.execute("SELECT unnest(CAST(xpath('olympics/olympic_results/local_event[@id=\""
        +local+"\"]/discipline/event_title/event_gender/medal_type[@id=\"GOLD\"]/athlete/@country_id', xml)as TEXT)::text[]) as pais, count(*) as num FROM xmldata where id="+id+"Group by pais order by num DESC")
        connection.commit()
        result = cursor.fetchall()
        return result     
    except (Exception, Error) as error:
        connection.rollback()
        print("Error executing: ", error)
        return(str(error))


def athlelet_info(name, id):#PEDIDO A BD PARA EXECUTAR O SEGUINT XPATH/XQUERY QUE OBTEM OS DADOS DE UM ATLETA A PARTIR DO SEU NOME
    try:
        cursor.execute("SELECT unnest(XPATH('/olympics/athletes/athlete[./athlete_full_name[contains(text(),\""+name+"\")]]/*/text()', xml)) FROM xmldata where id="+id)
        connection.commit()
        result = cursor.fetchall()
        return result     
    except (Exception, Error) as error:
        connection.rollback()
        print("Error executing: ", error)
        return(str(error))

def country_for_game(id): #PEDIDO A BD PARA EXECUTAR O SEGUINT XPATH/XQUERY QUE OBTEM O NUMERO DEJOGOS REALZIADOS NUM DADO PAIS
    try:
        cursor.execute("SELECT unnest(CAST(xpath('olympics/hosts/host/game_location/text()',xml) AS text)::text[]) as pais, count(*) FROM xmldata where id ="+id+" group by pais")
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
server.register_function(insert_file, "insert_file")
# server.register_function(update_file, "update_file")
server.register_function(delete_file, "delete_file")
server.register_function(convert, "convert")
server.register_function(validate, "validate")
server.register_function(country_for_game, "country_for_game")
server.register_function(athlelet_info, "athlelet_info")
server.register_function(country_gold_medals, "country_gold_medals")
server.register_function(count_medals_country_game, "count_medals_country_game")
server.register_function(order_games, "order_games")
server.register_function(get_athlete_data, "get_athlete_data")

server.serve_forever()

