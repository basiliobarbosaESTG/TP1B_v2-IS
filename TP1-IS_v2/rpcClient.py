import xmlrpc.client

def conect_rpc():
    conn = xmlrpc.client.ServerProxy("http://localhost:8000/")
    return conn

def convert_():
    athlete_events_file = input("Insert athlete_events_file: ")
    name_file = input("Insert name: ")
    try:
        conn = conect_rpc()
        conn.convert(athlete_events_file, name_file)
        return name_file + ".xml"
    except(Exception) as error:
        print("Error: ", error)

def validate():
    xml = input("Insert XML file: ")
    xsd = input("Insert XSD file: ")
    try:
        conn = conect_rpc()
        print(conn.validate(xml, xsd))
    except(Exception) as error:
        print("Error: ", error)

## MUDAR O NOME DESTA FUNCAO
def insert_doc():
    try:
        name = input("Insert a name: ")
        file = input("Insert the file: ")
        conn = conect_rpc()
        ficheiro = open(file, encoding="UTF8").read()
        result = conn.insert_file(name, ficheiro)
        print("Output: " + str(result))
    except(Exception) as error:
        print("Error: ", error)

def getAthleteByName():
    try:
        name = input("Insert the athelete name: \n EX: A Lamusi\n")
        id = input("Insert the id of de row: ")
        conn = conect_rpc()
        result = conn.getAthleteByName(name, id) #, id
        print("Athele Info:\n\tName: "+ result[1][0] + "\n\tSex: " + result[2][0] + "\n\tAge: "+ result[3][0])
    except(Exception) as error:
        print("Error: ", error)

def menu():
    while True:
        print("1 - Convert CSV to XML")
        print("2 - Validate XML with Schemma")
        print("3 - Insert new XML Document")
        print("4 - Get Athlete by name")
        print("0 - Quit")
        escolha = input("Choose a option: ")
        if escolha == "1":
            convert_()
        if escolha == "2":
            validate()
        ## MUDAR O NOME DESTA FUNCAO
        if escolha == "3":
            insert_doc()
        if escolha == "4":
            getAthleteByName()
        if escolha == "0":
            print("Bye")
            quit()

def main():
    menu()

if __name__ == "__main__":
    main()