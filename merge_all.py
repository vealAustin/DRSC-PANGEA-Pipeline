#from formatCorrectSpeciesGene2Go import correctSpeciesDict
import subprocess
from datetime import date
import re

today = date.today()
date_str = today.strftime("%Y-%m-%d")



#totalLines = 118128

outputFile = f"./output/{date_str}_Merge_File.tsv"

#inputFile = "output/2026-09-15_GO_Tree_W_Gene_Count.tsv"





def outToMasterFile(print_line):
    global outputFile
    with open(outputFile, 'a') as outFile2:
        outFile2.write(print_line)

#THIS IS THE FILE FOR DIRECT
#with open('./newest_go_relationship_07_11_25_final.tsv', 'r') as firstfile:
#this is the file for creating all other genesets
#with open('./output/version2_GO_Relationships_w_gene_count_08_05.tsv', 'r') as firstfile: #for gene count
#PARENT GO ID	PARENT NAMESPACE	PARENT NAME	CHILDREN AMOUNT	CHILDREN LIST
def main(SpeciesSynonymMappingDict):
    from parseCorrectSpecies_wo_NOT_v2 import correctSpeciesDict
    global date_str
    experimentalOnlyIncludeList = ['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'HTP', 'HDA', 'HMP', 'HGI', 'HEP']
    includeHighThroughputList = ['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'IBA', 'IBD', 'IRD', 'IKR', 'ISS', 'ISO', 'ISA', 'ISM', 'IGC', 'TAS', 'NAS', 'IC']
    uniqueSet = set()
    
    inputFile = f"output/{date_str}_GO_Tree_W_Gene_Count.tsv"
    totalLines = int(subprocess.getoutput(f"wc -l {inputFile}").strip().split()[0])
    
    progress = 0
    
    with open(outputFile, 'w') as outFile:
        outFile.write("PARENT TERM\tPARENT PROCESS NAME\tPARENT'S CHILDREN COUNT\tPARENT NAMESPACE\tSPECIES ID\tGENE ID\tEVIDENCE\tCHILD GO TERM\n")
    
    with open(inputFile, 'r') as firstfile:
        for line in firstfile:
            line = line.strip()
            lineArray = line.split('\t')
            
            goTerm = lineArray[0].strip()
            goTermNamespace = lineArray[1].strip()
            goTermProcessName = lineArray[2].strip()
            goTermChildrenCount = lineArray[3].strip()
            goTermChildrenArray = lineArray[4].strip().split(';')
            currentTaxID = lineArray[5].strip()
            
    
            
            childInformationDict = {}
            for child in goTermChildrenArray:
                child = child.strip()
                #for tax_id in correctSpeciesDict.keys():
                if currentTaxID in correctSpeciesDict.keys():
                    tax_id = currentTaxID
                    for go_id in correctSpeciesDict[tax_id].keys():
                        go_id = go_id.strip()
                        if go_id == child:
                            
                            for gene_id in correctSpeciesDict[tax_id][go_id].keys():
                                if tax_id not in childInformationDict.keys():
                                    childInformationDict[tax_id] = {}
                                    childInformationDict[tax_id][gene_id] = []
                                    childInformationDict[tax_id][gene_id].extend(correctSpeciesDict[tax_id][go_id][gene_id])
                                else:
                                    if gene_id not in childInformationDict[tax_id].keys():
                                        childInformationDict[tax_id][gene_id] = []
                                        childInformationDict[tax_id][gene_id].extend(correctSpeciesDict[tax_id][go_id][gene_id])
                                    else:
                                        childInformationDict[tax_id][gene_id].extend(correctSpeciesDict[tax_id][go_id][gene_id])
            
            
            for taxID in childInformationDict.keys():
                for geneID in childInformationDict[taxID].keys():
                    actualTaxID = None
                    if taxID in SpeciesSynonymMappingDict.keys():
                        if taxID != SpeciesSynonymMappingDict[taxID]:
                            actualTaxID = SpeciesSynonymMappingDict[taxID]
                        else:
                            actualTaxID = taxID
                            
                    infoForFinalFile = f"{goTerm}\t{goTermProcessName}\t{goTermChildrenCount}\t{goTermNamespace}\t{actualTaxID}\t{geneID}\t{';'.join(set(childInformationDict[taxID][geneID]))}\n"
                    codesSplit = infoForFinalFile.split('\t')[1].strip().split(';')
                    
                    
                    outToMasterFile(infoForFinalFile)
            
            progress = progress + 1
            if progress % 100 == 0:
                totalProgress = round(progress / totalLines * 100, 2)
                print(f"\r{totalProgress}%", end="")
                                
        

if __name__ == "__main__":
    main(SpeciesSynonymMappingDict)