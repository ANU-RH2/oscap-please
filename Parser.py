#                  _____  _______  ______ _______ _______  ______
#                 |_____] |_____| |_____/ |______ |______ |_____/
#                 |       |     | |    \_ ______| |______ |    \_
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: October 2014
#          Version: Extended Edition
#
# This is a simple command line parsing module, basically it is handed the
# user inputted command line arguments and then generated an options
# object from them. Unfortuntely I was unable to use the python modules
# related to parsing, as the one in 2.6 doesn't support multiple parameters
# to a single argument, and using the one available in Python 3 is an
# external library in Python 2.6, I don't think we need another dependency.
# At any rate, this module uses GetOpt and is thus a bit lower level, but
# it does the job.

__author__ = 'u5195918'
import getopt


class Parser:

    def __init__(self, arguments_string):
        self.arguments_string = arguments_string

    def parse_arguments(self):
        # Parse command line arguments
        # Since we are using an early version of Python, and optparse
        # doesn't handle multiple arguments, we'll have to go semi-manual
        # and go with getopt and some homebrew solutions

        # Set defaults
        insert_mode = False
        output_mode = False
        input_files = []
        database_name = 'osp'
        database_user = 'postgres'
        config_file = 'osp.cfg'
        output_file = 'osp_report.html'
        verbosity = 2
        file_verbosity = 4
        log_file_name = 'osp.log'
        log_file_width = 80

        try:
            opts, args = getopt.getopt(self.arguments_string,
                                       "hio:d:u:v:w:c:l:m:f", ["help",
                                       "insert", "output=",
                                       "database=", "dbuser=",
                                       "verbosity=", "fileverb=",
                                       "configfile=", "logfile=",
                                       "logfilewidth=", "files"])

            # Loop through arguments
            for opt, arg in opts:
                if opt in ('-h', '--help'):
                    self.print_help()
                if opt in ('-i', '--insert'):
                    # Insert Mode
                    insert_mode = True
                if opt in ('-o', '--output'):
                    # Output Mode
                    output_mode = True
                    output_file = arg
                if opt in ('-d', '--database'):
                    database_name = arg
                if opt in ('-u', '--dbuser'):
                    database_user = arg
                if opt in ('-v', '--verbosity'):
                    verbosity = int(arg)
                if opt in ('-w', '--fileverb'):
                    file_verbosity = int(arg)
                if opt in ('-c', '--configfile'):
                    config_file = arg
                if opt in ('-l', '--logfilename'):
                    log_file_name = arg
                if opt in ('m', '--logfilewidth'):
                    log_file_width = arg

            input_files = args

        except Exception:
            # If anything goes wrong, just print the help
            self.print_help()

        # Check if we have any argument issues
        if not insert_mode and not output_mode:
            self.display_error('Please select a mode of operation, data '
                               'insertion or report generation')

        if insert_mode and output_mode:
            self.display_error('Cannot both insert data and output HTML report,'
                               ' please select one or the other')

        if not input_files and insert_mode:
            self.display_error('Please provide files for insertion')

        if output_mode and input_files:
            print input_files
            self.display_error('Cannot insert files whilst performing report'
                               ' generation')

        # Create options object to hand back
        return Parser.Options(insert_mode,
                              output_mode,
                              input_files,
                              database_name,
                              database_user,
                              config_file,
                              output_file,
                              verbosity,
                              file_verbosity,
                              log_file_name,
                              log_file_width)

    @staticmethod
    def display_error(error):
        print error
        quit()

    @staticmethod
    def print_help():
        # Print the help function and exit
        print 'usage: oscap-please.py (-o <file> | -h | -i ) ' \
              '[-c <file>] [-d <dbname>] ' \
              '[-u <dbuser>] [-l <logfile>] [-m <width>] ' \
              '[-v <level>] [-w <level>] -f <files>...'
        print ''
        print 'oscap-please OpenSCAP result storage and report generation'
        print ''
        print ' -h   --help         Display this help message'
        print ' -o   --output       Select report generation mode and specify '\
              'report output file [default: osp_report.html]'
        print ' -i   --insert       Select data insertion mode'
        print ' -f   --files        OpenSCAP XML files for insertion, only' \
              'applicable if insert mode is selected'
        print ' -c   --config       Select configuration file to read from ' \
              '[default: osp.cfg]'
        print ' -d   --database     Select database to generate report from ' \
              '[default: osp]'
        print ' -u   --dbuser       Specify database user with which to ' \
              'connect with [default: postgres]'
        print ' -l   --logfilename  Specify file to write log information to' \
              ' [default: osp.log]'
        print ' -m   --logfilewidth Specify formatted width of log file ' \
              '[default: 80]'
        print ' -v   --verbosity    Specify standard output logging verbosity'
        print ' -w   --fileverb     Specify log file logging verbosity'
        print ' -f   --files        OpenSCAP XML files for insertion, only' \
              ' applicable if insert mode is selected'
        print ''
        quit()

    class Options:
        # Options object used to encapsulate command line parameters
        def __init__(self, insert_mode, output_mode, input_files,
                     database_name, database_user, config_file,
                     output_file, verbosity, file_verbosity, log_file_name,
                     log_file_width):

            self.insert_mode = insert_mode
            self.output_mode = output_mode
            self.input_files = input_files
            self.database_name = database_name
            self.database_user = database_user
            self.config_file = config_file
            self.output_file = output_file
            self.verbosity = verbosity
            self.file_verbosity = file_verbosity
            self.log_file_name = log_file_name
            self.log_file_width = log_file_width

        def __str__(self):
            return '(Insert Mode: ' + str(self.insert_mode) + \
                   ', Output Mode: ' + str(self.output_mode) + \
                   ', Input Files: ' + str(self.input_files) + \
                   ', Database Name: ' + str(self.database_name) + \
                   ', Database User: ' + str(self.database_user) + \
                   ', Config File: ' + str(self.config_file) + \
                   ', Output File: ' + str(self.output_file) + \
                   ', Verbosity: ' + str(self.verbosity) + \
                   ', File Verbosity: ' + str(self.file_verbosity) + \
                   ', Log File: ' + str(self.log_file_name) + \
                   ', Log File Width: ' + str(self.log_file_width) + ')'