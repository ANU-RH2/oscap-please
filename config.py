# OSP Configuration
# ospconfig.py
# Provides the state of user-configuration.
import datetime
import sys
import re
# Dict from option names to associated ConfigOption ojbect
options = {}

""" Get value of configured option """
def option(name):
    if name in options:
        return options[name].value
    else: raise Exception("Undefined option: %s" %name)

# Note on SQL Injection: psycopg2 will automatically
# sanitise input _as long as you pass it correctly_
# val_to_where functions defined below must return a string with %s
# where a parameter is needed, followed by a tuple of the parameters.
# The parameters will be sent to psycopg to sanitise.
# 
# To avoid SQL injection, do this: return "%s", (foo,) # safe
# not this: return "%s" %foo                           # vulnerable

class ConfigOption:
    """An option which can be adjusted by config file.
    name: name of option in config file
    str_to_val: function to convert string in config file to value
    val_to_where (optional): function to convert value
                             to a filter in the WHERE clause
    mandatory: set to True if the option is required in every config
"""
    def __init__(self, name, str_to_val,
                 val_to_where=None, mandatory=False):
        if name in options:
            raise Exception("Re-definition of config option %s."
                            %name)

        self.str_to_val = str_to_val
        self.val_to_where = val_to_where
        self.name = name
        self.value = None
        self.mandatory = mandatory
        self.set = False
        options[name] = self

# Database connection info
ConfigOption("db_username", str, mandatory=True)
ConfigOption("db_dbname", str, mandatory=True)

# Date filtering
def date_from_iso(datestring):
    #todo nice error handling    
    year, month, day = map(int, datestring.split("-"))
    return datetime.date(year, month, day)

def where_only_after(date):
    return "date >= %s", (date.isoformat(),)

def where_only_before(date):
    return "date <= %s", (date.isoformat(),)

ConfigOption("start_date", date_from_iso, where_only_after)
ConfigOption("end_date", date_from_iso, where_only_before)

# Machine name and group filtering
def regexp(exp):
    # We'll use python's regexp compilation to test for a valid regular
    # expression.
    re.compile(exp)
    try: re.compile(exp)
    except: 
        raise Exception("Error: unable to compile regular expression %s" %exp)

    # We need to convert \ to \\ since postgres will interpret them instead
    # of the regex. The python interpreter does the same thing.
    return exp.replace("\\", "\\\\") 

def where_name(exp):
    return "machine_name ~ %s", (regexp(exp),)

def where_group(exp):
    return "group_name ~ %s", (regexp(exp),)

ConfigOption("machine_name", regexp, where_name)
ConfigOption("group_name", regexp, where_group)

# Read the config file
lineno = 0
for line in  file("config.cfg").readlines():
    lineno += 1

    # Remove trailing whitespace
    line = line.strip()

    # Ignore comments and blank lines
    if len(line) == 0: continue
    if line[0] == "#": continue

    # Parse linse of the form [name] = [value]
    parts = line.split(" = ")
    if len(parts) != 2:
        print "Unable to parse config line %d: %s" % (lineno, line)
    if parts[0] in options:
        opt = options[parts[0]]
        opt.value = opt.str_to_val(parts[1])
        opt.set = True
    else:
        print "Unkown option in config %d: %s" % (lineno, line)

# make sure every mandatory option is there
for opt in options.itervalues():
    if opt.mandatory and opt.value is None:
        raise Exception("Mandatory option %s unconfigured."
                        %op.name)
