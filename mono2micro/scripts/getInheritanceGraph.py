"""
Gets the semantic inheritance dependency graph between classes. Requires the refTable-rich.json file in the workspace folder of the mono2micro application.
Only extracts the children of each class, not the parents.

ex.) python getInheritanceGraph refTable-rich.json

"""

import sys
import json

def getClassNames(refTableFile):
     json_file =  open(refTableFile,)
     refTable_json = json.load(json_file)

     # Gets all class names
     class_inheritance_graph_file = open("class_inheritance_dependencies.rsf", "x")
     for class_name in refTable_json["Inherit"]["Details"]:
        #for parent in refTable_json["Inherit"]["Details"][class_name]["parents"]:
        #   line = class_name.replace(" ", "") + " " + parent + " " + "1" + "\n"
        #   class_inheritance_graph_file.write(line)
        for child in refTable_json["Inherit"]["Details"][class_name]["children"]:
           line = class_name.replace(" ", "") + " " + child + " " + "1" + "\n"
           class_inheritance_graph_file.write(line)

if __name__ == "__main__":
    refTableFile = sys.argv[1]
    getClassNames(refTableFile)

