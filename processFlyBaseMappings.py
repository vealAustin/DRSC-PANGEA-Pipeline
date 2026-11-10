import os
import re
import subprocess


geneid_mapping_file = "input/GeneID_Mapping_Table.tsv"
gene_info_mapping_file = "input/Gene_Information_Table.tsv"
mapping_file = "input/gene_info"
mapping_dict = {}
reverse_mapping_dict = {}



if not os.path.exists(mapping_file):
    print("\nThe gene_info mapping file needed to map the FBgns from the Flybase gene2go file is missing")
    print("Please download it from https://ftp.ncbi.nlm.nih.gov/gene/DATA/ and put into input directory")
    print("Exiting...")
    print("\n")
    exit()

print("\t[inter] Processing mapping file for FlyBase...")
#tax_id	GeneID	Symbol	LocusTag	Synonyms	dbXrefs	chromosome	map_location	
#description	type_of_gene	Symbol_from_nomenclature_authority	Full_name_from_nomenclature_authority	Nomenclature_status	Other_designations	Modification_date	Feature_type
progress = 0

with open(mapping_file, 'r') as infile:
    #total_lines = int(subprocess.getoutput(f"wc -l {mapping_file}").strip().split()[0])
    for line in infile:
        line = line.strip()
        lineArray = line.split('\t')
        
        
        tax_id = lineArray[0]
        if str(tax_id).strip() != "7227":
            continue
        gene_id = lineArray[1]
        symbol = lineArray[2]
        db_xrefs = lineArray[5]
        for db_xref in db_xrefs.split('|'):
            if "flybase" in db_xref.lower():
                fbgn = str(db_xref.split(':')[-1]).strip()
                mapping_dict[fbgn] = {}
                mapping_dict[fbgn]['gene_id'] = gene_id
                mapping_dict[fbgn]['symbol'] = symbol
                reverse_mapping_dict[gene_id] = {}
                reverse_mapping_dict[gene_id]['symbol'] = symbol
                reverse_mapping_dict[gene_id]['fbgn'] = fbgn
    
        #progress += 1
        #print(f"\r\t[inter] {progress}/{total_lines}", end="", flush=True)

'''
with open(geneid_mapping_file, 'r') as infile:
    for line in infile:
        line = line.strip()
        
        lineArray = line.split('\t')
        lineArray = [str(x).strip() for x in lineArray]
        
        idvalue = lineArray[4]
        species_id = lineArray[1]
        if species_id != "7227":
            continue
        
        if not idvalue.lower().startswith('fbgn'):
            continue
        idvalue = idvalue.split('|')[0].strip()
        
        gene_id = lineArray[2]
        
        if idvalue not in mapping_dict.keys():
            mapping_dict[idvalue] = {}
            mapping_dict[idvalue]['gene_id'] = gene_id
        

with open(gene_info_mapping_file, 'r') as infile:
    for line in infile:
        line = line.strip()
        lineArray = line.split('\t')
        lineArray = [str(x).strip() for x in lineArray]
        
        gene_id = lineArray[0]
        species_id = lineArray[1]
        symbol = lineArray[2]
        
        if species_id != "7227":
            continue
        
        specific_geneid = lineArray[6]
        
        if specific_geneid in mapping_dict.keys():
            mapping_dict[specific_geneid]['symbol'] = symbol
        else:
            mapping_dict[specific_geneid] = {}
            mapping_dict[specific_geneid]['gene_id'] = gene_id
            mapping_dict[specific_geneid]['symbol'] = symbol
            
        
'''        
print("\n\t[inter] Done.")
