__author__ = 'Sauski'
# Controller class, responsible for
# Coordinating the whole thing.
#Import our XML Parsing Library

import xml.etree.ElementTree as ET
import OVALCollection
import XCCDFCollection
import psycopg2

# Parse XML File
# Remove any namespace while we're at it!
tree = ET.iterparse('oval-results.xml')
for _, el in tree:
    el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
root = tree.root

# Are we doing XCCDF or OVAL?
testType = root.find('TestResult')
if testType is not None:
    #XCCDF
    xccdf = True
else:
    xccdf = False

if xccdf:
    # XCCDF
    # Get host name
    machineName = (root.find('TestResult')).find('target').text

    # Grab the date
    status = root.find('status')
    date = status.get('date') #TODO normalise output dates

    testCollection = XCCDFCollection.XCCDFCollection(machineName, date, root)


else:
    # OVAL
    # Grab host name TODO THIS IS DUMB
    for host in root.getiterator('primary_host_name'):
        machineName = host.text

    # Figure out the date run
    generator = root.find('generator')
    date = generator.find('timestamp')
    date = date.text

    # Create a collection object and pass the relevant information
    testCollection = OVALCollection.OVALCollection(machineName, date, root)

print(testCollection)

testCollection.buildDefinitions()

# Alright, lets try and open the database
dbname = 'osp'
user = 'postgres'
try:
    connectionString = 'dbname=' + dbname + ' user=' + user
    conn = psycopg2.connect(connectionString)
except Exception, e:
    print ("Failure Connecting to Database, Check that Database "
           + dbname + " exists and user " + user + " can connect")
    exit()

# DB Open, setup the cursor
cur = conn.cursor()

# Create the table, TODO check if table already exists
execution_string = "create table osp(\
                        Machine_Name VARCHAR(255) NOT NULL,\
                        Definition_Name VARCHAR(255) NOT NULL,\
                        Result VARCHAR(255) NOT NULL,\
                        Date VARCHAR(255) NOT NULL,\
                        PRIMARY KEY(Machine_Name, Definition_Name, Date)\
                        );"
try:
    cur.execute(execution_string)
except Exception, e:
    print("Failure Creating Table")
    print(e.pgerror)

conn.commit()

# TODO I assume at this point we should check if the collection already exists
# JUST JAM IT IN

for definition in testCollection.definitions:
    execution_string = 'insert into osp(Machine_Name, Definition_Name, Result, Date) \
                         values(' + '\'' + testCollection.machineName + '\'' + ',' + \
                                    '\'' + definition.title.replace('\'', '\\\'') + '\'' + ',' + \
                                    '\'' + definition.result.replace('\'', '\\\'') + '\'' + ',' + \
                                    '\'' + testCollection.date + '\'' + ')'
    try:
        cur.execute(execution_string)
    except Exception, e:
        print("Failure Inserting Data")
        print(e.pgerror)

    conn.commit()

# Close it off
cur.close()
conn.close()

# So like...I think we're done here?







