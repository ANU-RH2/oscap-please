oscap-please: Making OpenSCAP results friendlier

************

* 1. Description **************************************************************

oscap-please (OSP) is a tool for storing historical data from OpenSCAP scans and generating user-friendly HTML documents. As such, there are two main components:
	* The Database component, which takes multiple OpenSCAP scan reports, strips out relevant information and puts it in a database.
	* The Report component, which takes a list of user options and generates a stand-alone HTML document.

oscap-please is currently in a polished state, but there are improvements that we'd love to see added to it.


* 2. Set-up and Dependencies **************************************************

oscap-please requires a PostgreSQL installation and the python libray psycopg2 to work. Before running, create a database in which you want the historical results data to be stored.


* 3. Usage ********************************************************************

To run, use the command 'python oscap-please.py [COMMAND]', where command is one of the following:
	* -h: prints help message. This is the best place to go to find out what all the optional commands do
	* -i: insert results and key data from multiple OpenSCAP reports into the database. This needs to be used in conjunction with other arguments (see 3.1 below)
	* -o: generate a report from the results stored in the database. (see 3.2)

For more thorough help on use, see Documentation/User_Guide.pdf. 

* 3.1 Database Component **************************************************
Command: python OSP.py -i -f file [files] 

Inserts results from an OpenSCAP report (or reports) into a pre-existing database. It will store the time of the scan, the name of the machine as well as the results of each test. It can read XCCDF and OVAL files and can be extended to read more formats.

Optional arguments:
	* -db: specifies the database in which to insert the data. Default is called osp.
	* -dbuser: the user with which to access the database. The default is postgres

* 3.2 Report Generator ****************************************************
Command: python OSP.py -o file

Generate an HTML report from data in the database.

The report generator takes in a list of user customisation options, stored in config.cfg. Templates for possible customisations are left in commented out by default. At current, you can filter results by date range, machine name and group.

The base of the HTML report is stored in report_template.htm.  If you want to customise the report to include a company name, logo etc, modify this base file. 

* 4. Improvements *************************************************************

oscap-please has been developed in a relatively short timeframe and there are many improvements that can be made, including:
	* Integration with orchestration tools (i.e. Puppet) to automate the colelction and storage of results data 
	* More XML results formats supported
	* More charts and data views in the report
	* In the report, have the ability to click on a definition and see the solution

To aid future development, we have included a number of technical reports discussing how oscap-please works and our design decisions.  These can be found in the Documentation folder.