import re
import subprocess
import os
import pandas as pd
import ast


def assembleGeneInfo(inputFile, speciesinfoDict, outputFile):
    speciesGenomeDict = {}
    finalMappingDict = {}
    
    with open(outputFile, 'w') as outfile:
        outfile.write("Tax_ID\tGeneID\tSymbol\tChromosome\tSpecies_Specific_ID\tSpecies_Specific_ID_Type\tBase_dbXrefs\n")
    
    
    
    
    progress = 0
    totalLines = int(subprocess.getoutput(f"wc -l {inputFile}").strip().split()[0])
    '''
    with open(inputFile, 'r') as infile, open(outputFile, 'a') as outfile:
        for line in infile:
            line = line.strip()
            progress += 1
            if progress % 10000 == 0:
                print(f"\r{round(progress / totalLines * 100, 2)}%", end="", flush=True)
            if line.startswith('#') or "NEWENTRY" in line or len(line) == 0:
                continue
            
            
            lineArray = line.split('\t')
            lineArray = [str(x).strip() for x in lineArray]
            taxId = lineArray[0]
            if taxId not in speciesInfoDict.keys():
                continue
            
            tax_final = speciesInfoDict[taxId]['actualSpeciesId']
            xdb = speciesInfoDict[taxId]['speciesSpecificIdType']
            
            geneId = lineArray[1]
            symbol = lineArray[2]
            locusTag = lineArray[3]
            synonyms = lineArray[4]
            dbxrefs = lineArray[5]
            chrom = lineArray[6]
            map_location = lineArray[7]
            desc = lineArray[8]
            type_of_gene = lineArray[9]
            symbol_from_nom = lineArray[10]
            full_name_from_nom = lineArray[11]
            nom_status = lineArray[12]
            other_desig = lineArray[13]
            modification_date = lineArray[14]
            feature_type = lineArray[15]
            
            
            if geneId != "-" and tax_final:
                xbdId = "-"
                xbd_final = "-"
                
                if type_of_gene == "protein-coding":
                    if tax_final not in speciesGenomeDict.keys():
                        speciesGenomeDict[tax_final] = {}
                        speciesGenomeDict[tax_final]['genome_gene_count'] = 1
                    else:
                        speciesGenomeDict[tax_final]['genome_gene_count'] += 1
                
                if dbxrefs != "-":
                    tmp1 = ""
                    tmp2 = ""
                    dbxrefs_split = dbxrefs.split('|')
                    dbxrefs_split = [str(x).strip() for x in dbxrefs_split]
                    for ref_split in dbxrefs_split:
                        new_split = ref_split.split(':')
                        new_split = [str(x).strip() for x in new_split]
                        if new_split[0].lower() == xdb:
                            xbdId = new_split[1]
                            xbd_final = xbd
                    
                outfile.write(f"{geneId}\t{tax_final}\t{symbol}\t{desc}\t{locusTag}\t{xbdId}\t{xbd_final}\t{chrom}\t{map_location}\t{type_of_gene}\n")
            
            
    '''
    actual_species_ids = [str(key).strip() for key in speciesinfoDict.keys()]
    actual_species_ids_string = [f"^{val}" for val in actual_species_ids]
    actual_species_ids_string.append("^#tax_id")
    
    actual_species_ids_string = "|".join(actual_species_ids_string)
    
    
    cmd = f"""egrep -w "{actual_species_ids_string}" {inputFile} > {inputFile}_formatted"""
    subprocess.getoutput(cmd)
    
    final_mapping_dict = {str(speciesinfoDict[key]['actualSpeciesId']).strip(): str(speciesinfoDict[key]['speciesSpecificIdType']).strip() for key in speciesinfoDict.keys()}
    
    df = pd.read_csv(f"{inputFile}_formatted", sep="\t")
    with open(outputFile, 'w') as outfile:
        for row in df.to_dict(orient="records"):
            symbol = None
            geneid = None
            chromosome = None
            dbXrefs = None
            species_specific_id = "-"
            species_specific_id_type = "-"
            
            
            
            actual_tax_id = speciesinfoDict[str(row['#tax_id']).strip()]['actualSpeciesId']
            if str(row['Symbol']).strip().lower() == "newentry":
                continue
            row['GeneID'] = str(row['GeneID']).strip()
            
            if row["type_of_gene"] == "protein-coding":
                if actual_tax_id not in speciesGenomeDict.keys():
                    speciesGenomeDict[actual_tax_id] = {}
                    speciesGenomeDict[actual_tax_id]['genome_gene_count'] = 1
                else:
                    speciesGenomeDict[actual_tax_id]['genome_gene_count'] += 1
            
            if row['dbXrefs'] != "-":
                specific_type_from_dict = final_mapping_dict[actual_tax_id]
                for xrefs_info in row['dbXrefs'].strip().split('|'):
                    new_split = xrefs_info.split(':')
                    xrefs_type = new_split[0]
                    if new_split[0].strip() == specific_type_from_dict:
                        species_specific_id = new_split[-1]
                        species_specific_id_type = specific_type_from_dict
                dbXrefs = row['dbXrefs'] 
                
                
            outfile.write(f"{actual_tax_id}\t{row['GeneID']}\t{str(row['Symbol']).strip()}\t{row['chromosome']}\t{species_specific_id}\t{species_specific_id_type}\t{row['dbXrefs'].strip()}\n")
            
            if row['GeneID'] not in finalMappingDict.keys():
                finalMappingDict[row['GeneID']] = {}
                finalMappingDict[row['GeneID']]['symbol'] = str(row['Symbol']).strip()
                finalMappingDict[row['GeneID']]['species_specific_id'] = species_specific_id
                finalMappingDict[row['GeneID']]['species_specific_id_type'] = species_specific_id_type
                finalMappingDict[row['GeneID']]['chromosome'] = row['chromosome']
        
    
        
    return speciesGenomeDict, finalMappingDict

def main(arguments):
    invalid = False
    speciesGenomeDict = None
    finalMappingDict = None
    arguments = [str(x).strip() for x in arguments]
    
    if len(arguments) == 4:
        mapping_file = arguments[0]
        ncbi_gene_inputfile = arguments[1]
        speciesInfoDict = arguments[2]
        outputFile = arguments[3]
    else:
        print("Arguments are wrong")
        exit()
    
    
    if speciesInfoDict:
        speciesInfoDict = ast.literal_eval(speciesInfoDict)
    if mapping_file.lower() == "gene_information" or mapping_file.lower() == "assemblegeneinfo":
        
        speciesGenomeDict, finalMappingDict = assembleGeneInfo(ncbi_gene_inputfile, speciesInfoDict, outputFile)
    
    
    
    return speciesGenomeDict, finalMappingDict
    
    
    
    
    
    



if __name__ == "__main__":
    main(arguments)