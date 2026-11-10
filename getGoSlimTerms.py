from openpyxl import load_workbook
import re


go_slim_fly_1_terms = []
go_slim_fly_2_terms = []
go_slim_other_1_terms = []
go_slim_other_2_terms = []


wb = load_workbook("input/GO_slim_1_2.xlsx")
ws = wb.active  # or wb["SheetName"]
print(wb.sheetnames)

for row in ws.iter_rows(values_only=True):
    row = list(row)
    row[0] = str(row[0]).strip()
    row[1] = str(row[1]).strip()
    if row[0] != "None":
        #print(row[0])
        if re.match(r"^GO", row[0]):
            go_slim_fly_1_terms.append(row[0])
        
    if row[1] != "None":
        #print(row[1])
        if re.match(r"^GO", row[1]):
            go_slim_fly_2_terms.append(row[1])
    



ws = wb["other species"]

for row in ws.iter_rows(values_only=True):
    row = list(row)
    row[0] = str(row[0]).strip()
    row[1] = str(row[1]).strip()
    if row[0] != "None":
        #print(row[0])
        if re.match(r"^GO", row[0]):
            go_slim_other_1_terms.append(row[0])
    if row[1] != "None":
        #print(row[1])
        if re.match(r"^GO", row[1]):
            go_slim_other_2_terms.append(row[1])
#ws = wb["other species"]