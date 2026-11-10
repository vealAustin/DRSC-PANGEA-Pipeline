"""
FOR VERSION 2
"""


from datetime import date
import re
import subprocess
import os
import time

today = date.today()
date_str = today.strftime("%Y-%m-%d")
correctSpeciesDict = {}


start = False


def outToNewVersion2GoRelationshipFile(lineToPrint, outputFile):
    with open(outputFile, 'a') as outfile:
        outfile.write(lineToPrint)
        



            
            
"""
def interProcessGene2Go(inputFile):
    correct_species_file = f"output/{date_str}_gene2go_processed"
    correctSpeciesDict = {}
    notGoTerms = set()
    tax_id_list = set()
    
    allLines = None
    mappingDict = None
    if inputFile:
        with open(inputFile, 'r') as infile:
            allLines = infile.read()
        from processFlyBaseMappings import mapping_dict as mappingDict
    else:
        with open(correct_species_file, 'r') as infile:
            allLines = infile.read()
    
    
    for line in allLines.split('\n'):
        line = line.strip()
        
        
        if line.startswith('!'):
            continue
        
        #['FB', 'FBgn0043467', '064Ya', 'involved_in', 'GO:0048149', 'PMID:11086999', 'IMP', '', 'P', '064Ya', '', 'gene_product', 'taxon:7227', '20060803', 'FlyBase']
        
        tax_id = None
        gene_id = None
        go_id = None
        evidence = None
        col_4 = None
        lineArray = line.split('\t')
        if not lineArray[0]:
            continue
        
        if inputFile:
            try:
                lineArray = [str(x).strip() for x in lineArray]
                tax_id = "7227"
                gene_id = mappingDict[lineArray[1]]['gene_id']
                go_id = lineArray[4].strip()
                evidence = lineArray[6].strip()
                col_4 = lineArray[3].strip()
            except KeyError as e:
                print(e)
                outToNonMappedFBgns(lineArray[1])
                continue
        else:
            
            tax_id = lineArray[0].strip()
            gene_id = lineArray[1].strip()
            go_id = lineArray[2].strip()
            evidence = lineArray[3].strip()
            col_4 = lineArray[4].strip()

        
        try:
            if 'not' in col_4.lower():
                notGoTerms.add(go_id)
                continue
        except AttributeError as e:
            print(e)
            print("LINE ARRAY [3]", lineArray[3])
            print("LINE ARRAY:", lineArray)
            print("COL 4:", col_4)
            exit()
            
        if go_id not in correctSpeciesDict.keys():
            tax_id_list.add(tax_id)
            correctSpeciesDict[go_id] = {}
            correctSpeciesDict[go_id][tax_id] = {}
            correctSpeciesDict[go_id][tax_id][gene_id] = []
            correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
        else:
            if tax_id not in correctSpeciesDict[go_id].keys():
                tax_id_list.add(tax_id)
                correctSpeciesDict[go_id][tax_id] = {}
                correctSpeciesDict[go_id][tax_id][gene_id] = []
                correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
            else:
                if gene_id not in correctSpeciesDict[go_id][tax_id].keys():
                    correctSpeciesDict[go_id][tax_id][gene_id] = []
                    correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
                else:
                    correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
    
    return correctSpeciesDict, tax_id_list


def interProcessGene2Go(inputFile):
    correct_species_file = f"output/{date_str}_gene2go_processed"
    correctSpeciesDict = {}
    notGoTerms = set()
    tax_id_list = set()
    
    allLines = None
    mappingDict = None
    
    with open(correct_species_file, 'r') as infile:
        for line in infile:
            line = line.strip()
            
            if line.startswith('!'):
                continue
            
            lineArray = line.split('\t')
            
            if not lineArray[0]:
                continue
            
            tax_id = lineArray[0].strip()
            gene_id = lineArray[1].strip()
            go_id = lineArray[2].strip()
            evidence = lineArray[3].strip()
            col_4 = lineArray[4].strip()
            
            
            
            if inputFile:
                if tax_id == "7227":
                    continue
                
            
            try:
                if 'not' in col_4.lower():
                    notGoTerms.add(go_id)
                    continue
            except AttributeError as e:
                print(e)
                print("LINE ARRAY [3]", lineArray[3])
                print("LINE ARRAY:", lineArray)
                print("COL 4:", col_4)
                exit()
                
            if go_id not in correctSpeciesDict.keys():
                tax_id_list.add(tax_id)
                correctSpeciesDict[go_id] = {}
                correctSpeciesDict[go_id][tax_id] = {}
                correctSpeciesDict[go_id][tax_id][gene_id] = []
                correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
            else:
                if tax_id not in correctSpeciesDict[go_id].keys():
                    tax_id_list.add(tax_id)
                    correctSpeciesDict[go_id][tax_id] = {}
                    correctSpeciesDict[go_id][tax_id][gene_id] = []
                    correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
                else:
                    if gene_id not in correctSpeciesDict[go_id][tax_id].keys():
                        correctSpeciesDict[go_id][tax_id][gene_id] = []
                        correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
                    else:
                        correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
        
        
    if inputFile:
        from processFlyBaseMappings import mapping_dict as mappingDict
        with open(inputFile, 'r') as infile:
            for line in infile:
                line = line.strip()
                if line.startswith('!'):
                    continue
                lineArray = line.split('\t')
                lineArray = [str(x).strip() for x in lineArray]
                
                if not lineArray[0]:
                    continue
                
                try:
                    tax_id = "7227"
                    gene_id = mappingDict[lineArray[1]]['gene_id']
                    go_id = lineArray[4].strip()
                    evidence = lineArray[6].strip()
                    col_4 = lineArray[3].strip()
                except KeyError as e:
                    outToNonMappedFBgns(lineArray[1])
                    continue
                
                try:
                    if 'not' in col_4.lower():
                        notGoTerms.add(go_id)
                        continue
                except AttributeError as e:
                    print(e)
                    print("LINE ARRAY [3]", lineArray[3])
                    print("LINE ARRAY:", lineArray)
                    print("COL 4:", col_4)
                    exit()
                    
                if go_id not in correctSpeciesDict.keys():
                    tax_id_list.add(tax_id)
                    correctSpeciesDict[go_id] = {}
                    correctSpeciesDict[go_id][tax_id] = {}
                    correctSpeciesDict[go_id][tax_id][gene_id] = []
                    correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
                else:
                    if tax_id not in correctSpeciesDict[go_id].keys():
                        tax_id_list.add(tax_id)
                        correctSpeciesDict[go_id][tax_id] = {}
                        correctSpeciesDict[go_id][tax_id][gene_id] = []
                        correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
                    else:
                        if gene_id not in correctSpeciesDict[go_id][tax_id].keys():
                            correctSpeciesDict[go_id][tax_id][gene_id] = []
                            correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
                        else:
                            correctSpeciesDict[go_id][tax_id][gene_id].append(evidence)
            
    
    return correctSpeciesDict, tax_id_list

"""

def getGenesPerParent():
    from parseCorrectSpecies_wo_NOT import correctSpeciesDict
    progress = 0
    
    
    outputFile = f"output/{date_str}_GO_Tree_W_Gene_Count.tsv"
    inputFile = f"output/{date_str}_GO_Tree.tsv"
    #inputFile = "input/version2_GORelationships_08_18_ACTUAL_INFO.tsv"
    #outputFile = "output/FINAL_OLD_genesPerGo.tsv"
    
    
    
    with open(outputFile, 'w') as outfile:
        outfile.write("PARENT_GO_ID\tPARENT_NAMESPACE\tPARENT_NAME\tCHILDREN_COUNT\tCHILDREN_LIST\tTAX_ID\tGENE_COUNT\tGENE_LIST\n")
        
    
    with open(inputFile, 'r') as firstFile:
        totalLines = int(subprocess.getoutput(f"wc -l {inputFile}").strip().split()[0].strip())
        for line in firstFile:
            line = line.strip()
            lineArray = line.split('\t')
                
            parent_term = lineArray[0].strip()
            parent_name_space = lineArray[1].strip()
            parent_name = lineArray[2].strip()
            children_amount = lineArray[3].strip()
            childrenList = lineArray[4].strip().split(';')
            geneCount = 0
            taxGeneCount = 0
            uniqueGeneSet = set()
            speciesGeneSet = set()
            noOutput = False
            taxGeneDict = {}
            
            for child in childrenList:
                child = child.strip()
                if child in correctSpeciesDict.keys():
                    for tax_id in correctSpeciesDict[child.strip()].keys():
                        for gene_id in correctSpeciesDict[child.strip()][tax_id.strip()].keys():
                            tax_id = tax_id.strip()
                            gene_id = gene_id.strip()
                            masterString = tax_id + "|" + gene_id
                            if tax_id not in taxGeneDict.keys():
                                taxGeneDict[tax_id] = set()
                                taxGeneDict[tax_id].add(gene_id.strip())
                            else:
                                taxGeneDict[tax_id].add(gene_id.strip())
                            
                    
                        
            for tax_id in taxGeneDict.keys():
                geneCount = len(taxGeneDict[tax_id])
                if geneCount < 5000:
                    line_to_print = line + "\t" + str(tax_id) + "\t" + str(len(taxGeneDict[tax_id])) + "\t" + str(";".join(taxGeneDict[tax_id])) + "\n"
                    outToNewVersion2GoRelationshipFile(line_to_print, outputFile)
            
            
            progress = progress + 1
            totalProgress = round(progress / totalLines * 100, 2)
            print(f"\r{totalProgress}%", end="", flush=True)
            
            

if __name__ == "__main__":
    getGenesPerParent()