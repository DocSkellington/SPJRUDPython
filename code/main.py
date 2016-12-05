import Operations
from Database import Database

class InvalidKeywordException(Exception):
    pass

class InvalidRequestException(Exception):
    pass

def decomposition(request, pieces):
    """ Parses a SPJRUD request and return a list with the keywords.
    For example, Proj(['Name'], Rel('Cities')) returns ['Proj', [['Name'], 'Rel', ['Cities']]]. See exempleDécomposition.txt for further example
    Args:
        request (str): The request in SPJRUD
        pieces (str): The list we must store the decomposition in
    """
    curName = ""
    j = 0
    inStr = False
    typeStr = ""
    i = 0
    while i < len(request):
    # The ' and " mark the start and the end of a str. Everything within a str must not be processed by the parser. A str starting by a " must end by a " (same thing for ')
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
                if request[i] == '[':
                    # A [ marks the start of a list (used by Projection)
                    subp = []
                    k = decomposition(request[i+1:], subp)
                    pieces.append(subp)
                    i += k+1
                elif request[i] == '(':
                    # If we have a (, we have a new operation to parse.
                    pieces.append(curName)
                    curName = ""
                    subp = []
                    # We pass the part of the request we need to process next. subp contains the decomposition of this sub-request.
                    k = decomposition(request[i+1:], subp)
                    pieces.append(subp)
                    i += k+1
                elif request[i] == ",":
                    # A , marks a new element in an operation
                    if curName != "":
                        pieces.append(curName)
                    curName = ""
                elif request[i] == ')' or request[i] == ']':
                    # A ) marks the end of an operation and a ] marks the end of a list. In this case, we return the index we arrived at
                    if curName != "":
                        pieces.append(curName)
                        curName = ""
                    return i
                elif not request[i] == " ":
                    # A space is considered as a part of the string we are working on
                    curName += request[i]
        i += 1

    if curName != "":
        if inStr:
            raise InvalidRequestException("Missing a " + typeStr + " in " + request[0:])
        else:
            raise InvalidRequestException("Missing a ')' or ']' in " + request[0:])
        
def buildAST(decomposition, database):
    """ Takes the information from the decomposition list and returns the corresponding AST
    Args:
        decomposition (list of str): The result of the decomposition function (or a subpart of it)
        database (Database.Database): The database we want to use
    """
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
        # Is it a constant?
        const = (decomposition[1][1][1] == 'Cst')
        # We give the column name, the comparator, the constant/column name to compare, if it is a constant and the sub operation
        return Operations.Selection(decomposition[1][1][0], comparator, decomposition[1][1][2][0], const, buildAST(decomposition[1][2:], database))
    elif decomposition[0] == "Proj":
        if len(decomposition[1][0]) == 0:
            raise InvalidParameterException("You must provide at least one column to Project")
        return Operations.Projection(decomposition[1][0], buildAST(decomposition[1][1:], database))
    elif decomposition[0] == "Join":
        pass
    elif decomposition[0] == "Rename":
        # We give the name to replace, the new name to use and the operation to proceed next
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
    """ Parses the SPJRUD request and returns the corresponding AST
    Args:
        database (Database.Database): The database we want to use (it must already be connected)
        request (str): The SPJRUD request
    """
    decompo = []
    # We decompose the request into a list we can use
    decomposition(request, decompo)
    # We can build the AST with the list
    return buildAST(decompo, database) 

print("Please type the name of the database you want to use.")
database = input()
db = Database()
db.connect_to_SQL(database + ".db")
print("Please insert your SPJRUD request.")
request = input()
ast = parser(db, request)
if ast.check():
    print("ok")
else:
    print("nok")
