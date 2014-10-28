# OSP Data Analyzer

# ospdata.py
# Extracts data from the SQL Database
# By Elliot Osborne (u4670030)

import config
import psycopg2
import datetime
import json

from Logging import LogEvents

# Print out each SQL query as it's executed?
debug_sql = False

# Convert types which the JSON module can't serialize to something it can
def make_serializable(obj):
        if type(obj) is datetime.datetime:
                return obj.strftime("%y-%m-%d %H:%M:%S")
        else: return obj

# Fetch data from the database. 
def make_report(options, logger=None):
    try:
            dname = options.database_name
            uname = options.database_user
            conn = psycopg2.connect(dbname=options.database_name, user=options.database_user)
            cur = conn.cursor()
    except e:
            logger.log(LogEvents.DBConnectionFailure(dname, uname))
            sys.exit(1)
    
    # Columns we want from the database
    cols = ["title", "result", "machine_name", "date", "description", "resolution"]

    # Names present in Alex' code in javascript_report.hm
    colnames = ["test", "result", "machinename", "date", "description", "resolution"]

    if len(cols) != len(colnames): raise Exception("cols/colnames mismatch")

    query = "SELECT " + ", ".join(cols) + \
        " FROM tests as t " \
        " JOIN definitions as d ON t.definition_id = d.id " \
        " JOIN machines as m on t.machine_name = m.name "
    
    # Build filter list from configuration
    # parameters are used with psycopg's mogrify to avoid sql-injection
    where_clauses = []
    parameters = ()        
    for option in config.options.itervalues():
        if option.set and option.val_to_where is not None:
            clause, ps = option.val_to_where(option.value)
            # Make sure we've given all the parameters we said 
            # we would.
            if not clause.count("%s") == len(ps):
                raise Exception("option parameter"
                                " mismatch, (%s %s/%s)" %(option.name,
                                                          clause.count("%s"),
                                                          len(ps)))
            else:
                where_clauses.append(clause);
                parameters += ps
                        
    # Combine the clauses into the query
    if where_clauses:
        query += "\n WHERE " + " AND ".join(where_clauses)
        # Apply the parameters
        query = cur.mogrify(query, parameters)
        
        # Final semicolon                
        query += ";"
            
        #  Output Query for debug purposes
        # todo: replace debug_sql with Theo's logging module.
        if debug_sql: 
            print "Executing SQL Query:"
            print query
    try:
            cur.execute(query)
            results = cur.fetchall()
    except e:
            logger.log(LogEvents.GeneralExecutionFailure, e)
    if debug_sql:
        print query
        print "RESULTS:"
        print results

    # Convert it all to Javascript data with the appropriate names for Alex' report.
    try:
            results = json.dumps([dict(zip(colnames, map(make_serializable, row))) for row in results])
    except e:
            logger.log(LogEvents.SerializationError(e))
    
    # Load in the report template
    report = file("report_template.htm").read();

    # Put in the data 
    report = report.replace("//<!-- ospdata.py insertion point 515E9F05FB142DCECDB71F72DA96BAABD7503266D6E1E95989D06A296A0EF9C -->", 'var data = {"resultdata":' + results + '};')

    # And write it out to the requested file.
    file(options.output_file, "w").write(report);

