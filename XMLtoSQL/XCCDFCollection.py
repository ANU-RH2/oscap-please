__author__ = 'Sauski'
# A collection is a file basically
# They are uniquely identified by the date they were
# run as well as the computer name.
# XCCDF Collection
import Definition


class XCCDFCollection:


    def __init__(self, machineName, date, XMLRoot):
        self.machineName = machineName
        self.date = date
        self.XMLRoot = XMLRoot
        self.definitions = []

    def __str__(self):
        return "(Machine Name: " + self.machineName + \
                " Date: " + self.date + ")"

    def buildDefinitions(self):
        # Look through our XML tree and find our definitions
        # First move through the tree to the correct position
        testResults = self.XMLRoot.find('TestResult')
        ruleResults = testResults.findall('rule-result')

        # Setup data to reverse lookup title and description info
        rules = self.XMLRoot.getiterator('Rule')

        # We have a list of results, iterate over them
        for ruleResult in ruleResults:
            result = ruleResult.find('result').text
            id = ruleResult.get('idref')

            # From the results, look back up the title and description
            for rule in rules:
                if rule.get('id') == id:
                    # Found it
                    title = rule.find('title').text
                    # So often the description will have embedded
                    # The description tag sometimes has other tags inside it...
                    # Which is really, really dumb. So this only returns the
                    # text up to the first tag.
                    description = rule.find('description').text
                    break

            definition_object = Definition.Definition(result, id, title, description)
            self.definitions.append(definition_object)