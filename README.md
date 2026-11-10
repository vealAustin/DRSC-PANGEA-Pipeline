# DRSC-PANGEA-Pipeline

Pipeline Assumptions
-----------------------------------------------------------------
1. The files listed below should be in the input directory and
   should have the exact name as specified:
      - gene2go
      - go-basic.obo
      - gene_info
      - Geneset_assignment.xlsx
2. The first argument is a file (preferably a .tsv) that has the
   species information for the species you want with the
   columns being:
   Synonym Species ID\tActual Species ID\tSpecies Specific ID type
       - Ex. 559292\t4932\tSGD\n4932\t4932\tSGD
3. The second argument is the Fly gene association file if being
   used (see the base file)
