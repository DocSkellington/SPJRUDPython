
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
