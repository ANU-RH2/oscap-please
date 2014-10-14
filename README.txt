oscap-please: Making OpenSCAP results friendlier

************

* 1. Description **************************************************************

oscap-please (OSP) is a tool for storing historical data from OpenSCAP scans and generating user-friendly HTML documents. As such, there are two main components:
	* The Database component, which takes multiple OpenSCAP scan reports, strips out relevant information and puts it in a database.
	* The Report component, which takes a list of user options and generates a stand-alone HTML document.

oscap-please is in its very early stages and there are many bugs and places for improvement.


* 2. Set-up and Dependencies **************************************************

oscap-please requires a PostgreSQL installation and the python libray psycopg2 to work. Before running, create a database in which you want the historical results data to be stored.


* 3. Usage ********************************************************************

To run, use the command 'python OSP.py [COMMAND]', where command is one of the following:
	* -h: prints help message
	* -i: insert results and key data from multiple OpenSCAP reports into the database. This needs to be used in conjunction with other arguments (see 3.1 below)
	* -r: generate a report from the results stored in the database. The report will be written to the file report.html (see 3.2)

This command must be run as a PostgreSQL user WITHOUT A PASSWORD with access to the database. Please ensure this user also has write access to report.html.

* 3.1 Database Component **************************************************
Command: python OSP.py -i file [files] [-db dbname] [-dbuser dbuser]

Inserts results from an OpenSCAP report (or reports) into a pre-existing database. It will store the time of the scan, the name of the machine as well as the results of each test. It can read XCCDF and OVAL files and can be extended to read more formats.

Optional arguments:
	* -db: specifies the database in which to insert the data. Default is called osp.
	* -dbuser: the user with which to access the database. The default is postgres

* 3.2 Report Generator ****************************************************
Command: python OSP.py -r

Generate an HTML report from data in the database. The end report is stored in report.html (make sure you have write access to this file).

The report generator takes in a list of user customisation options, stored in config.cfg. Templates for possible customisations are left in commented out by default. At current, the date range of scan data is the only customisation option, but we hope to expand this considerably in future versions.

* 4. Improvements *************************************************************

oscap-please is in very early stages and there are many improvements to be made, including
	* Ability to run without being a PostgreSQL user
	* Ability to run as PostgreSQL user with a password
	* Read dbname and dbuser from config.cfg when using -i
	* Better presentation of HTML report
	* Better error handling, especially in regard to XML parsing
	* Ability to link in with an orchestration tool, rather than simply point it to a group of files to be read
