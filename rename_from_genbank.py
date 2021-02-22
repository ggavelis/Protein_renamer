#!/usr/bin/python

org_info = [ \
'Vitrella_brassicaformis Vitrella_brassicaformis other_Alveolata 1169539 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Vitrella_brassicaformis.v1.faa', \
'Perkinsus_chesapeaki Perkinsus_chesapeaki other_Alveolata 330153 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Perkinsus_chesapeaki.v1.faa', \
'Perkinsus_marinus Perkinsus_marinus other_Alveolata 423536 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Perkinsus_marinus.v1.faa', \
'Perkinsus_olseni Perkinsus_olseni other_Alveolata 32597 /depot/jwisecav/data/ggavelis/dino_hgt/genomes/Perkinsus_olseni.v1.faa'       
]

for sample in org_info:
    
    count=0; idlist = []   
    sample = sample.split()
    LIB = sample[0]; ORGNAME = sample[1]; LINEAGE = sample[2]; TAXID = sample[3]; ACCESSION = sample[4]; INFILE = sample[5]
    OUTFILE = OUTPUT_DIR + '/' + LIB + '.faa'
    OUT = open(OUTFILE,"w")
    
    print('renaming sample ' + LIB)

    for seq_record in SeqIO.parse(INFILE, "fasta"):
        count += 1
        
        header = seq_record.id
        sequence = seq_record.seq
    
        # SEQUENCE
        newsequence = re.sub(r'\*$', '', str(sequence)) #Removing trailing asterisk (stop codon)

        # HEADER
        baseheader = seq_record.id
        accession = baseheader.replace('.1','') # Extract the genbank accession for that transcript
                
        #PUT IT ALL TOGETHER
        newheader = accession+'-'+TAXID+'-'+ORGNAME+'-'+LINEAGE
        
        if count < 2:
            print("example seqid:"); print(newheader)
        
        OUT.write('>' + newheader + '\n' + newsequence + '\n')
    OUT.close()
    
    print(str(count) + ' proteins renamed')

    ###### Check to make sure sequids in output is unique
    !/depot/jwisecav/data/ggavelis/scripts/is_uniq.sh "$OUTFILE"
    
    print(ORGNAME + '\n' + str(count) + ' proteins renamed')
print("all done")