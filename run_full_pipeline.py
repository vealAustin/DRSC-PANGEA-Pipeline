import re
import subprocess
from datetime import date
import sys
import time
import os
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook, Workbook

#PROGRAM IMPORTS
import createGOTree
import getGenesPerParent
import findGenesPerParent_Direct_Go
import merge_all
import assembleMappingFiles
import assignGenesetCategoryID
import createSubsets
import processGeneInfoFile





today = date.today()
date_str = today.strftime("%Y-%m-%d")



SpeciesSynonymMappingDict = {}
SpeciesInfoDict = {}

#GLOBALS
BASE_GENESET_INFO = [
    {'name': 'Direct GO Biological Processes', 'name_prev': 'GO BP All', 'sub_group_name': 'Direct GO term only', 'group_name': 'Gene Ontology Sets', 'order': '4',
    'long_description': 'GO Biological Process Annotations - direct to term; no enrichment using GO relationships', 'table_name': 'ET_Genes2Go_bp'},
    {'name': 'Direct GO Cellular Component', 'name_prev': 'GO CC All', 'sub_group_name': 'Direct GO term only', 'group_name': 'Gene Ontology Sets', 'order': '4',
    'long_description': 'GO Celular Component Annotations - direct to term; no enrichment using GO relationships', 'table_name': 'ET_Genes2Go_cc'},
    {'name': 'Direct GO Molecular Function', 'name_prev': 'GO MF All', 'sub_group_name': 'Direct GO term only', 'group_name': 'Gene Ontology Sets', 'order': '4',
    'long_description': 'GO Molecular Function Annotations  - direct to term; no enrichment using GO relationships', 'table_name': 'ET_Genes2Go_mf'},
    {'name': 'EXP GO Biological Processes', 'name_prev': 'GO BP Experiment Only', 'sub_group_name': 'Experimental data only', 'group_name': 'Gene Ontology Gene Annotation Subsets', 'order': '17',
    'long_description': 'GO Biological Process Annotations (direct to term), only  experimental data', 'table_name': 'ET_Genes2Go_bp_exp'},
    {'name': 'EXP GO Cellular Component', 'name_prev': 'GO CC Experiment Only', 'sub_group_name': 'Experimental data only', 'group_name': 'Gene Ontology Gene Annotation Subsets', 'order': '17',
    'long_description': 'GO Cellular Component Annotations (direct to term), only  experimental data', 'table_name': 'ET_Genes2Go_cc_exp'},
    {'name': 'EXP GO Molecular Function', 'name_prev': 'GO MF Experiment Only', 'sub_group_name': 'Experimental data only', 'group_name': 'Gene Ontology Gene Annotation Subsets', 'order': '17',
    'long_description': 'GO Molecular Function Annotations (direct to term), only  experimental data', 'table_name': 'ET_Genes2Go_mf_exp'},
    {'name': 'No HTP GO Biological Processes', 'name_prev': 'GO BP exclude High Throughput', 'sub_group_name': 'Excluding high-throughput experiments', 'group_name': 'Gene Ontology Gene Annotation Subsets', 'order': '15',
    'long_description': 'GO Biological Process Annotations (direct to term), excluding high throughput evidence', 'table_name': 'ET_Genes2Go_bp_high_th'},
    {'name': 'No HTP GO Cellular Component', 'name_prev': 'GO CC exclude High Throughput', 'sub_group_name': 'Excluding high-throughput experiments', 'group_name': 'Gene Ontology Gene Annotation Subsets', 'order': '15',
    'long_description': 'GO Celular Component Annotations (direct to term), excluding high throughput evidence', 'table_name': 'ET_Genes2Go_cc_high_th'},
    {'name': 'No HTP GO Molecular Function', 'name_prev': 'GO MF exclude High Throughput', 'sub_group_name': 'Excluding high-throughput experiments', 'group_name': 'Gene Ontology Gene Annotation Subsets', 'order': '15',
    'long_description': 'GO Molecular Function Annotations (direct to term), excluding high throughput evidence', 'table_name': 'ET_Genes2Go_mf_high_th'},
    {'name': 'SLIM1 GO BP', 'name_prev': 'SLIM1 GO BP', 'sub_group_name': 'Generic GO consortium Subsets (GO slim)', 'group_name': 'Gene Ontology Subsets', 'order': '11',
    'long_description': 'GO Biological Process, high-level categorization set . 20 terms.', 'table_name': '-'},
    {'name': 'SLIM1 GO CC', 'name_prev': 'SLIM1 GO CC', 'sub_group_name': 'Generic GO consortium Subsets (GO slim)', 'group_name': 'Gene Ontology Subsets', 'order': '11',
    'long_description': 'GO Cellular Component, high-level categorization set . 10 terms.', 'table_name': '-'},
    {'name': 'SLIM1 GO MF', 'name_prev': 'SLIM1 GO MF', 'sub_group_name': 'Generic GO consortium Subsets (GO slim)', 'group_name': 'Gene Ontology Subsets', 'order': '11',
    'long_description': 'GO Molecular Function, high-level categorization set. 18 terms.', 'table_name': '-'},
    {'name': 'SLIM2 GO BP', 'name_prev': 'SLIM2 GO BP', 'sub_group_name': 'AGR GO Subsets (GO slim)', 'group_name': 'Gene Ontology Subsets', 'order': '13',
    'long_description': 'GO Biological Process  subset,  for enrichment analysis . 84  terms.', 'table_name': '-'},
    {'name': 'SLIM2 GO CC', 'name_prev': 'SLIM2 GO CC', 'sub_group_name': 'AGR GO Subsets (GO slim)', 'group_name': 'Gene Ontology Subsets', 'order': '13',
    'long_description': 'GO Cellular Component  subset,  for enrichment analysis . 20 terms.', 'table_name': '-'},
    {'name': 'SLIM2 GO MF', 'name_prev': 'SLIM2 GO MF', 'sub_group_name': 'AGR GO Subsets (GO slim)', 'group_name': 'Gene Ontology Subsets', 'order': '13',
    'long_description': 'GO Molecular Function, high-level categorization set. 18 terms.', 'table_name': '-'},
    {'name': 'GO Biological Processes', 'name_prev': 'GO BP All Flatten', 'sub_group_name': 'Using GO hierarchy', 'group_name': 'Gene Ontology Sets', 'order': '0',
    'long_description': 'GO Biological Process Annotations, enrichment uses GO relationships to transit enrichment to parent terms', 'table_name': 'ET_Genes2Go_bp'},
    {'name': 'GO Cellular Component', 'name_prev': 'GO CC All Flatten', 'sub_group_name': 'Using GO hierarchy', 'group_name': 'Gene Ontology Sets', 'order': '0',
    'long_description': 'GO Biological Process Annotations, enrichment uses GO relationships to transit enrichment to parent terms', 'table_name': 'ET_Genes2Go_cc'},
    {'name': 'GO Molecular Function', 'name_prev': 'GO MF All Flatten', 'sub_group_name': 'Using GO hierarchy', 'group_name': 'Gene Ontology Sets', 'order': '0',
    'long_description': 'GO Biological Process Annotations, enrichment uses GO relationships to transit enrichment to parent terms.', 'table_name': 'ET_Genes2Go_mf'},
]

PROCESS_GENE2GO_FILE = f"output/{date_str}_gene2go_processed"
GO_TREE_FILE = f"output/{date_str}_GO_Tree.tsv"
GENE_PER_GO_FILE = f"output/{date_str}_GO_Tree_W_Gene_Count.tsv"
FLYBASE_GENE_PER_GO_FILE = f"output/{date_str}_FlyBase_GO_Tree_W_Gene_Count.tsv"
DIRECT_GO_GENES_PER_GO_FILE = f"output/{date_str}_Direct_GO_genesPerParent_w_count.tsv"
MERGE_FILE = f"output/{date_str}_Merge_File.tsv"
DIRECT_MERGE_FILE = f"output/{date_str}_merge_direct_GO.tsv"
GENE_INFO_FILE = f"input/{date_str}_Gene_Information.tsv"
GENESET_FINAL_FILE = f"output/{date_str}_geneset_file.tsv"
GENE2GENESET_FILE = f"output/{date_str}_gene2geneset_all_species.tsv"
HIGHTHROUGHPUT_FILE = f"output/{date_str}_high_throughput.tsv"
EXPERIMENTAL_FILE = f"output/{date_str}_experimental_file.tsv"
SLIM_FLY_1_FILE = f"output/{date_str}_go_slim_1_fly.tsv"
SLIM_FLY_2_FILE = f"output/{date_str}_go_slim_2_fly.tsv"
SLIM_OTHER_1_FILE = f"output/{date_str}_go_slim_1_other.tsv"
SLIM_OTHER_2_FILE = f"output/{date_str}_go_slim_2_other.tsv"



species_list = None
FLYBASE_GENE2GO = None
species_without_fly = None
Geneset_Assignment_File = None
species_file = None
speciesFileSep = None
genomeGeneCountDict = {}


#there is a gene_information and geneid_mapping file in the input directory
print("---------------PIPELINE ASSUMPTIONS---------------")
print("1. gene2go file is in input directory and")
print("\t the file name is gene2go")
print("\n")
print("2. go-basic.obo file is in input directory")
print("\twith the exact name go-basic.obo")
print("\n")
print("3. first argument passed in is the location")
print("\tof a file specifying the species you ")
print("\tare looking for in the format below: ")
print("\tSynonym_Species_ID\tActual_Species_ID\tSpecies_Specific_Gene_ID_Type")
print("\tEx. 559292\t4932\tSGD\n4932\t4932\tSGD\netc...")
print("\n")
print("4. gene_info file is in input directory and")
print("\tthe exact file name is gene_info")
print("\n")
print("5. Geneset_assignment file is in input")
print("\tdirectory with the name: geneset_assignment.")
print("\tCan be a .tsv, .csv, .xlsx, or .xls")
print("\n")
time.sleep(5)

print("ARGV:", sys.argv)
print("ARGV len:", len(sys.argv))
print("\n")

if len(sys.argv) < 2:
    print("Argument list is invalid")
    exit()

elif len(sys.argv) > 3:
    print("Argument list is invalid")
    exit()
elif len(sys.argv) == 3:
    FLYBASE_GENE2GO = sys.argv[2]


#STEP 0.5 Make sure the input and output directories exist and gene2go, go-basic.obo files exist
os.makedirs('input', exist_ok=True)
os.makedirs('output', exist_ok=True)


fileMissing = False
if FLYBASE_GENE2GO:
    if not os.path.exists(FLYBASE_GENE2GO):
        fileMissing = True
        print("Flybase gene2go file entered but not found")
        print("Please make sure the file is located in the input directory")
    if not os.path.exists("input/gene_info"):
        print("gene_info file was not found in input directory")
        print("Downloading and unzipping one now")
        subprocess.getoutput(f"cd {Path.cwd()}/input && wget https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz && gunzip gene_info.gz")
        print("Done")


if not os.path.exists('input/gene2go'):
    print("gene2go file doesn't exist")
    print("Need the gene2go file with the exact name in the input directory")
    fileMissing = True

if not os.path.exists("input/go-basic.obo"):
    print("go-basic.obo file was not found")
    print("Need the go-basic.obo file with that exact name in input directory")
    fileMissing = True

if fileMissing:
    exit()



#STEP 1 - Process the gene2go file with all the species needed
if sys.argv[1]:
    species_line = None
    incorrectFormat = False
    species_file = sys.argv[1].strip()
    species_list = []
    if species_file.endswith('.tsv') or species_file.endswith('.csv'):
        speciesFileSep = "tsv" if species_file.endswith('.tsv') else "csv"
        with open(species_file, 'r') as infile:
            for line in infile:
                line = line.strip()
                lineArray = line.split('\t') if species_file.endswith('.tsv') else line.split(',')
                lineArray = [str(x).strip() for x in lineArray]
                if len(lineArray) != 3:
                    incorrectFormat = True
                    break
                else:
                    species_list.append(lineArray[0])
                    SpeciesSynonymMappingDict[lineArray[0]] = lineArray[1]
                    SpeciesInfoDict[lineArray[0]] = {}
                    SpeciesInfoDict[lineArray[0]]['actualSpeciesId'] = lineArray[1]
                    SpeciesInfoDict[lineArray[0]]['speciesSpecificIdType'] = lineArray[2]

    elif species_file.endswith('.xlsx') or species_file.endswith('.xls'):
        speciesFileSep = "excel"
        df = pd.read_excel(species_file, sheet_name=0)
        count = 0
        for row in df.to_dict(orient="records"):
            if len(row) != 3:
                incorrectFormat = True
                break
            else:
                if count == 0 and re.match(r"^[0-9]+$", f"{row[list(row.keys())[0]]}"):
                    lineArray = [str(x).strip() for x in row.keys()]
                    species_list.append(lineArray[0])
                    SpeciesSynonymMappingDict[lineArray[0]] = lineArray[1]
                    SpeciesInfoDict[lineArray[0]] = {}
                    SpeciesInfoDict[lineArray[0]]['actualSpeciesId'] = lineArray[1]
                    SpeciesInfoDict[lineArray[0]]['speciesSpecificIdType'] = lineArray[2]

                lineArray = [str(x).strip() for x in row.values()]
                species_list.append(lineArray[0])
                SpeciesSynonymMappingDict[lineArray[0]] = lineArray[1]
                SpeciesInfoDict[lineArray[0]] = {}
                SpeciesInfoDict[lineArray[0]]['actualSpeciesId'] = lineArray[1]
                SpeciesInfoDict[lineArray[0]]['speciesSpecificIdType'] = lineArray[2]

            count += 1
    else:
        print("Make sure the species input file is either a .tsv, .csv, .xlsx or .xls file")
        incorrectFormat = True


    if incorrectFormat:
        print("Species list is in an incorrect format. See format below")
        print("Synonym_Species_ID\tActual_Species_ID\tSpecies_Specific_Gene_ID_Type")
        print("559292\t4932\tSGD\n")
        print("4932\t4932\tSGD\n")
        print("7227\t7227\tFlyBase\n")
        print("Etc.")
        exit()







species_list_formatted = None
gene2goSpeciesLine = None
if FLYBASE_GENE2GO:
    species_without_fly = [str(x).strip() for x in species_list if str(x).strip() != "7227"]
    species_list_formatted = [f"^{str(x).strip()}" for x in species_without_fly]
else:
    species_list_formatted = [f"^{str(x).strip()}" for x in species_list]


gene2goSpeciesLine = "|".join(species_list_formatted)


if not os.path.exists(PROCESS_GENE2GO_FILE):
    print("Processing gene2go file...")
    subprocess.getoutput(f'egrep -Ew "{gene2goSpeciesLine}" input/gene2go > {PROCESS_GENE2GO_FILE}')
    if FLYBASE_GENE2GO:
        with open(FLYBASE_GENE2GO, 'r') as infile, open(PROCESS_GENE2GO_FILE, 'a') as outfile:
            for line in infile:
                line = line.strip()
                lineArray = line.split('\t')
                if line.startswith('!'):
                    continue

                outfile.write(line + "\n")
    print("Done")
    print("\n")
else:
    print("Gene2go file already processed.")





#if FLYBASE_GENE2GO:


#STEP 2 - Create GO Tree

if not os.path.exists(GO_TREE_FILE):
    print("Creating GO Tree...")
    createGOTree.main()
    print("Done")
    print("\n")
else:
    print("GO Tree already created.")


print("SPECIES LIST:", species_list)
#STEP 3 - Get genes per parent
if not os.path.exists(f"{GENE_PER_GO_FILE}"):
    print("Getting genes per GO...")

    getGenesPerParent.getGenesPerParent()
    print("Done.")
    print("\n")
else:
    print("Genes per GO file already created.")


if not os.path.exists(DIRECT_GO_GENES_PER_GO_FILE):
    print("Getting genes per GO for direct go terms...")
    findGenesPerParent_Direct_Go.main()
    print("Done.")
else:
    print("Direct genes per GO file already created.")


if not os.path.exists(MERGE_FILE):
    print("Creating the merge file...")
    merge_all.main(SpeciesSynonymMappingDict)
    print("Done.")
else:
    print("Merge file already created.")

if not os.path.exists(DIRECT_MERGE_FILE):
    import merge_Direct_GO
    print("Creating the Direct merge file...")
    merge_Direct_GO.main()
    print("Done.")
else:
    print("Direct Merge file already created.")



#Create the category assignment file with the new species if there are new species

#check if there are new species
#Get all the current species from the current assignment file
geneset_assignment_file = subprocess.getoutput("find input -type f -name 'Geneset_assignment*'").strip()
Geneset_Assignment_File = [str(x).strip() for x in geneset_assignment_file.split('\n') if re.search(r"Geneset_assignment\.", x)]
if not Geneset_Assignment_File:
    print("Geneset_assignment File can't be found.")
    print("Please make sure it is in the input directory and is named: Geneset_assignment")
    exit()

Geneset_Assignment_File = Geneset_Assignment_File[0]


incorrectAssignmentFormat = False
geneset_assignment_species = set()
geneset_assignment_all_info = []
largestGenesetID = 0
seperator = None
if Geneset_Assignment_File.endswith('.tsv') or Geneset_Assignment_File.endswith('.csv'):
    seperator = "tsv" if Geneset_Assignment_File.endswith('.tsv') else "csv"
    with open(Geneset_Assignment_File, 'r') as infile:
        for line in infile:
            line = line.strip()
            lineArray = line.split('\t') if Geneset_Assignment_File.endswith('.tsv') else line.split(',')
            lineArray = [str(x).strip() for x in lineArray]
            if len(lineArray) != 15:
                incorrectAssignmentFormat = True
                break
            else:
                geneset_assignment_species.add(lineArray[7])
                currentDict = {'id': lineArray[0], 'name': lineArray[1], 'name_prev': lineArray[2], 'sub_group_name': lineArray[3], 'group_name': lineArray[4],
                    'order': lineArray[5], 'gene_name_terms': lineArray[6], 'species_id': lineArray[7], 'comment': lineArray[8], 'genome_gene_count': lineArray[9],
                    'long_description': lineArray[10], 'table_name': lineArray[11]}
                geneset_assignment_all_info.append(currentDict)
                if int(lineArray[0]) > largestGenesetID:
                    largestGenesetID = int(lineArray[0])

elif Geneset_Assignment_File.endswith('.xlsx') or Geneset_Assignment_File.endswith('.xls'):
    seperator = "excel"
    df = pd.read_excel(Geneset_Assignment_File)
    for row in df.to_dict(orient="records"):
        if len(row) != 15:
            incorrectAssignmentFormat = True
            break
        else:
            if row['id'] > largestGenesetID:
                largestGenesetID = row['id']
            geneset_assignment_species.add(str(row['species_id']).strip())
            geneset_assignment_all_info.append(row)


if incorrectAssignmentFormat:
    print("Geneset Assignment file is in the incorrect format")
    print("Headers show be as shown below")
    print("id\tname\tname_prev\tsub_group_name\tgroup_name\torder\tgene_name_terms\trow_count\tunique_gene_count\tspecies_id\tcomment\tgenome_gene_count\tlong_description\ttable_name\tnew_info\n")
    print("Use - for empty")
    print("If this is your first time running the pipeline you can leave row_count, unique_gene_count and genome_gene_count empty")
    exit()




#Create Mapping File with new species




#ALWAYS PROCESS THIS TO GET THE GENOME GENE COUNT INFO
arguments = ["gene_information", "input/gene_info", SpeciesInfoDict, GENE_INFO_FILE]
print("Assembling mapping files...")
genomeGeneCountDict, finalMappingDict = assembleMappingFiles.main(arguments)
print("Done.")


print("GENOME GENE COUNT DICT:", genomeGeneCountDict)
print("TYPE:", type(genomeGeneCountDict))


difference = set(species_list) - geneset_assignment_species

final_new_species_list = set()
new_species_assignment_info = {}
for key in SpeciesSynonymMappingDict.keys():
    if key in difference:
        if SpeciesSynonymMappingDict[key] not in geneset_assignment_species:
            final_new_species_list.add(SpeciesSynonymMappingDict[key])


if seperator == "tsv" or seperator == "csv":
    with open(Geneset_Assignment_File, 'a') as outfile:
        for species in final_new_species_list:
            for geneset_info_dict in BASE_GENESET_INFO:
                largestGenesetID += 1
                if species not in new_species_assignment_info.keys():
                    new_species_assignment_info[species] = []

                new_species_assignment_info[species].append(largestGenesetID)
                if seperator == "tsv":
                    outLine = f"{largestGenesetID}\t{geneset_info_dict['name']}\t{geneset_info_dict['name_prev']}\t{geneset_info_dict['sub_group_name']}\t{geneset_info_dict['group_name']}\t{geneset_info_dict['order']}\t-\t-\t-\t{species}\t-\t{genomeGeneCountDict[species]['genome_gene_count']}\t{geneset_info_dict['long_description']}\t{geneset_info_dict['table_name']}\tnew species added: {date_str}\n"
                else:
                    outLine = f"{largestGenesetID},{geneset_info_dict['name']},{geneset_info_dict['name_prev']},{geneset_info_dict['sub_group_name']},{geneset_info_dict['group_name']},{geneset_info_dict['order']},-,-,-,{species},-,{genomeGeneCountDict[species]['genome_gene_count']},{geneset_info_dict['long_description']},{geneset_info_dict['table_name']},new species added: {date_str}\n"
                outfile.write(outLine)

elif seperator == "excel":
    workbook = None
    if not os.path.exists(Geneset_Assignment_File):
        workbook = Workbook()

    else:
        workbook = load_workbook(Geneset_Assignment_File)

    worksheet = workbook.active
    for species in final_new_species_list:
        for geneset_info_dict in BASE_GENESET_INFO:
            if species not in new_species_assignment_info.keys():
                new_species_assignment_info[species] = []
            largestGenesetID += 1
            new_species_assignment_info[species].append(largestGenesetID)
            current_info = [largestGenesetID, geneset_info_dict['name'], geneset_info_dict['name_prev'], geneset_info_dict['sub_group_name'], geneset_info_dict['group_name'], geneset_info_dict['order'], "-", "-", "-", species, "-", genomeGeneCountDict[species]['genome_gene_count'], geneset_info_dict['long_description'], geneset_info_dict['table_name'], f"new species added: {date_str}"]
            worksheet.append(current_info)

    workbook.save(Geneset_Assignment_File)

print("Done.")



if not os.path.exists(HIGHTHROUGHPUT_FILE) or not os.path.exists(EXPERIMENTAL_FILE) or not os.path.exists(SLIM_FLY_1_FILE) or not os.path.exists(SLIM_FLY_2_FILE) or not os.path.exists(SLIM_OTHER_1_FILE) or not os.path.exists(SLIM_OTHER_2_FILE):
    print("Creating subset files...")
    createSubsets.main(SpeciesSynonymMappingDict)
    print("Done")
else:
    print("Already created subset files.")


if not os.path.exists(GENESET_FINAL_FILE) or not os.path.exists(GENE2GENESET_FILE):
    print("Creating final files...")
    assignGenesetCategoryID.main(finalMappingDict, SpeciesSynonymMappingDict)
    print("Done.")
else:
    print("Already assigned geneset category ids.")


if new_species_assignment_info:
    print("Updating Geneset Assignment files columns: row_count and unique_gene_count for the species:", ", ".join(final_new_species_list))
    geneset_df = None
    if seperator == "excel":
        geneset_df = pd.read_excel(Geneset_Assignment_File)

    else:
        df = None
        if seperator == "tsv":
            geneset_df = pd.read_csv(Geneset_Assignment_File, sep="\t")
        else:
            geneset_df = pd.read_csv(Geneset_Assignment_File)


    #NEED TO ADD THE NEW INFORMATION TO THE GENESET ASSIGNMENT FILE
    gene2geneset_df = pd.read_csv(GENE2GENESET_FILE, sep="\t")
    #need to populate row_count and unique_gene_count for the new species

    for species in final_new_species_list:
        for geneset_id in new_species_assignment_info[species]:
            #find the right row of the dataframe
            mask = geneset_df["id"] == geneset_id
            matches = gene2geneset_df[gene2geneset_df["GENESET_CATEGORY_ID"] == geneset_id]

            geneset_df.loc[mask, "row_count"] = len(matches["GENE_ID"])
            geneset_df.loc[mask, "unique_gene_count"] = matches["GENE_ID"].nunique()

    if seperator == "excel":
        geneset_df.to_excel(Geneset_Assignment_File, index=False)
    elif seperator == "tsv":
        geneset_df.to_csv(Geneset_Assignment_File, sep="\t", index=False)
    else:
        geneset_df.to_csv(Geneset_Assignment_File, index=False)


print("\n\nPipeline Finished!")
