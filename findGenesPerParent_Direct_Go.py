from datetime import date
import re
import subprocess

today = date.today()
date_str = today.strftime("%Y-%m-%d")
outputFile = f"output/{date_str}_Direct_GO_genesPerParent_w_count.tsv"


def outToNewVersion2GoRelationshipFile(lineToPrint):
    global outputFile
    with open(outputFile, 'a') as outfile:
        outfile.write(lineToPrint)
        #print(lineToPrint)


def main():
    global outputFile
    from parseCorrectSpecies_wo_NOT import correctSpeciesDict
    progress = 0
    inputFile = f"output/{date_str}_GO_Tree.tsv"
    totalLines = int(subprocess.getoutput(f"wc -l {inputFile}").strip().split()[0])
    
    with open(outputFile, 'w') as outfile:
        outfile.write("PARENT_GO_ID\tPARENT_NAMESPACE\tPARENT_NAME\tCHILDREN_COUNT\tCHILDREN_LIST\tTAX_ID\tGENE_COUNT\n")
    
    
    with open(inputFile, 'r') as firstFile:
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
            
            
            if parent_term in correctSpeciesDict.keys():
                for tax_id in correctSpeciesDict[parent_term]:
                    tax_id = tax_id.strip()
                    for gene_id in correctSpeciesDict[parent_term][tax_id.strip()].keys():
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
                    line_to_print = line + "\t" + str(tax_id) + "\t" + str(geneCount) + "\n"
                    #print(line_to_print)
                    outToNewVersion2GoRelationshipFile(line_to_print)
            
            
            progress = progress + 1
            totalProgress = round(progress / totalLines * 100, 2)
            print(f"\r{totalProgress}%", end="", flush=True)
            


if __name__ == "__main__":
    main()