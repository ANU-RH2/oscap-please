# Generate fake data in the same format as would be returned by
# ospdata.py for testing without database.

import random
import datetime

machine_names = ["Azov", "Baez", "Benz", "Cruz", "Diaz", "Ezra", "Fiji", "Fuji",
                 "Gaza", "Giza", "Inez", "Izod", "Liza", "Lodz", "Nazi", "Puzo",
                 "Ritz", "Ruiz", "Suez", "Suzy", "Tujo"]

definition_names = ["50% of the manual is in .pdf readme files",
                    "had to use hammer to free stuck disk drive heads.",
                    "Program load too heavy for processor to lift.",
                    "bank holiday - system operating credits not recharged.",
                    "Electrical conduits in machine room are melting.",
                    "short leg on process table",
                    "The Borg tried to assimilate your system. Resistance is futile. ",
                    "Telecommunications is downshifting.",
                    "temporary routing anomaly",
                    "Repeated reboots of the system failed to solve problem",
                    "halon system went off and killed the operators.",
                    "Suspicious pointer corrupted virtual machine ",
                    "Standing room only on the bus. ",
                    "PEBKAC (Problem Exists Between Keyboard And Chair)",
                    "old inkjet cartridges emanate barium-based fumes",
                    "Electromagnetic energy loss ",
                    "RPC_PMAP_FAILURE",
                    "Just type 'mv * /dev/null'.",
                    "parallel processors running perpendicular today ",
                    "we just switched to FDDI. " ]

results = ["notapplicable", "notselected", "pass", "fixed", "error", "fail"]


def get_MVP():
    mvp = []
    for x in range(random.randint(15, 25)):
        random.shuffle(machine_names)
        machine_name = machine_names[0]
        random.shuffle(definition_names)
        definition_name = definition_names[0]
        random.shuffle(results)
        result = results[0]

        date = datetime.date(random.randint(1949, 2014), random.randint(1, 12), random.randint(1, 25))

        mvp.append({"machine_name"    : machine_name,
                    "definition_name" : definition_name,
                    "result"          : result,
                    "date"            : date })

    return mvp
        

if __name__ == "__main__":
    results = get_MVP()
    for result in results:
        s = ""
        for key in result.iterkeys():
            s += key + ": '" + str(result[key]) + "' "
        print(s)
