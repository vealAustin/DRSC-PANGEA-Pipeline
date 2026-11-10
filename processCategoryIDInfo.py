from openpyxl import load_workbook

categoryDict = {}
progress = 0


wb = load_workbook('input/Geneset_assignment.xlsx')

sheet = wb.active
print("PROCESSING CATEGORY ID FILE...")
for row in sheet.iter_rows(values_only=True):
    row = list(row)
    if row[0] is not None:
        #print(row)
        row = [str(x).strip() for x in row]
        
        process = None
        fileId = None
        
        
        category_id = row[0]
        name = row[1]
        name_prev = row[2]
        sub_group_name = row[3]
        group_name = row[4]
        order = row[5]
        speciesId = row[9]
        genome_gene_count = row[10]
        long_description = row[11]
        table_name = row[12]
        
        
        
        
        if "biological process" in name.lower() or "BP" in name:
            process = "biological_process"
        elif "molecular function" in name.lower() or "MF" in name:
            process = "molecular_function"
        elif "cellular component" in name.lower() or "CC" in name:
            process = "cellular_component"
        
        if "Direct" in name:
            fileId = "merge_Direct_GO"
        elif "EXP" in name:
            fileId = "experimental_file"
        elif "HTP" in name:
            fileId = "high_throughput"
        elif "SLIM1" in name:
            fileId = "go_slim_1"
        elif "SLIM2" in name:
            fileId = "go_slim_2"
        elif "flatten" in name_prev.lower():
            fileId = "flattened"
        
        if process == None:
            #print("PROCESS NOT FOUND:", row)
            continue
        
        
        
        
        
        
        if fileId not in categoryDict.keys():
            categoryDict[fileId] = {}
            categoryDict[fileId][speciesId] = {}
            categoryDict[fileId][speciesId][process] = {}
            categoryDict[fileId][speciesId][process]['category_id'] = category_id
            categoryDict[fileId][speciesId][process]['name'] = name
            categoryDict[fileId][speciesId][process]['sub_group_name'] = sub_group_name
        else:
            if speciesId not in categoryDict[fileId].keys():
                categoryDict[fileId][speciesId] = {}
                categoryDict[fileId][speciesId][process] = {}
                categoryDict[fileId][speciesId][process]['category_id'] = category_id
                categoryDict[fileId][speciesId][process]['name'] = name
                categoryDict[fileId][speciesId][process]['sub_group_name'] = sub_group_name
            else:
                if process not in categoryDict[fileId][speciesId].keys():
                    categoryDict[fileId][speciesId][process] = {}
                    categoryDict[fileId][speciesId][process]['category_id'] = category_id
                    categoryDict[fileId][speciesId][process]['name'] = name
                    categoryDict[fileId][speciesId][process]['sub_group_name'] = sub_group_name
        
    else:
        #DON'T WANT THE EXTRA ROWS
        continue    
        
    
        
categoryCount = 0  
for fileKey in categoryDict.keys():
    for speciesKey in categoryDict[fileKey].keys():
        for process in categoryDict[fileKey][speciesKey].keys():
            categoryCount += 1
        

print("\nDONE PROCESSING CATEGORY ID FILE...")
print("TOTAL CATEGORY ID COUNT", categoryCount, "\n")