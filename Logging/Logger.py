#                   _____   ______  ______ _______  ______
#           |      |     | |  ____ |  ____ |______ |_____/
#           |_____ |_____| |_____| |_____| |______ |    \_
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: August 2014
#          Version: Extended Edition
#
# This class performs the logging of events for the OSP Extended Edition.
# Is is designed to be created at the commencement of the program and then
# handed to each component for their logging purposes. Verbosity levels
# determine what get logged, their are independent levels for file logging
# and print logging. Fatal error are always printed. File output is also
# formatted to a specified width and indented under a time entry for easy
# reading, for example outputs consult the design document.

from datetime import datetime
from LogEvents import *
__author__ = 'u5195918'


class Logger:

    def __init__(self, log_file_name, file_verbosity, std_out_verbosity,
                 log_file_width):
        # Variables pretty self explanatory
        # Verbosity levels are different for
        self.log_file_name = log_file_name
        self.file_verbosity = file_verbosity
        self.std_out_verbosity = std_out_verbosity
        self.log_file_width = log_file_width

        # Attempt to open logging file.
        self.log_file = self.open_log_file()

        # Build padding string (this is an optimisation)
        # for use when padding out log entries
        self.date_width = 21
        self.padding = self.create_padding(self.date_width)

        # Is the width appropriate?
        self.minimum_width = 40
        self.default_width = 80

        if self.log_file_width < self.minimum_width:
            # If not adjust it.
            requested_width = self.log_file_width
            self.log_file_width = self.default_width
            self.text_width = self.log_file_width - self.date_width
            self.log(LogWidthSizeError(requested_width, self.default_width))


        self.write_heading()

    def log(self, log_object):
        # So we've been handed a log object and now
        # are required to log it.

        # Was it fatal?
        # TODO Make this cleaner, this is checked too many times
        if log_object.fatal:
            fatal_string = 'FATAL: '
        else:
            fatal_string = ''

        # Check the verbosity level
        if log_object.verbosity <= self.std_out_verbosity or log_object.fatal:
            # Log to standard output
            print fatal_string + str(log_object)

        if log_object.verbosity <= self.file_verbosity:
            # Log to file
            self.write_to_file(fatal_string + str(log_object))

        if log_object.fatal:
            # Close file
            self.log_file.close()
            quit()

    def write_to_file(self, log_string):
        # Formats and writes the string to the file
        self.log_file.write(self.format(log_string))

    def format(self, input_string):
        # Takes a character string representing what is wished to be logged
        # adds a date at the front and formats it to width specified.
        # The date plus colon appended to the front is 21 characters wide
        # therefore widths are the provided logging width - date_width
        return_string = ''
        no_of_words_on_line = 0
        current_line_length = 0
        first_word = True

        # Split the input string into words
        input_words = input_string.split()

        for word in input_words:
            if first_word:
                # This is the first word on the first line, just append
                return_string += word + ' '
                current_line_length += len(word) + 1
                no_of_words_on_line += 1
                first_word = False

            elif current_line_length + len(word) > self.text_width:
                # This word will push us over the length, append new line
                # but first remove the trailing space
                return_string = return_string[:-1] \
                    + '\n' + self.padding + word + ' '

                no_of_words_on_line = 1
                current_line_length = len(word) + 1

            else:
                # We can add the word!
                return_string += word + ' '
                no_of_words_on_line += 1
                current_line_length += len(word) + 1

        # Close off with a new line
        return_string += '\n'

        # Add the time
        return self.time() + return_string

    def open_log_file(self):
        try:
            # Open in append + updating mode
            return open(self.log_file_name, 'a+')
        except IOError:
            print('Error Opening Logging File')
            quit()

    def write_heading(self):
        # Attempt to write heading to logging file
        try:
            self.write_to_file('Logging Commenced, File Verbosity: '
                               + str(self.file_verbosity))
        except IOError:
            print('Error Writing to Logging File')
            # TODO is this actually fatal?
            quit()

    @staticmethod
    def time():
        # Simple method that returns a string of the current time.
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S: ')

    @staticmethod
    def create_padding(width):
        # Create a list of spaces of a specific width
        padding = ''

        for i in range(width):
            padding += ' '

        return padding