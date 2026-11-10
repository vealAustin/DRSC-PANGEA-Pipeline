import re
import subprocess



currentName = ""
currentGoID = ""

previousInfo = ""
shouldPrint = False

goInfoDict = {}

progress = 0

print("PROCESSING GO INFO DICT...")

inputFile = "./input/go-basic.obo"
totalLines = int(subprocess.getoutput(f"wc -l {inputFile}").strip().split()[0])

with open(inputFile, 'r') as infile:
    for line in infile:
        line = line.strip()

        if line == "[Term]":
            #print(line)
            previousInfo = ""
            shouldPrint = False
            goInfoDict[currentGoID] = currentName
            
        
        if line.startswith('id'):
            lineArray = line.split()
            currentGoID = lineArray[-1].strip()
        
        elif line.startswith('name:'):
            lineArray = line.split()
            currentName = " ".join(lineArray[1:])
            
        
        progress += 1
        totalProgress = round(progress / totalLines * 100, 2)
        print(f"\r{totalProgress}%", end="")
        
        
        
        
print("\n\nDONE PROCESSING GO INFO DICT...")