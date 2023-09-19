import xmlrpc.client

def conect_rpc():
    conn = xmlrpc.client.ServerProxy("http://localhost:8000/")
    return conn


def convert_():
    host_file = input("Insert host_file: ")
    medals_file = input("Insert medals_file: ")
    atleta_file = input("Insert atheletes_file: ")
    name_file = input("Insert name: ")
    try:
        conn = conect_rpc()
        conn.convert(host_file, medals_file, atleta_file, name_file)
        return name_file+".xml"
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


# def update_doc():
#     id = input("Insert the ID: ")
#     new_name = input("Insert the new name: ")
#     new_file = input("Insert the new file: ")

#     try:
#         conn = conect_rpc()
#         result = conn.update_file(id, new_name, new_file)
#         print("Output: " + str(result))
#     except(Exception) as error:
#         print("Error: ", error)

def soft_delete():
    id = input("Insert the ID: ")
    try:
        conn = conect_rpc()
        result = conn.delete_file(id)
        print("Output: " + str(result))
    except(Exception) as error:
        print("Error: ", error)

def getAthlete():
    try:
        game = input("Insert the name of the Game: \n EX: tokyo-2020\n")
        disc = input("Insert the discipline: \n EX: Atheletics\n")
        event = input("Insert the event: \n EX: 100 m\n")
        gender = input("Insert the category: \n EX: Men\n")
        medal = input("Insert the medal: \n EX: GOLD\n")
        id = input("Insert the id of de row: ")
        conn = conect_rpc()
        result = conn.get_athlete_data(game, disc, event, gender, medal, id)
        tamanho = len(result)/6
        if(tamanho >= 2):
            for i in range(int(tamanho)):
                p = 6
                p= p*i
                print("Athele Info:\n\tName: "+result[p][0] + "\n\tYear of birth: "+ result[p+1][0] + "\n\tFirst Game: " 
                +result[p+3][0]+ "\n\tNumber of Partifipations: " + result[p+5][0] 
                + "\n\tNumber of Medals: " + result[p+4][0])  
        else:
            print("Athele Info:\n\tName: "+result[0][0] + "\n\tYear of birth: "+ result[1][0]  + "\n\tFirst Game: "
             +result[3][0]+ "\n\tNumber of Partifipations: " + result[4][0] + "\n\tNumber of Medals: " + result[5][0])
 
    except(Exception) as error:
        print("Error: ", error)

def games_contry():
    try:
        id = input("Insert the id of de row: ")
        conn = conect_rpc()
        result = conn.country_for_game(id)
        print("Info:")
        for r in result:
                print("\n\tCountry: "+r[0] + "\n\t\tNumber of times: " + str(r[1]))  
        
    except(Exception) as error:
        print("Error: ", error)
  
def getAthlete_info():
    try:
        name = input("Insert the athelete name: \n EX: Usain BOLT\n")
        id = input("Insert the id of de row: ")
        conn = conect_rpc()
        result = conn.athlelet_info(name, id)
        print("Athele Info:\n\tName: "+result[0][0] + "\n\tYear of birth: "+ result[1][0]  + "\n\tFirst Game: "
        +result[3][0]+ "\n\tNumber of Partifipations: " 
        + result[5][0] + "\n\tNumber of Medals: " + result[4][0])
 
    except(Exception) as error:
        print("Error: ", error)


def gold_for_countries():
    try:
        local = input("Insert the local of the game: \n EX: tokyo-2020\n")
        id = input("Insert the id of de row: ")
        conn = conect_rpc()
        result = conn.country_gold_medals(local, id)
        print("Info:")
        for r in result:
                print("\n\tCountry: "+r[0] + "\n\t\tNumber of gold medals: " + str(r[1]))  
        
    except(Exception) as error:
        print("Error: ", error)

def country_medals():
    try:
        local = input("Insert the local of the game: \n EX: tokyo-2020\n")
        medal = input("Insert the medal: \n EX: GOLD\n")
        pais = input("Insert the 3 letter code of the Country: \n EX: POR\n")
        id = input("Insert the id of de row: ")
        conn = conect_rpc()
        result = conn.count_medals_country_game(local, medal, pais, id)
        print("Info:")
        for r in result:
                print("\n\tCountry: "+r[0] + "\n\t\tNumber of medals: " + str(r[1]))  
        
    except(Exception) as error:
        print("Error: ", error)

def order_names():
    try:
        order = input("Insert the order: \nASC or DESC\n")
        id = input("Insert the id of de row: ")
        conn = conect_rpc()
        result = conn.order_games(order, id)
        print("Info:")
        for r in result:
                print("\n\Game name: "+r[0]) 
        
    except(Exception) as error:
        print("Error: ", error)



def menu():
    while True:
        print("1 - Convert CSV to XML")
        print("2 - Validate XML with Schemma")
        print("3 - Insert new XML Document")
        #print("4 - Update XML Document")
        print("4 - Delete Row from DB")
        print("5 - Get Athlete resumed info from competition")
        print("6 - Get Games in one Country")
        print("7 - Get Athlete info by name")
        print("8 - Get Countries number of gold medals for game")
        print("9 - Get Country medals")
        print("10 - Get Games by order (NAME)")
        print("0 - Quit")
        escolha = input("Choose a option: ")
        if escolha == "1":
            convert_()
        if escolha == "2":
            validate()
        if escolha == "3":
            insert_doc()
        if escolha == "4":
            soft_delete() 
        if escolha == "5":
            getAthlete()
        if escolha == "6":
            games_contry() 
        if escolha == "7":
            getAthlete_info()
        if escolha == "8":
            gold_for_countries() 
        if escolha == "9":
            country_medals()
        if escolha == "10":
            order_names() 
        if escolha == "0":
            print("Bye")
            quit()

def main():
    menu()

if __name__ == "__main__":
    main()

