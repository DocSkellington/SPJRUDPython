import Operations
from Database import Database

class InvalidKeywordException(Exception):
    pass

def parse(request, pieces, ope=""):
    """ Parses a SPJRUD request and return a list with the keywords.
    For example, Proj(['Name'], Rel('Cities')) returns ['Proj', [['Name'], 'Rel', ['Cities']]]. See exempleDécomposition.txt for further example
    """
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
        comparator = None
        if decomposition[1][0] == "Eq":
            comparator = Operations.Equal()
        elif decomposition[1][0] == "Di":
            comparator = Operations.Different()
        elif decomposition[1][0] == "Gr":
            comparator = Operations.Greater()
        elif decomposition[1][0] == "Le":
            comparator = Operations.Lesser()
        else:
            raise InvalidKeywordException(decomposition[1][0] + " is not a valid comparator")
        const = (decomposition[1][1][1] == 'Cst')
        return Operations.Selection(decomposition[1][1][0], comparator, decomposition[1][1][2][0], const, buildAST(decomposition[1][2:], database))
    elif decomposition[0] == "Proj":
        if len(decomposition[1][0]) == 0:
            raise InvalidParameterException("You must provide at least one column to Project")
        return Operations.Projection(decomposition[1][0], buildAST(decomposition[1][1:], database))
    elif decomposition[0] == "Join":
        pass
    elif decomposition[0] == "Rename":
        return Operations.Rename(decomposition[1][0], decomposition[1][1], buildAST(decomposition[1][2:], database))
    elif decomposition[0] == "Union":
        pass
    elif decomposition[0] == "Diff":
        pass
    elif decomposition[0] == "Rel":
        return Operations.Relation(decomposition[1][0], database)
    else:
        raise InvalidKeywordException(decomposition[0] + " is not a valid operation. Please refer to the manual.")

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
