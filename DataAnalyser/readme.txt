* OSP Data Analyser
** Description
   This module interfaces with the database produced by the XML to SQL
   tool. It provides the data as a python dictionary, ready for pretty
   printing.

** Usage
*** Config
    Configuration is done via editing config.cfg 
    The config file consists of lines of the form [option] = [value],
    and comments on lines starting with a #. Blank lines are
    ignored. Anything else will cause the data analyzer to terminate
    with an error.

    At present, the only options are setting the database username and
    password, and filtering results to only those between fixed dates:

| Option      | Value type | Description                           | Example                 |
|-------------+------------+---------------------------------------+-------------------------|
| db_dbname   | string     | Name of database containing OSP data  | db_dbname = osp         |
|-------------+------------+---------------------------------------+-------------------------|
| db_username | string     | Username to use when connecting to db | db_username = osp       |
|-------------+------------+---------------------------------------+-------------------------|
| start_date  | yyyy-mm-dd | Use only results after this date      | start_date = 2014-08-04 |
|             |            | (inclusive, optional)                 |                         |
|-------------+------------+---------------------------------------+-------------------------|
| end_date    | yyyy-mm-dd | Use only results before this date     | end_date = 2014-08-04   |
|             |            | (inclusive, optional                  |                         |
|-------------+------------+---------------------------------------+-------------------------|

*** ospdata.py
This is the main interface to the tool. Just import the module and
call get_MVP(). This will provide a list of python dictionaries with keys
'date' 'machine_name', 'definition_name', and 'result'. Date is a
python datetime.date. The other fields contain strings. Each
dictionary corresponds to a definition tested by OpenSCAP.

You can also test the module by executing it directly: via "python
ospdata.py". This will just print the dictionaries to standard output.
 
*** fakedata.py
This provides semi-random data of the same format as output by
ospdata.py. Its main use is to test code that uses ospdata.py without
having to set up a postgres database.

** Extending ospdata with new options
The config format is defined in config.py
New options are defined by instantiating the ConfigOption class.

The ConfigOption constructor takes four arguments: the name, which
appears on the left of the equals sign in the config file, a function
to convert what appears on the right of the equals sign into a python
object, (optionally) a function to convert the python object into a
filter for the WHERE clause when searching the database, and a boolean
controlling whether or not the new option must be supplied in every
valid configuration file.

