import Operations
import Database
import Description
from Exceptions import *

def check_parenthesises(request):
    """ Checks if the parenthesises (and brackets) are correct.
    """
    stack = []
    other = False
    for i in range(len(request)):
        char = request[i]
        if char == '(' or char == '[':
            stack.append(char)
        elif char == ')' or char == ']':
            if len(stack) == 0:
                raise MissingOpeningParenthesisException(char, '(' if char==')' else '[')
            prev = stack.pop()
            if prev == "(" and char != ")":
                raise InvalidParenthesisException(char, prev, ')', i)
            elif prev == "[" and char != "]":
                raise InvalidParenthesisException(char, prev, ']', i)
        else:
            other = True
    if len(stack) != 0:
        raise MissingParenthesisException(stack.pop())
    return other

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
    return i

    if curName != "":
        if inStr:
            raise InvalidRequestException("Missing a " + typeStr + " in " + request[0:])
        else:
            raise InvalidRequestException("Missing a ')' or ']' in " + request[0:])

def build_AST(decomposition, database):
    """ Takes the information from the decomposition list and returns the corresponding AST
    Args:
        decomposition (list of str): The result of the decomposition function (or a subpart of it)
        database (Database.Database): The database we want to use
    """
    if len(decomposition) == 0:
        raise InvalidRequestException("the request you entered is empty or does not contain any keyword")
    if decomposition[0] == "Select":
        # Searching the comparator
        comparator = None
        if decomposition[1][0] == "Eq":
            comp = "="
        elif decomposition[1][0] == "Di":
            comp = "<>"
            comparator = Operations.Different()
        elif decomposition[1][0] == "Gr":
            comp = "<"
            comparator = Operations.Greater()
        elif decomposition[1][0] == "Geq":
            comp = "<="
            comparator = Operations.GreaterEqual()
        elif decomposition[1][0] == "Le":
            comp = ">"
            comparator = Operations.Lesser()
        elif decomposition[1][0] == "Leq":
            comp = ">="
            comparator = Operations.LesserEqual()
        else:
            raise InvalidKeywordException(decomposition[1][0], "comparator")
        # Is it a constant?
        const = False
        if decomposition[1][1][1] == 'Cst':
            const = True
        elif decomposition[1][1][1] == 'Col':
            const = False
        else:
            raise InvalidKeywordException(decomposition[1][1][1], "type of data for the selection")
        other = decomposition[1][1][2][0]
        try:
            other = int(other)
        except ValueError:
            try:
                other = float(other)
            except ValueError:
                other = other
        comparator = Operations.Comparator(decomposition[1][1][0], comp, other, const)
        # We give the column name, the comparator, the constant/column name to compare, if it is a constant and the sub operation
        return Operations.Selection(comparator, build_AST(decomposition[1][2:], database))
    elif decomposition[0] == "Proj":
        if len(decomposition[1][0]) == 0:
            raise InvalidParameterException("at least one column" , "Project")
        return Operations.Projection(decomposition[1][0], build_AST(decomposition[1][1:], database))
    elif decomposition[0] == "Join":
        return Operations.Join(build_AST(decomposition[1][0:2], database), build_AST(decomposition[1][2:], database))
    elif decomposition[0] == "Rename":
        # We give the name to replace, the new name to use and the operation to proceed next
        return Operations.Rename(decomposition[1][0], decomposition[1][1], build_AST(decomposition[1][2:], database))
    elif decomposition[0] == "Union":
        return Operations.Union(build_AST(decomposition[1][0:2], database), build_AST(decomposition[1][2:], database))
    elif decomposition[0] == "Diff":
        return Operations.Difference(build_AST(decomposition[1][0:2], database), build_AST(decomposition[1][2:], database))
    elif decomposition[0] == "Rel":
        return Operations.Relation(decomposition[1][0], database)
    else:
        raise InvalidKeywordException(decomposition[0], "operation. Please refer to the manual.")

def parser(database, request):
    """ Parses the SPJRUD request and returns the corresponding AST
    Args:
        database (Database.Database): The database we want to use (it must already be connected)
        request (str): The SPJRUD request
    """
    if check_parenthesises(request) == 0:
        raise InvalidSchemaException("you cannot create an empty request")
    decompo = []
    # We decompose the request into a list we can use
    decomposition(request, decompo)
    # We can build the AST with the list
    return build_AST(decompo, database) 

def parse_schema(schema, database):
    """ Parses a schema of a the table from the schema given by the user and add the description in the database
    Args:
        schema (str): The string the user typed with the schema he wants to use
        database (Database.Database): The database to use
    """
    if check_parenthesises(schema) == 0:
        raise InvalidSchemaException("you can not have an empty schema")
    decompo = []
    decomposition(schema, decompo)
    description = Description.Description()
    name = decompo[0]
    for column in decompo[1:]:
        if len(column) >= 3:
            description.add_column(column[0], column[1], column[len(column)-1])
    database.add_description(name, description)

def execute_print(request, database):
    """ Executes the SQL request on the database and prints the result
    Args:
        request (SQLRequest.SQLRequest): The SQL request
        database (Database.Database): The database on which the request must be executed
    """
    description, result = database.execute(str(request))
    columns_names = []
    lengths = []                                # The lengths to use to display each column
    for column in description:
        columns_names.append(column[0])
        lengths.append(len(column[0]))

    for row in result:
        for i in range(len(row)):
            lengths[i] = max(lengths[i], len(str(row[i])))
    hline = "-"
    for length in lengths:
        hline += "-" * (length+3)
    print(hline)
    header = "|"
    for i in range(len(columns_names)):
        header += " " + ("{0:^" + str(lengths[i]) + "s}").format(columns_names[i]) + " |"
    print(header)
    print(hline)
    for row in result:
        rowPrint = "|"
        for i in range(len(row)):
            rowPrint += " " + ("{0:^" + str(lengths[i]) + "s}").format(str(row[i])) + " |"
        print(rowPrint)
        print(hline)


askDb = True
while askDb:
    print("Do you want to use an existing database? (y/n)")
    res = input()
    while res != 'y' and res != 'n':
        print("Please type y if you want to use an existing database or n otherwise")
        res = input()

    db = Database.Database()
    useDb = False
    if res == 'y':
        print("Please type the name of the database you want to use.")
        database = input()
        try:
            db.connect_to_SQL(database + ".db")
            useDb = True
            askDb = False
        except DatabaseException as err:
            print("ERROR: " + str(err))
    else:
        while db.get_number_tables() == 0:
            print("Please type the schema of a table as following: Name, (ColumnName, the SQL type of the column, if it can contain NULL), (ColumnName2, ...), ...\nEnd the sequence with an empty line")
            res = input()
            while res != '':
                try:
                    parse_schema(res, db)
                except ParserException as err:
                    print("ERROR: Your schema does not correspond to our exigences because " + str(err) + ". Please correct it")
                res = input()
            if db.get_number_tables() == 0:
                print("ERROR: Your database must contain at least 1 table.")
            else:
                askDb = False

print("\n\n\n\n")

ok = False
while not ok:
    print("Please insert your SPJRUD request. Enter an empty line to exit the application")
    request = input()

    if request == "":
        ok = True
    else:
        ast = None
        try:
            ast = parser(db, request)
            try:
                ast.check()
                print("You request was correct.")
                request = ast.translate()
                print("The SQL request corresponding to your SPJRUD request is:")
                print(str(request))
                if useDb:
                    execute_print(request, db)
                print("\n\n\n\n")
            except OperationException as err:
                print("ERROR: The expression:")
                print("\t" + request)
                print("is invalid because:")
                print(str(err))
            except DatabaseException as err:
                print("ERROR (Database): The expression:")
                print("\t" + request)
                print("is invalid because:")
                print(str(err))
        except ParserException as err:
            print("ERROR: You did not write the request correctly because " + str(err) + ".")

