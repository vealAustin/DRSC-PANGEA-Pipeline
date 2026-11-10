from datetime import date

today = date.today()
date_str = today.strftime("%Y-%m-%d")

geneInfoDict = {}

uniqueSet = set()

with open(f'./input/{date_str}_Gene_Information.tsv', encoding='latin1') as infile:
    for line in infile:
        line = line.strip()
        lineArray = line.split('\t')
        lineArray = [str(x).strip() for x in lineArray]
        gene_id = str(lineArray[0]).strip()
        species_id = str(lineArray[1]).strip()
        symbol = lineArray[2].strip()
        name = lineArray[3].strip()
        cg = lineArray[4].strip()
        species_specific_gene_id = lineArray[5].strip()
        species_specific_gene_id_type = lineArray[6].strip()
        
        
        if species_id not in geneInfoDict.keys():
            geneInfoDict[species_id] = {}
            geneInfoDict[species_id][gene_id] = {}
            geneInfoDict[species_id][gene_id]['symbol'] = symbol
            geneInfoDict[species_id][gene_id]['name'] = name
            geneInfoDict[species_id][gene_id]['cg'] = cg
            geneInfoDict[species_id][gene_id]['species_specific_gene_id'] = species_specific_gene_id
            geneInfoDict[species_id][gene_id]['species_specific_gene_id_type'] = species_specific_gene_id_type
        
        else:
            if gene_id not in geneInfoDict[species_id].keys():
                geneInfoDict[species_id][gene_id] = {}
                geneInfoDict[species_id][gene_id]['symbol'] = symbol
                geneInfoDict[species_id][gene_id]['name'] = name
                geneInfoDict[species_id][gene_id]['cg'] = cg
                geneInfoDict[species_id][gene_id]['species_specific_gene_id'] = species_specific_gene_id
                geneInfoDict[species_id][gene_id]['species_specific_gene_id_type'] = species_specific_gene_id_type
            else:
                print("ALREADY A RECORD IN THE DICT AT THE CURRENT INFO", species_id, gene_id)
                print("INFO THAT ALREADY IN THE DICT", geneInfoDict[species_id][gene_id])
                print("NEW INFORMATION", lineArray)
                print("\n")
                exit()
        