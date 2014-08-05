# OSP Sql data fetcher
# ospsql.py

import config
import psycopg2

debug_sql = True

conn = psycopg2.connect(dbname=config.db_dbname,
                        user=config.db_username)

cur = conn.cursor()

def get_MVP():
        # Grab the right data
        fetchstring = "SELECT machine_name, \
                            definition_name, \
                            result, \
                            date \
                            FROM osp"
        # Filter the results
        # Todo: Chaining these is seriously awkward. Config modules
        # are a great idea.
        if config.start_date is not None or config.end_date is not None:
                fetchstring += "\n WHERE \n"
        if config.start_date is not None:
                fetchstring += " date >= " + "'" + config.start_date + "'"
                if config.end_date is not None:
                        fetchstring += " AND "
        if config.end_date is not None:
                fetchstring += "date <= " + "'" + config.end_date + "'"

        # Final semicolon
        fetchstring += ";"

        # Output Query for debug purposes
        if debug_sql:
                print fetchstring

        # Do it!
        cur.execute(fetchstring)
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
