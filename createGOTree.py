"""
FOR VERSION 2
"""
from datetime import date
import re
import sys

today = date.today()
date_str = today.strftime("%Y-%m-%d")

reverseDict = {}
recordDict = {}

go_basic_file = "input/go-basic.obo"
outputFile = f"output/{date_str}_GO_Tree.tsv"

def findAllChildren(firstChild, unique_set, original_children_set):
    if firstChild not in unique_set and firstChild not in original_children_set:
        unique_set.add(firstChild)
    if firstChild in reverseDict.keys():
        for newValue in reverseDict[firstChild]['children']:
            if newValue != firstChild:
                newResult = findAllChildren(newValue, unique_set, original_children_set)

    return unique_set



def main():
    with open(go_basic_file, 'r') as gofile:
        currentID = ""
        currentNamespace = ""
        currentName = ""
        for line in gofile:
            line = line.strip()
    
            if line.startswith('[Term]'):
                recordDict[currentID] = {}
                recordDict[currentID]['namespace'] = currentNamespace
                recordDict[currentID]['name'] = currentName
    
                currentID = ""
                currentNamespace = ""
    
    
            elif line.startswith('id'):
                lineArray = line.split()
                currentID = lineArray[-1].strip()
    
    
            elif line.startswith('namespace'):
                lineArray = line.split()
                currentNamespace = lineArray[-1].strip()
    
            elif line.startswith('name:'):
                lineArray = line.split(":")
                currentName = lineArray[-1].strip()
    
            elif line.startswith('is_a:'):
                lineArray = line.split()
                relationship_id = lineArray[1].strip()
                if relationship_id not in reverseDict.keys():
                    reverseDict[relationship_id] = {}
                    reverseDict[relationship_id]['children'] = set()
                    reverseDict[relationship_id]['children'].add(currentID)
                else:
                    reverseDict[relationship_id]['children'].add(currentID)
    
            elif line.startswith('relationship:'):
                if currentNamespace.strip() != "biological_process":
                    #molecular function and cellular component
                    lineArray = line.split()
                    if lineArray[1] == "part_of":
                        relationship_id = lineArray[2].strip()
                        if relationship_id not in reverseDict.keys():
                            reverseDict[relationship_id] = {}
                            reverseDict[relationship_id]['children'] = set()
                            reverseDict[relationship_id]['children'].add(currentID)
                        else:
                            reverseDict[relationship_id]['children'].add(currentID)
                elif currentNamespace.strip() == "biological_process":
                    lineArray = line.split()
                    relationship_id = lineArray[2].strip()
                    if relationship_id not in reverseDict.keys():
                        reverseDict[relationship_id] = {}
                        reverseDict[relationship_id]['children'] = set()
                        reverseDict[relationship_id]['children'].add(currentID)
                    else:
                        reverseDict[relationship_id]['children'].add(currentID)
            
    
    
    with open(outputFile, 'w') as outfile:
        outfile.write("PARENT GO ID\tPARENT NAMESPACE\tPARENT NAME\tCHILDREN AMOUNT\tCHILDREN LIST\n")
        for recordID in recordDict.keys():
            uniqueSet = set()
            uniqueList = []
            originalChildrenSet = set()
            childrenString = ""
            printLine = ""
            shouldPrint = False
            originalChildren = []
            allChildren = []
                
            if recordID in reverseDict.keys():
                for child in reverseDict[recordID]['children']:
                    originalChildrenSet = set(reverseDict[recordID]['children'])
                    childrenResults = findAllChildren(child, uniqueSet, originalChildrenSet)
                    
                    uniqueList.extend(list(childrenResults))
                    uniqueList = set(uniqueList)
                    uniqueList = list(uniqueList)
                    
                    
                allChildren = list(originalChildrenSet)
                allChildren.extend(uniqueList)
                
                
                if recordID not in uniqueList:
                    uniqueList.append(recordID.strip())
                    allChildren.append(recordID.strip())
                
                
                allChildren = sorted(set(allChildren))
                childrenAmount = len(allChildren)
                childrenString = ";".join(allChildren)
                printLine = f"{recordID}\t{recordDict[recordID]['namespace']}\t{recordDict[recordID]['name']}\t{str(childrenAmount)}\t{childrenString}\n"
                
                outfile.write(f"{recordID}\t{recordDict[recordID]['namespace']}\t{recordDict[recordID]['name']}\t{str(childrenAmount)}\t{childrenString}\n")
                
            else:
                printLine = f"{recordID}\t{recordDict[recordID]['namespace']}\t{recordDict[recordID]['name']}\t1\t{recordID};\n"
                outfile.write(f"{recordID}\t{recordDict[recordID]['namespace']}\t{recordDict[recordID]['name']}\t1\t{recordID};\n")


if __name__ == "__main__":
    main()