from OSP.XMLtoSQL import Definition, Collection

__author__ = 'Sauski'
# A collection is a file basically
# They are uniquely identified by the date they were
# run as well as the computer name.
# XCCDF Collection


class XCCDFCollection(Collection.Collection):

    def __init__(self, xml_root):
        Collection.Collection.__init__(self, xml_root)

    def __str__(self):
        return "(Machine Name: " +SP.XMLtoSQL. self.machine_name + \
               " Date: " + self.date.__str__() + ")"

    def build_definitions(self):
        # Get host name
        self.machine_name = (self.xml_root.find('TestResult')).\
            find('target').text

        # Look through our XML tree and find our definitions
        # First move through the tree to the correct position
        test_results = self.xml_root.find('TestResult')
        rule_results = test_results.findall('rule-result')

        # Setup data to reverse lookup title and description info
        rules = self.xml_root.getiterator('Rule')

        # Grab the date, easiest from a test result
        #TODO Reconsider normalisation, they look the same.
        self.date = rule_results[1].get('time')

        formatted_date = Definition.Definition.Date(self.date[17:19],
                                                    self.date[14:16],
                                                    self.date[11:13],
                                                    self.date[8:10],
                                                    self.date[5:7],
                                                    self.date[:4])
        self.date = formatted_date

        # We have a list of results, iterate over them
        for rule_result in rule_results:
            result = rule_result.find('result').text
            unique_id = rule_result.get('idref')

            #Setup Defaults
            title = 'No Title Found'
            # TODO implement description
            description = 'No Description Found'

            # From the results, look back up the title and description
            for rule in rules:
                if rule.get('id') == unique_id:
                    # Found it
                    title = rule.find('title').text
                    # So often the description will have embedded
                    # The description tag sometimes has other tags inside it...
                    # Which is really, really dumb. So this only returns the
                    # text up to the first tag.
                    description = rule.find('description').text
                    break

            definition_object = Definition.Definition(self.machine_name,
                                                      unique_id,
                                                      title,
                                                      result,
                                                      self.date)
            self.definitions.append(definition_object)

    @staticmethod
    def is_of_type(xml_root):
        # Is this an XCCDF file?
        test_result = xml_root.find('TestResult')
        return test_result is not None
