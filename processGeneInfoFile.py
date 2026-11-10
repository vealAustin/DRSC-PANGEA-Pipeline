import re
import subprocess
import pandas as pd






def main(SpeciesInfoDict):
    
    gene_info_file = "input/gene_info"
    
    print("SpeciesInfoDict:", SpeciesInfoDict)
    
    actual_species_ids = [str(key).strip() for key in SpeciesInfoDict.keys()]
    final_mapping_dict = {str(SpeciesInfoDict[key]['actualSpeciesId']).strip(): str(SpeciesInfoDict[key]['speciesSpecificIdType']).strip() for key in SpeciesInfoDict.keys()}
    
    actual_species_ids_string = [f"^{val}" for val in actual_species_ids]
    #so I can keep the header for pandas
    actual_species_ids_string.append("^#tax_id")
    actual_species_ids_string = "|".join(actual_species_ids_string)
    
    cmd = f"""egrep "{actual_species_ids_string}" {gene_info_file} > {gene_info_file}_formatted"""
    print("COMMAND:", cmd)
    subprocess.getoutput(cmd)
    subprocess.getoutput(f"ls {gene_info_file}_formatted")
    
    
    gene_info_file_formatted = "input/gene_info_formatted"
    df = pd.read_csv(gene_info_file_formatted, sep="\t")
    
    for row in df.to_dict(orient="records"):
        if row['Symbol'].strip().lower() == "newentry":
            continue
        print(row)
        exit()
    
    





if __name__ == "__main__":
    main(SpeciesInfoDict)