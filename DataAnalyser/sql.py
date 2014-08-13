# OSP Sql data fetcher
# ospsql.py

import config
import psycopg2

debug_sql = True

conn = psycopg2.connect(dbname=config.option("db_dbname"),
                        user=config.option("db_username"))

cur = conn.cursor()

def get_MVP():
        # Select the appropriate fields
        # Beacuse the number of where clauses is unkown, 
        # We will be building the query via string concatenation.
        # Be mindful not to introduce an SQL injection opportunity!
 
        query =("SELECT machine_name," 
                "       definition_name," 
                "       result," 
                "       date" 
                "       FROM   osp" )
        
        # Apply any configured options
        where_clause_added = False
        parameters = ()
        for option in config.options.itervalues():
                # todo use an option.set boolean instead of a 
                # value of None to tell if an option has been set
                if (option.val_to_where is not None and
                    option.value        is not None):
                        if not where_clause_added:
                                where_clause_added = True
                                query += " WHERE\n"
                        else: query += "AND "
                        clause, ps = option.val_to_where(option.value)
                        if not clause.count("%s") == len(ps):
                                raise Exception("option parameter"
                                  " mismatch, (%s)" %option.name)
                        else: 
                                query+= clause + "\n"
                                parameters += ps
        
        # Final semicolon                
        query += ";"

        #  Output Query for debug purposes
        if debug_sql: 
                print "Executing SQL Query:"
                print cur.mogrify(query, parameters)
        cur.execute(query, parameters)
        results = cur.fetchall()

        # Convert into an order-independant format
        # Todo: Split into a helper function so we only
        # list the fields once.
        rval = []
        for r in results:
                rdict = {"machine_name" : r[0],
                         "definition_name" : r[1],
                         "result" : r[2],
                         "date" : r[3], }
                rval.append(rdict)

        return rval
