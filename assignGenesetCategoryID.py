#fileDict = {'./output/non_go_info.tsv': 'non_go'}
#fileDict = {'./output/high_throughput_w_tick_08_28_v2.tsv': 'high_throughput', './output/go_slim_1_all.tsv': 'go_slim_1', './output/go_slim_2_all.tsv': 'go_slim_2',
#    '../output/merge_Direct_GO.tsv': 'merge_Direct_GO', '../output/merge_version2_all_species_08_25_sbatch.tsv': 'flattened'}


#TO GET THE NON GO DATA FOR UPLOADING LATER

def getSpeciesSpecificID(gene_id, finalMappingDict):
    if gene_id in finalMappingDict.keys():
        return finalMappingDict[gene_id]['species_specific_id'], finalMappingDict[gene_id]['species_specific_id_type']
    else:
        return "-", "-"


def main(finalMappingDict, SpeciesSynonymMappingDict):
    genesetInfo = set()
    from processCategoryIDInfo import categoryDict
    import subprocess
    
    #SHOULD ADJUST THIS SO THAT ITS ACTUALLY CORRECT
    #from process_gene_info_table import geneInfoDict
    import re
    from format_GO_info import goInfoDict
    import time
    from datetime import date
    from processFlyBaseMappings import reverse_mapping_dict
    
    
    totalYeastDirectCount = 0
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    noRemapCount = 0
    remappedCount = 0
    
    outputGenesetFile = f"output/{date_str}_geneset_file.tsv"
    outputGensetCategoriesFile = f"output/{date_str}_categories.tsv"
    gene2genesetAllSpeciesFile = f"output/{date_str}_gene2geneset_all_species.tsv"
    notMappedFile = f"output/{date_str}_not_mapped.tsv"
    
    fileDict = {f'output/{date_str}_experimental_file.tsv': "experimental_file", f"output/{date_str}_high_throughput.tsv": 'high_throughput', f"output/{date_str}_go_slim_1_other.tsv": "go_slim_1", f"output/{date_str}_go_slim_2_other.tsv": "go_slim_2",
        f"output/{date_str}_merge_direct_GO.tsv": "merge_Direct_GO", f"output/{date_str}_Merge_File.tsv": "flattened", f"output/{date_str}_go_slim_1_fly.tsv": "go_slim_1", f"output/{date_str}_go_slim_2_fly.tsv": "go_slim_2"}

    #fileDict = {f"output/{date_str}_merge_direct_GO.tsv": "merge_Direct_GO"}

    print("Getting non go info to upload later...")
    #subprocess.getoutput(f"""mysql devflyrnai -e "SELECT * FROM ET_Gene_2_Geneset_All_Species WHERE gene_set_id not like '%GO%';" --batch > output/{date_str}_non_go_info.tsv""")
    print("Done.")
    
    for file in fileDict.keys():
        print(file, "\n")
        progress = 0
        totalLines = int(subprocess.getoutput(f"wc -l {file}").split()[0].strip())
        time.sleep(2)
        with open(file, 'r') as infile, open(outputGenesetFile, 'a') as geneset_file, open(gene2genesetAllSpeciesFile, 'a') as gene2geneset_file, open(notMappedFile, 'a') as not_mapped_file:
            gene2geneset_file.write("SPECIES_SPECIFIC_ID\tSPECIFIC_ID_TYPE\tSPECIES_ID\tSYMBOL\tGENE_ID\tGO_ID\tGO_NAME\tGO_PROCESS\tEVIDENCE\tGENESET_CATEGORY_ID\n")
            geneset_file.write("GENESET_CATEGORY_ID\tGO_ID\tGO_NAME\n")
            for line in infile:
                line = line.strip()
                lineArray = line.split('\t')
                if lineArray[0].strip().startswith("GO"):
                    
                    
                    
                    if progress < 10:
                        print(lineArray)
                        
                    
                    
                    go_id = lineArray[0].strip()
                    go_name = lineArray[1].strip()
                    go_term_children_count = lineArray[2].strip()
                    go_process = lineArray[3].strip()
                    tax_id = lineArray[4].strip()
                    gene_id = lineArray[5].strip()
                    evidence_codes = lineArray[6].strip()
                    species_specific_id = "-"
                    species_specific_id_type = "-"
                    symbol = "-"
                    
                    tax_id = SpeciesSynonymMappingDict[tax_id]
                    
                    
                    
                    species_specific_id, species_specific_id_type = getSpeciesSpecificID(gene_id, finalMappingDict)
                    
                    
                    if str(tax_id).strip() == "7227" and species_specific_id == "-":
                        species_specific_id = reverse_mapping_dict[gene_id]['fbgn']
                        species_specific_id_type = "FlyBase"
                    
                    if gene_id in finalMappingDict.keys():
                        symbol = finalMappingDict[gene_id]['symbol']
                    elif gene_id in reverse_mapping_dict.keys():
                        symbol = reverse_mapping_dict[gene_id]['symbol']
                    
                    try:
                        gene_set_category_id = str(categoryDict[fileDict[file]][tax_id][lineArray[3]]['category_id'])
                    except KeyError as e:
                        print(e)
                        print("fileDict.keys():", fileDict.keys())
                        print("categoryDict keys:", categoryDict.keys())
                        print("Category w file keys:", categoryDict[fileDict[file]].keys())
                        print("LINE ARRAY:", lineArray)
                        print("Third category dict keys:", categoryDict[fileDict[file]][tax_id].keys())
                        #print("Fourth category dict:", categoryDict[fileDict[file]][lineArray[-3]][lineArray[3]])
                        
                        exit()
                    
                    
                    if str(gene_set_category_id).strip() in ('255', '256', '257') and fileDict[file] == "merge_Direct_GO":
                        totalYeastDirectCount += 1
                    
                    
                    currentGenesetInfo = f"{gene_set_category_id}|{go_id}|{goInfoDict[go_id]}"
                    if currentGenesetInfo not in genesetInfo:
                        geneset_file.write(f"{gene_set_category_id}\t{go_id}\t{goInfoDict[go_id]}\n")
                        genesetInfo.add(currentGenesetInfo)
                    
                    
                    gene2geneset_file.write(f"{species_specific_id}\t{species_specific_id_type}\t{tax_id}\t{symbol}\t{gene_id}\t{go_id}\t{go_name}\t{go_process}\t{evidence_codes}\t{gene_set_category_id}\n")
                    
                    '''
                    if gene_id in geneInfoDict[tax_id].keys():
                        gene2geneset_file.write(f"{species_specific_id}\t{species_specific_id_type}\t{geneInfoDict[tax_id][gene_id]['symbol']}\t{gene_id}\t{go_id}\t{evidence_codes}\t{gene_set_category_id}\n")
                    else:
                        noRemapCount += 1
                        print("GENE ID:", gene_id)
                        print("TAX ID:", tax_id)
                        print("GENE_ID NOT IN GENEINFODICT")
                        #exit(1)
                        not_mapped_file.write(f"{gene_id}\t{go_id}\t{evidence_codes}\t{gene_set_category_id}\n")
                    '''  
                elif re.match(r"^[0-9]+$", str(lineArray[0]).strip()):
                    lineArray = [str(x).strip() for x in lineArray]
                    
                    print("JUST A NUMBER AT THE BEGINNING:", lineArray)
                    exit()
                    
                    gene2geneset_file.write(f"{lineArray[1]}\t{lineArray[2]}\t{lineArray[3]}\t{lineArray[4]}\t{lineArray[5]}\t{lineArray[6]}\n")
                    
                    
                    
                
                progress += 1
                totalProgress = round(progress / totalLines * 100, 2)
                print(f"\r{totalProgress}%", end="")
    
    
    print("AMOUNT OF RECORDS THAT WERE ABLE TO BE REMAPPED", remappedCount)
    print("AMOUNT OF RECORDS THAT WERE NOT ABLE TO BE MAPPED", noRemapCount)
    
    print("TOTAL YEAST DIRECT COUNT:", totalYeastDirectCount)
    
    


if __name__ == "__main__":
    main(finalMappingDict, SpeciesSynonymMappingDict)