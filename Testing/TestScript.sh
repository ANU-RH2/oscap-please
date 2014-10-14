#!/bin/bash
#                         _______ _______ _______ _______
#                            |    |______ |______    |   
#                            |    |______ ______|    |   
#                                                        
#                  _______ _______  ______ _____  _____  _______
#                  |______ |       |_____/   |   |_____]    |   
#                  ______| |_____  |    \_ __|__ |          |   
#                                                               
#
#		Written By: Theodore Olsauskas-Warren - u5195918
#			In: October 2014
#		   Version: Extended Edition
#
# This script file serves as the home for the external tests written for the
# XMLtoSQL component of the Oh Scap Please program. The general modus operandi
# of the tests within the script is to use the createXCCDF function to make
# an imitation XCCDF XML file, this file contains only the information that
# OSP is lookig for, and is thus significantly smaller than any real world
# XCCDF example file. The tests are designed primarilly around ensuring that
# when OSP fails, or encounters some issue, it correctly logs it and exits
# of it's own accord, rather than simply throwing an exception and crashing.
# The tests included in this file by no means provide a complete coverage of
# all possible test cases, but are more designed with regression and sanity
# testing in mind. For more information on individual tests and the testing
# stratergy as a whole, please refer to the XMLtoSQL testing documentation. 


# General construction variables
xmltag="<?xml version="1.0" encoding=\"UTF-8\"?>"

# XML Construction functions
function wrapWithTag() {
	# Wrap the second argument with the first in tags
	local string="<"$1">"$2"</"$1">"
	echo $string
}

function addProperties() {
	# Add properties to existing, outermost tag
	tag=$1
	for var in "${@:2}"
	do
		# Only add the second var onwards
		tag=$(echo $tag | sed "s@>@ $var>@")
	done
	echo $tag
}

function createXCCDF() {
	# Create an XCCDF file
	# Parameters:
	# 1: Target Name
	# 2: Test Time
	# 3: No. of Passes
	# 4: No. of Fails
	# 5: No. of Not Applicable
	# 6: Random Rule ID's? (0 no, 1 yes)
	# 	No gives each rule a sequential ID, desc and fix
	#	Yes randomises every attribute of the rule

	# Check if we've recieved the correct number of args
	if [ "$#" -ne 6 ]; then
		echo "INTERNAL ERROR:"
  		echo "createXCCDF recieved incorrect number of parameters"
		exit
	fi

	# Create target
	local target=$(wrapWithTag target $1)

	# Create Results and Rules
	results=""
	rules=""
	totalResults=$(($3 + $4 + $5))
	fails=$(($3 + $4))
	for i in `seq 1 $totalResults`;
	do
	        # Which result are we adding?
		if [ "$i" -le "$3" ]
		then
			res="Pass"
		elif [ "$i" -le "$fails" ]
		then
			res="Fail"
		else
			res="Not Applicable"
		fi
	
		result=$(wrapWithTag result "$res")
		ruleRes=$(wrapWithTag "rule-result" "$result")
		if [ $6 -eq 0 ] 
		then
			id=$(echo "$i")
			title=$(echo "${i}th test title")
			desc=$(echo "${i}th test desc")
			fix=$(echo "${i}th test fix")
			
		else
			IDLength=$((32))
			AttLength=$((50))
			# Random ID
			id=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' \
				| fold -w "$IDLength" | head -n 1)
			# Random Title, Desc and Fix
			title=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' \
				| fold -w "$AttLength" | head -n 1)
			desc=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' \
				| fold -w "$AttLength" | head -n 1)
			fix=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' \
				| fold -w "$AttLength" | head -n 1)
		fi	

		# Add properties to result
		newPass=$(addProperties "$ruleRes" "idref=\"$id\""\
				 "time=\"$2\"")
		results=$(echo $results $newPass)
		
		# Make the rule
		title=$(wrapWithTag title "$title")
		desc=$(wrapWithTag description "$desc")
		fix=$(wrapWithTag fix "$fix")
		rule=$(wrapWithTag Rule "$title $desc $fix")
		ruleWID=$(addProperties "$rule" "id=\"$id\"")
	
		# Add rule to list
		rules=$(echo $rules $ruleWID)

	done	

	# Glue together
	TestResult=$(wrapWithTag TestResult "$target $results")
	Benchmark=$(wrapWithTag	Benchmark "$TestResult $rules")
	
	echo $Benchmark
}

function runBasicTest(){
	# Simple function to create an XCCDF file, insert it, then check it
	# inserted correctly, creates a temp file then removes it
	# leaving folder in same state as previously
	# First arugment is location of runner file
	
	createXCCDF localmachine.localgroup \
	"2014-07-20T03:12:40" 1 1 1 0 > XCCDFTestOne.xml.tmp

	# Check for a fatal error
	python $1 -i -v 5 -w 5 -f XCCDFTestOne.xml.tmp | grep 'FATAL' >\
	 /dev/null
	if [ $? -eq 0 ]; then
		# Here we are looking for not matches
		checkFailure 1
	fi
	
	# Check that we have one collection
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM COLLECTIONS;" | grep '1' > /dev/null
	checkFailure $?

	# Check we have three definitions	
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM DEFINITIONS;" | grep '3' > /dev/null
	checkFailure $?
	
	# Check the pass rate is 50 percent
	psql -U "$dbuser" -d "$database" -c \
	"SELECT (pass_rate) FROM COLLECTIONS;" | grep '50' > /dev/null
	checkFailure $?

	# Remove file and clear database
	clearDatabase
	rm -f XCCDFTestOne.xml.tmp
	

}

function runMalformedDateTest(){
	# Create an XCCDF file with an invalid date, make sure OSP
	# picks it up and logs it

	createXCCDF machine.group \
		"2014-07-20T03:12:80" 5 4 2 0 > XCCDFTest.xml.tmp

	# Insert and check that OSP has identified error
	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp | grep 'FATAL' > \
	/dev/null
	checkFailure $?

	# Remove files and clear DB
	clearDatabase
	rm -f XCCDFTest.xml.tmp

}

function runLargeInputTest(){
	# Test that nothing terrible happens with a very large input
	# size, creating the input files takes much, much longer
	# than actually inserting them

	for i in `seq 10 39`;
	do
		# Create 30 collections that have tests with random
		# attributes, all with different names, times and
		# groups
		createXCCDF machine$i.group$i \
		"2014-07-20T12:$i:$i" 3 2 1 1 \
		> XCCDFTest.xml.tmp.$i
	done

	echo -n "."

	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp.* | grep 'FATAL' 
	if [ $? -eq 0 ]; then
		# Here we are looking for not matches
		checkFailure 1
	fi

	echo -n ".. "

	# 30 collections each with 6 tests, means there should be
	# 180 entries in the tests and definitions sections
	
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM DEFINITIONS;" | grep '180' > /dev/null
	checkFailure $?
	
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM TESTS;" | grep '180' > /dev/null
	checkFailure $?

	# Remove files and clear DB
	clearDatabase
	rm -f XCCDFTest.xml.tmp.*
}

function runConnectionIssueTest (){
	# Check that when handed a nonsense database OSP logs a message
	# and exits correctly
	
	# Create Collection
	createXCCDF machine.group \
	"2014-07-20T03:12:40" 4 2 1 1 > XCCDFTest.xml.tmp

	# Attempt connection to non-existent database
	python $1 -i -v 5 -w 5 -d nonexistent -f XCCDFTest.xml.tmp \
	| grep 'FATAL: Failed to connect' > /dev/null
	checkFailure $?

	clearDatabase
	rm -f XCCDFTest.xml.tmp
}

function runIgnoreDuplicatesTest(){
	# Check that OSP correctly identifies that no insetion is
	# required as all the collections already exist
	
	# Create two colections
	createXCCDF machineone.groupone \
	"2014-07-20T03:12:40" 4 2 1 1 > XCCDFTest.xml.tmp.one

	createXCCDF machinetwo.groupone \
	"2013-07-20T03:12:40" 1 2 4 1 > XCCDFTest.xml.tmp.two

	# Insert both the first time
	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp.* | grep 'FATAL' > \
	/dev/null
	if [ $? -eq 0 ]; then
		# Here we are looking for not matches
		checkFailure 1
	fi

	# Second time
	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp.* | \
	grep 'No collections deemed' > /dev/null
	checkFailure $?
	
	clearDatabase
	rm -f XCCDFTest.xml.tmp.*
	
}

function runSchemaConsistencyCheck(){
	# Checks that OSP correctly identifes a mismatch in database
	# relation schemas and exits, logging a useful message

	# Create invalid table schema
	psql -U "$dbuser" -d "$database" -c \
	"CREATE TABLE TESTS(bogus 	VARCHAR(255)	NOT NULL,
			    PRIMARY KEY(bogus))" &> /dev/null

	# Create basic input file
	createXCCDF machine.group \
	"2014-07-20T03:12:40" 3 2 1 0 > XCCDFTest.xml.tmp

	# Attempt insertion
	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp | grep 'FATAL' > /dev/null
	checkFailure $?

	clearDatabase
	rm -f XCCDFTest.xml.tmp

}

function runSanitisationCheck (){
	# Checks thart Psycopg2 is actually sanitising input
	createXCCDF "machine.local" \
	"2014-07-20t03:12:40" 1 0 0 0 | \

	sed "s/1th test title/title')drop table definitions cascade;/"> \
		XCCDFTest.xml.tmp

	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp | grep 'FATAL' > /dev/null
	if [ $? -eq 0 ]; then
		# Here we are looking for not matches
		checkFailure 1
	fi

	# Drop the collections table from the DB
	psql -U "$dbuser" -d "$database" -c \
	"DROP TABLE COLLECTIONS CASCADE;" &> /dev/null

	# Check we didn't lose the table
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM definitions;" | grep 1 > /dev/null
	checkFailure $?

	clearDatabase
	rm -f XCCDFTest.xml.tmp
}
function runDatabaseAlterationTest(){
	# Checks that removing a table in between data additions
	# doesn't affect insertion, of course data may be lost
	# when removing tables, but OSP should be able to mend the
	# damage for future additions

	# Create basic input file
	createXCCDF machine.group \
	"2014-07-20t03:12:40" 3 2 1 0 > XCCDFTest.xml.tmp
	# Insert into DB
	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp  | grep 'FATAL' > /dev/null
	if [ $? -eq 0 ]; then
		# Here we are looking for not matches
		checkFailure 1
	fi
	# Drop the collections table from the DB
	psql -U "$dbuser" -d "$database" -c \
	"DROP TABLE COLLECTIONS CASCADE;" &> /dev/null

	# Re-add collection
	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp | grep 'FATAL' > /dev/null
	if [ $? -eq 0 ]; then
		# Here we are looking for not matches
		checkFailure 1
	fi

	# Check collection was succesfully added
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM COLLECTIONS;" | grep '1' > /dev/null
	checkFailure $?

	clearDatabase
	rm -f XCCDFTest.xml.tmp

}
function runConstraintTest(){
	# Checks that constraints are enforced on definitions
	# i.e. that we don't for some reason get duplicate entries
	# but all tests are preserved

	for i in `seq 1 10`;
	do
		# Create 10 collections, each with exactly the same 
		# definitions and group, but different machines names
		createXCCDF machine$i.group \
		"2014-07-20T03:12:40" 3 2 1 0 > XCCDFTest.xml.tmp.$i

	done

	# Insert and check for error	
	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp.* | grep 'FATAL' > \
	/dev/null
	if [ $? -eq 0 ]; then
		# Here we are looking for not matches
		checkFailure 1
	fi

	# Check that 6 definitions have been created
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM DEFINITIONS;" | grep '6' > /dev/null
	checkFailure $?

	# Check that 10 machines have been created
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM MACHINES;" | grep '10' > /dev/null
	checkFailure $?

	# Check that only one group exists
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM GROUPS;" | grep '1' > /dev/null
	checkFailure $?

	# Check that we have 10 collections
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM COLLECTIONS;" | grep '10' > /dev/null
	checkFailure $?

	# Check that we have 60 tests recorded
	psql -U "$dbuser" -d "$database" -c \
	"SELECT COUNT(*) FROM TESTS;" | grep '60' > /dev/null
	checkFailure $?

	# Remove files and clear DB
	clearDatabase
	rm -f XCCDFTest.xml.tmp.*
	
}

function runCommandLineArgumentTest (){
	# Do some simple argument checks, i.e. make sure that 
	# the location of commands doesn't affect thier validity
	# (within specification), also check that long names
	# work

	# For these tests we can just use a dummy XML file
	# and look at the log output
	echo "<empty>XML</empty>" > DummyXML.xml.tmp

	# Basic Sanity Test
	python $1 -i -v 5 -w 5 -f DummyXML.xml.tmp | \
	grep 'Began extraction on file DummyXML.xml.tmp' > /dev/null
	checkFailure $? 

	# Minimal Long Options
	python $1 --insert --files DummyXML.xml.tmp 	| \
	grep 'Began extraction on file DummyXML.xml.tmp' > /dev/null
	checkFailure $? 
	
	# Full long options
	python $1 --insert --verbosity 5 \
		--fileverb 5 --database osp \
		--dbuser postgres --files DummyXML.xml.tmp  | \
	grep 'Began extraction on file DummyXML.xml.tmp' > /dev/null
	checkFailure $? 

	# Re ordered long options
	python $1 --insert --dbuser 5 \
		--fileverb 5 --database osp \
		--verbosity 5 --files DummyXML.xml.tmp  | \
	grep 'Began extraction on file DummyXML.xml.tmp' > /dev/null
	checkFailure $? 

	# Nonsensical options	
	python $1 --insert --mistake -i | \
	grep 'usage: OSP.py' > /dev/null
	checkFailure $? 

	# Mixture of random options	
	python $1 --insert -v 5 --database osp -w 4 --files DummyXML.xml.tmp| \
	grep 'Began extraction on file DummyXML.xml.tmp' > /dev/null
	checkFailure $? 

	clearDatabase
	rm -f DummyXML.xml.tmp

}

function runPassPercentageTest (){
	# Check that the pass percentages stored in the DB are correct
	# as well as the number of tests reported for each collection

	# Create 10 percent pass collection
	# with 20 non applicable tests
	createXCCDF tenpercent.group \
	"2014-07-20T03:12:40" 1 9 20 0 > XCCDFTest.xml.tmp.1

	# Create 90 percent pass collection 
	# with 0 non applicable tests
	createXCCDF ninetypercent.group \
	"2014-07-20T03:12:40" 18 2 0 0 > XCCDFTest.xml.tmp.2

	# Insert both
	python $1 -i -v 5 -w 5 -f XCCDFTest.xml.tmp.* | grep 'FATAL' > \
	/dev/null
	if [ $? -eq 0 ]; then
		# Here we are looking for not matches
		checkFailure 1
	fi

	# Check that the collection with machine name tenpercent
	# has a 10% pass rate and 10 tests
	psql -U "$dbuser" -d "$database" -c \
	"SELECT (machine_name) FROM COLLECTIONS WHERE pass_rate = 10 AND
	 no_of_tests = 10;" \
		| grep 'tenpercent' > /dev/null
	checkFailure $?

	# Check that the collection with machine name ninety
	# has a 90% pass rate and 20 tests
	psql -U "$dbuser" -d "$database" -c \
	"SELECT (machine_name) FROM COLLECTIONS WHERE pass_rate = 90 AND
	 no_of_tests = 20;" \
		| grep 'ninetypercent' > /dev/null
	checkFailure $?

	clearDatabase
	rm -f XCCDFTest.xml.tmp.*

}
function runInvalidXMLTest(){
	# Check that OSP handles invalid XML files correctly
	# that is logging and exiting

	echo "</broken>This is not very good XML!<broken>" > BadXML.xml.tmp
	
	python $1 -i -v 5 -w 5 -f BadXML.xml.tmp | grep 'Unable to parse' \
		> /dev/null
	checkFailure $?

	# Remove files and clear DB
	clearDatabase
	rm -f BadXML.xml.tmp
}

function checkFailure() {
	# Small helper, checks if the last program execution
	# was sucessful
	# Can also force failure by simply handing in a 1
	if [ $1 -eq 1 ]; then
		echo "FAILED"
		clearDatabase
		rm -f *.tmp
		rm -f *.tmp.*
		exit
	fi
}

function clearDatabase(){
	# It's easier if the DB is cleared before every test

	psql -U "$dbuser" -d \
	"$database" -c "drop schema public cascade;" &> /dev/null
	psql -U "$dbuser" -d \
	"$database" -c "create schema public;" &> /dev/null

	checkFailure $?
}

# Start the script
# Parameters:
# 1: Location of Runner.py or equivilent
# 2: Database to connect to, default osp
# 3: User to connect as, default postgres
echo ""
echo "Welcome to the Oh Scap Please XMLtoSQL Test Script"

# Set defauls
database='osp'
dbuser='postgres'

# Check and save input parameters
if [ "$#" -ge 1 ]; then
	runner=$1
fi
if [ "$#" -ge 2 ]; then
	database=$2
fi
if [ "$#" -ge 3 ]; then
	dbuser=$3
fi
if [ "$#" -eq 0 ]; then
	echo "This script requires the location of Runner.py be specified"
fi

echo "Warning! This script will destroy the public schema of database $database"
echo ""
# Clear database
echo -n "Clearing Database $database... "
clearDatabase
echo "Complete"

# Perform basic test
echo -n "Starting basic test... "
runBasicTest $runner
echo "Complete"

# Perform insertion constrain test
echo -n "Starting insertion constraint test... "
runConstraintTest $runner
echo "Complete"

# Perform malformed date test
echo -n "Starting malformed date test... "
runMalformedDateTest $runner
echo "Complete"

# Perform bad XML test
echo -n "Starting malformed XML test... "
runInvalidXMLTest $runner
echo "Complete"

# Perform ignore duplicates test
echo -n "Starting ignore duplicates test... "
runIgnoreDuplicatesTest $runner
echo "Complete"

# Perform database schema consistency check
echo -n "Starting database schema consistency test... "
runSchemaConsistencyCheck $runner
echo "Complete"

# Perform connection issue test
echo -n "Starting connection issue test... "
runConnectionIssueTest $runner
echo "Complete"

# Perform Pass percentage and test count test
echo -n "Starting pass percentage and test count test... "
runPassPercentageTest $runner
echo "Complete"

# Perform database integrity alteration test
echo -n "Starting database alteration test... "
runDatabaseAlterationTest $runner
echo "Complete"

# Perform command line interpretation test
echo -n "Starting command line argument test... "
runCommandLineArgumentTest $runner
echo "Complete"

# Perform database entry sanitisation check
echo -n "Starting sanitisation check..."
runSanitisationCheck $runner
echo "Complete"

# Perform Large Input test
echo -n "Starting large input test"
runLargeInputTest $runner
echo "Complete"

echo ""
echo "All tests complete"

exit
