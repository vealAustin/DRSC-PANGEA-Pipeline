from datetime import date
import re
import subprocess

today = date.today()
date_str = today.strftime("%Y-%m-%d")




def outToHighThroughputFile(line_to_print):
    with open(f'./output/{date_str}_high_throughput.tsv', 'a') as highFile:
        highFile.write(line_to_print)
            
        
def outToExperimentalFile(line_to_print):
    with open(f'./output/{date_str}_experimental_file.tsv', 'a') as experFile:
        experFile.write(line_to_print)
    
def outToSlim1Fly(line_to_print):
    with open(f'./output/{date_str}_go_slim_1_fly.tsv', 'a') as outfile1:
        outfile1.write(line_to_print)
    
    
def outToSlim2Fly(line_to_print):
    with open(f'./output/{date_str}_go_slim_2_fly.tsv', 'a') as outfile2:
        outfile2.write(line_to_print)
            
            
def outToSlim1Other(line_to_print):
    with open(f'./output/{date_str}_go_slim_1_other.tsv', 'a') as outfile3:
        outfile3.write(line_to_print)
    
    
def outToSlim2Other(line_to_print):
    with open(f'./output/{date_str}_go_slim_2_other.tsv', 'a') as outfile4:
        outfile4.write(line_to_print)


def main(SpeciesSynonymMappingDict):
    from getGoSlimTerms import go_slim_fly_1_terms, go_slim_fly_2_terms, go_slim_other_1_terms, go_slim_other_2_terms
    global date_str
    testFileList = [f'./output/{date_str}_Merge_File.tsv']
    excludeHighThroughputList = ['HTP', 'HDA', 'HMP', 'HGI', 'HEP', 'RCA']
    includeHighThroughputList = ['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'IBA', 'IBD', 'IRD', 'IKR', 'ISS', 'ISO', 'ISA', 'ISM', 'IGC', 'TAS', 'NAS', 'IC']
    
    experimentalOnlyIncludeList = ['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'HTP', 'HDA', 'HMP', 'HGI', 'HEP']
    
    
    test_go_id_fly_count = 0
    test_go_id = "GO:0006914"
    
    for file in testFileList:
        count = 0
        totalLines = int(subprocess.getoutput(f"wc -l {file}").strip().split()[0])
        with open(file, 'r') as infile:
            for line in infile:
                #GO:2001311      lysobisphosphatidic acid metabolic process      1       biological_process      10116   305795  ISS;ISO
                line = line.strip()
                lineArray = line.split('\t')
                parentTerm = lineArray[0].strip()
                parentProcessName = lineArray[1].strip()
                parentChildrenCount = lineArray[2].strip()
                parentNamespace = lineArray[3].strip()
                tax_id = lineArray[4].strip()
                gene_id = lineArray[5].strip()
                evidence_codes_unf = lineArray[6].strip()
                #print(evidence_codes.strip().split(';'))
                evidence_codes = list(set(evidence_codes_unf.strip().split(';')))
                #print("NEW", evidence_codes)
                
                if tax_id in SpeciesSynonymMappingDict.keys():
                    tax_id = SpeciesSynonymMappingDict[tax_id]
                    
                
                newOutputInfo = f"{parentTerm}\t{parentProcessName}\t{parentChildrenCount}\t{parentNamespace}\t{tax_id}\t{gene_id}\t{';'.join(evidence_codes)}\n"
                
                
                if tax_id == "7227":
                    if parentTerm in go_slim_fly_1_terms:
                        outToSlim1Fly(newOutputInfo)
                        #print("outToSlim1Fly", newOutputInfo)
                    if parentTerm in go_slim_fly_2_terms:
                        outToSlim2Fly(newOutputInfo)
                        #print("outToSlim2Fly", newOutputInfo)
                    
                    if parentTerm == test_go_id:
                        test_go_id_fly_count += 1
                        
                else:
                    #print("TAX ID",tax_id)
                    if parentTerm in go_slim_other_1_terms:
                        outToSlim1Other(newOutputInfo)
                        #print("outToSlim1Other", newOutputInfo)
                    if parentTerm in go_slim_other_2_terms:
                        outToSlim2Other(newOutputInfo)
                        #print("outToSlim2Other", newOutputInfo)
                
                
                
                highThroughputSet = set()
                experimentalSet = set()
                includeInHighThroughput = False
                includeInExperimental = False
                for code in evidence_codes:
                    if code.strip() in includeHighThroughputList:
                        includeInHighThroughput = True
                        if code not in highThroughputSet:
                            highThroughputSet.add(code)
                    
                    if code in experimentalOnlyIncludeList:
                        includeInExperimental = True
                        if code not in experimentalSet:
                            experimentalSet.add(code)
                
                
                
                
                if includeInHighThroughput:
                    newOutputInfo = f"{parentTerm}\t{parentProcessName}\t{parentChildrenCount}\t{parentNamespace}\t{tax_id}\t{gene_id}\t{';'.join(highThroughputSet)}\n"
                    outToHighThroughputFile(newOutputInfo)
                    #print("HIGH THROUGHPUT INFO", newOutputInfo)
                
                if includeInExperimental:
                    newOutputInfo = f"{parentTerm}\t{parentProcessName}\t{parentChildrenCount}\t{parentNamespace}\t{tax_id}\t{gene_id}\t{';'.join(experimentalSet)}\n"
                    outToExperimentalFile(newOutputInfo)
                    #print("EXPERIMENTAL INFO", newOutputInfo)
                    
                
                #print("\n")
                
                count += 1
                print(f"\r{count} / {totalLines}", end="", flush=True)
    
    print("Done.")
    print("TEST GO ID COUNT:", test_go_id_fly_count)
    
if __name__ == "__main__":
    main(SpeciesSynonymMappingDict)
