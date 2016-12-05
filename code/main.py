import Operations
from Database import Database

class InvalidKeywordException(Exception):
    pass

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
        
def buildAST(decomposition, database):
    """ Takes the information from the decomposition list and returns the corresponding AST """
    print("Working on:")
    print(decomposition)
    if decomposition[0] == "Select":
        # Searching the comparator
        if decomposition[0][0] == "Eq":
            comparator = Equal()
        elif decomposition[0][0] == "Di":
            comparator = Different()
        elif decomposition[0][0] == "Gr":
            comparator = Greater()
        elif decomposition[0][0] == "Le":
            comparator = Lesser()
        else:
            raise InvalidKeywordException
    elif decomposition[0] == "Proj":
        pass
    elif decomposition[0] == "Join":
        pass
    elif decomposition[0] == "Rename":
        pass
    elif decomposition[0] == "Union":
        pass
    elif decomposition[0] == "Diff":
        pass
    elif decomposition[0] == "Rel":
        return Operations.Relation(decomposition[1][0], database)
    else:
        raise InvalidKeywordException

def parser(database, request):
    """ Parses the SPJRUD request and returns the corresponding AST """
    decompo = []
    parse(request, decompo)
    return buildAST(decompo, database) 

print("Please type the name of the database you want to use.")
database = input()
db = Database()
db.connect_to_SQL(database)
print("Please insert your SPJRUD request.")
request = input()
ast = parser(db, request)
if ast.check():
    print("ok")
else:
    print("nok")
