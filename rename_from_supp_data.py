#!/usr/bin/python

## From paper: https://onlinelibrary.wiley.com/doi/full/10.1111/jpy.12947
## Example header for Symbiodinium_tridacnidorum.v2020.faa:
## >Stri.gene2.mRNA

org_info = [ \
'Breviolum_minutum Breviolum_minutum Dinophyceae 2499525 PMID31713873 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Breviolum_minutum.v2020.faa', \
'Cladocopium_goreaui Cladocopium_goreaui Dinophyceae 2499525 PMID31713873 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Cladocopium_goreaui.v2020.faa', \
'Cladocopium_sp_C92 Cladocopium_sp_C92 Dinophyceae 452016 PMID31713873 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Cladocopium_sp_C92.v2020.faa', \
'Fugacium_kawagutii Fugacium_kawagutii Dinophyceae 2697096 PMID31713873 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Fugacium_kawagutii.v2020.faa', \
'Symbiodinium_microadriaticum Symbiodinium_microadriaticum Dinophyceae 2951 PMID31713873 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Symbiodinium_microadriaticum.v2020.faa', \
'Symbiodinium_tridacnidorum Symbiodinium_tridacnidorum Dinophyceae 1602974 PMID31713873 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Symbiodinium_tridacnidorum.v2020.faa' \
]

for sample in org_info:
    
    sample = sample.split()
    LIB = sample[0]; ORGNAME = sample[1]; LINEAGE = sample[2]; TAXID = sample[3]; ACCESSION = sample[4]; INFILE = sample[5]
    OUTFILE = OUTPUT_DIR + '/' + LIB + '.faa'
    OUT = open(OUTFILE,"w")
    print(ORGNAME)
    
    for seq_record in SeqIO.parse(INFILE, "fasta"):
        count += 1; protein=1
    
        # SEQUENCE 
        sequence = seq_record.seq
        newsequence = re.sub(r'\*$', '', str(sequence)) ## removing trailing asterisk (stop codon)
        
        # HEADER
        baseid = seq_record.id
        baseid = re.sub(r'^.....','',baseid)            ## remove four_letter_species_code_&_period
        baseid = baseid.replace('gene','g').replace('.mRNA','m')
        
        ## PUT IT ALL TOGETHER
        newheader = ACCESSION + '_' + baseid + '-'+TAXID+'-'+ORGNAME+'-'+LINEAGE
        
        if count < 2:
            print("example seqid:")
            print(newheader)
        
        OUT.write('>' + newheader + '\n' + newsequence + '\n')
    
    OUT.close()
    
    print(str(count) + ' proteins renamed')

    ###### Check to make sure sequids in output is unique
    !/depot/jwisecav/data/ggavelis/scripts/is_uniq.sh "$OUTFILE"

    
    print(ORGNAME)
    print(str(count) + ' proteins renamed')
    print('')
print("all done")