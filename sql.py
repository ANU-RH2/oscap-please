# OSP Sql data fetcher
# Elliot Osborne (u4670030)
# ospsql.py

import config
import psycopg2
import datetime

# Print out the exectued SQL statements?
debug_sql = True

# Connect to the database using dbname and username from config file.
conn = psycopg2.connect(dbname=config.option("db_dbname"),
                        user=config.option("db_username"))
cur = conn.cursor()

# Convert types which the JSON module can't serialize to something it can
def make_serializable(obj):
        if type(obj) is datetime.datetime:
                return obj.strftime("%y-%m-%d %H:%M:%S")
        else: return obj

def get_collections():
        cols = ["machine_name", "Date", "no_of_tests", "pass_rate"]
        query = "SELECT " + ", ".join(cols) + " FROM collections JOIN machines ON collections.machine_name = machines.name"

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

        cur.execute(query)
        results = cur.fetchall()
        if debug_sql:
                print "RESULTS:"
                print results
        # The json module doesn't know how to serialize datetime objects,
        # so I'll convert them to strings.
        results = [[make_serializable(val) for val in row] for row in results]
        return results
 
