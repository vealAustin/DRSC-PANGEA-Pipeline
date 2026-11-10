from datetime import date
import re

today = date.today()
date_str = today.strftime("%Y-%m-%d")
correctSpeciesDict = {}
notGoTerms = set()



def outToNonMappedFBgns(fbgn):
    with open(f"output/Not_Mapped_FBgns_{date_str}.txt", 'a') as outfile:
        outfile.write(fbgn + "\n")


print("PARSING CORRECT SPECIES GENE 2 GO FILE...")
##tax_id	GeneID	GO_ID	Evidence	Qualifier	GO_term	PubMed	Category
#with open('./output/correctSpeciesGene2Go_FINAL.tsv', 'r') as infile:
#with open('./output/new_correct_species.tsv', 'r') as infile:
correct_species_file = f"output/{date_str}_gene2go_processed"
print("GENE 2 GO FILE NAME:", correct_species_file)

"""
def getGenesPerParent(inputFile):
if inputFile:
    with open(inputFile, 'r') as infile:
else:
"""
with open(correct_species_file, 'r') as infile:
    mappingDict = None
    imported = False
    for line in infile:
        line = line.strip()
        lineArray = line.split('\t')
        
        if len(lineArray) == 8:
            tax_id = lineArray[0].strip()
            gene_id = lineArray[1].strip()
            go_id = lineArray[2].strip()
            evidence = lineArray[3].strip()
            col_4 = lineArray[4].strip()
        else:
            if not imported:
                from processFlyBaseMappings import mapping_dict as mappingDict
                imported = True
        
            try:
                tax_id = "7227"
                gene_id = mappingDict[lineArray[1]]['gene_id']
                go_id = lineArray[4].strip()
                evidence = lineArray[6].strip()
                col_4 = lineArray[3].strip()
            except KeyError as e:
                outToNonMappedFBgns(lineArray[1])
                continue
        
        if not lineArray[0]:
            continue
        
        if 'NOT' in col_4:
            notGoTerms.add(go_id)
            continue
        
        if tax_id not in correctSpeciesDict.keys():
            correctSpeciesDict[tax_id] = {}
            correctSpeciesDict[tax_id][go_id] = {}
            correctSpeciesDict[tax_id][go_id][gene_id] = {}
            correctSpeciesDict[tax_id][go_id][gene_id]['evidence_codes'] = []
            correctSpeciesDict[tax_id][go_id][gene_id]['evidence_codes'].append(evidence)
        else:
            if go_id not in correctSpeciesDict[tax_id].keys():
                correctSpeciesDict[tax_id][go_id] = {}
                correctSpeciesDict[tax_id][go_id][gene_id] = {}
                correctSpeciesDict[tax_id][go_id][gene_id]['evidence_codes'] = []
                correctSpeciesDict[tax_id][go_id][gene_id]['evidence_codes'].append(evidence)
            else:
                if gene_id not in correctSpeciesDict[tax_id][go_id].keys():
                    correctSpeciesDict[tax_id][go_id][gene_id] = {}
                    correctSpeciesDict[tax_id][go_id][gene_id]['evidence_codes'] = []
                    correctSpeciesDict[tax_id][go_id][gene_id]['evidence_codes'].append(evidence)
                else:
                    if "evidence_codes" not in correctSpeciesDict[tax_id][go_id][gene_id].keys():
                        correctSpeciesDict[tax_id][go_id][gene_id]['evidence_codes'] = []
                        correctSpeciesDict[tax_id][go_id][gene_id]['evidence_codes'].append(evidence)
                    else:
                        correctSpeciesDict[tax_id][go_id][gene_id]['evidence_codes'].append(evidence)
    
print("DONE PARSING CORRECT SPECIES GENE 2 GO FILE...")
