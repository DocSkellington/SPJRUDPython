# Demander à l'utilisateur quelle base de données

def parserRelation(database, request):
    """ Parses a relation request and returns an object of type Relation """
    name = ""
    inStr = False
    for i in range(len(request)):
        if request[i] == '"':
            inStr = not inStr
        elif inStr:
            name += request[i]
        else:
            raise Exception
    return Relation(name, database)

def parse(request, pieces, ope=""):
    curName = ""
    j = 0
    inStr = False
    typeStr = ""
    i = 0
    while i < len(request):
        if request[i] == '"' or request[i] == "'":
            if inStr:
                if request[i] == typeStr:
                    inStr = False
                else:
                    curName += request[i]
            else:
                inStr = True
                typeStr = request[i]
        else:
            if inStr:
                curName += request[i]
            else:
                if request[i] == '(':
                    pieces.append(curName)
                    curName = ""
                    subp = []
                    k = parse(request[i+1:], subp)
                    pieces.append(subp)
                    i += k+1
                elif request[i] == ",":
                    if curName != "":
                        pieces.append(curName)
                    curName = ""
                elif request[i] == ')':
                    if curName != "":
                        pieces.append(curName)
                        curName = ""
                    return i
                elif not request[i] == " ":
                    curName += request[i]
        i += 1
        


def parser(database, request):
    """ Parses the SPJRUD request and returns the corresponding AST """
    decompo = []
    parse(request, decompo)
    print(decompo)

print("Please type the name of the database you want to use.")
database = input()
print("Please insert your SPJRUD request.")
request = input()
ast = parser(database, request)
if ast.check():
    print("ok")
else:
    print("nok")
