from datetime import date
import re
import subprocess

today = date.today()
date_str = today.strftime("%Y-%m-%d")


#THIS IS THE FILE FOR DIRECT
#with open('./newest_go_relationship_07_11_25_final.tsv', 'r') as firstfile:
#this is the file for creating all other genesets
#with open('./output/version2_GO_Relationships_w_gene_count_08_05.tsv', 'r') as firstfile: #for gene count
#PARENT GO ID	PARENT NAMESPACE	PARENT NAME	CHILDREN AMOUNT	CHILDREN LIST

def main():
    from formatCorrectSpeciesGene2Go import correctSpeciesDict
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    progress = 0
    uniqueSet = set()
    inputFile = f"output/{date_str}_Direct_GO_genesPerParent_w_count.tsv"
    totalLines = int(subprocess.getoutput(f"wc -l {inputFile}").strip().split()[0])
    outputFile = f"output/{date_str}_merge_direct_GO.tsv"
    with open(inputFile, 'r') as firstfile, open(outputFile, 'w') as outFile:
        outFile.write("PARENT TERM\tPARENT PROCESS NAME\tPARENT'S CHILDREN COUNT\tPARENT NAMESPACE\tSPECIES ID\tGENE ID\tEVIDENCE\tCHILD GO TERM\n")
        for line in firstfile:
            line = line.strip()
            lineArray = line.split('\t')
            
            goTerm = lineArray[0].strip()
            goTermNamespace = lineArray[1].strip()
            goTermProcessName = lineArray[2].strip()
            goTermChildrenCount = lineArray[3].strip()
            goTermChildrenArray = lineArray[4].strip().split(';')
            goTermChildrenCount = len(goTermChildrenArray) if goTermChildrenCount != len(goTermChildrenArray) else goTermChildrenCount
            speciesID = lineArray[5].strip()
            
            
            informationDict = {}
            if speciesID in correctSpeciesDict.keys():
                for go_id in correctSpeciesDict[speciesID].keys():
                    go_id = go_id.strip()
                    if go_id == goTerm:
                        for gene_id in correctSpeciesDict[speciesID][go_id].keys():
                            gene_id = gene_id.strip()
                            if speciesID not in informationDict.keys():
                                informationDict[speciesID] = {}
                                informationDict[speciesID][gene_id] = []
                                informationDict[speciesID][gene_id].extend(correctSpeciesDict[speciesID][go_id][gene_id]['evidence_codes'])
                            else:
                                if gene_id not in informationDict[speciesID].keys():
                                    informationDict[speciesID][gene_id] = []
                                    informationDict[speciesID][gene_id].extend(correctSpeciesDict[speciesID][go_id][gene_id]['evidence_codes'])
                                else:
                                    informationDict[speciesID][gene_id].extend(correctSpeciesDict[speciesID][go_id][gene_id]['evidence_codes'])
            
            
            
            
            
            for taxID in informationDict.keys():
                for geneID in informationDict[taxID].keys():
                    infoForFinalFile = f"{goTerm}\t{goTermProcessName}\t{goTermChildrenCount}\t{goTermNamespace}\t{taxID}\t{geneID}\t{';'.join(set(informationDict[taxID][geneID]))}\n"
                    outFile.write(infoForFinalFile)
            
            progress = progress + 1
            if progress % 100 == 0:
                totalProgress = round(progress / totalLines * 100, 2)
                print(f"\r{totalProgress}%", end="")
        
                                

if __name__ == "__main__":
    main()