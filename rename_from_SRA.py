#!/usr/bin/python

org_info = [ \
'Peridinium_bipes Peridinium_bipes Dinophyceae 2868 PRJNA608149 /depot/jwisecav/data/ggavelis/dino_hgt/to_rename/Peridinium_bipes.faa', \
'Gymnoxanthella_radiolariae Gymnoxanthella_radiolariae Dinophyceae 1798043 PRJEB25203 /depot/jwisecav/data/ggavelis/dino_hgt/to_rename/Gymnoxanthella_radiolariae.faa', \
'Brandtodinium_nutricula Brandtodinium_nutricula Dinophyceae 1333877 SAMEA104598819 /depot/jwisecav/data/ggavelis/dino_hgt/to_rename/Brandtodinium_nutricula.faa', \
'Amyloodinium_ocellatum Amyloodinium_ocellatum Dinophyceae 79898 SRR8776921 /depot/jwisecav/data/ggavelis/dino_hgt/to_rename/Amyloodinium_ocellatum.faa' \
]

import os; import re; import Bio; from Bio.Seq import Seq; from Bio import SeqIO; from Bio import pairwise2; from Bio.pairwise2 import format_alignment

for sample in org_info:
    count=0; cluster_count=0
    
    sample = sample.split()
    LIB = sample[0]; ORGNAME = sample[1]; LINEAGE = sample[2]; TAXID = sample[3]; ACCESSION = sample[4]; INFILE = sample[5]
    OUTFILE = OUTPUT_DIR + '/' + LIB + '.faa'
    OUT = open(OUTFILE,"w")
    print(ORGNAME)
    used_ids='blank'; old_cluster='blank' #initialize list to store ids used in each assembly cluster
    
    for seq_record in SeqIO.parse(INFILE, "fasta"):
        count += 1; protein=1
    
        # SEQUENCE 
        sequence = seq_record.seq
        sequence = re.sub(r'\*$', '', str(sequence)) ## removing trailing asterisk (stop codon)
        
        # HEADER
        header = seq_record.id
        
        ####### If the header is in OLD Transdecoder format (e.g. '::' in header, and no unique ORF numbers('p')) ######
        if '::' in header:
            if count < 2:
                print("old transdecoder format (must make own protein numbers)")

            baseid = re.sub(r'::', ':', header)
            baseid = baseid.split(':')[1:4]       ## discarding redund' zeroth field in seqid
            del baseid[1]                         ## remove the "gene field" info from the list, since these are transcripts, gene info not informative
            baseid = '_'.join(baseid)             ## fuse back into string
        
            ## Shorten seq_id -> baseid
            baseid = re.sub(r'.*_DN', '', baseid) ## remove wordy 'TRINITY_DN' prefix
            baseid = re.sub(r'm.*', '', baseid)   ## remove unique 'm' number because we'll instead use a more concise protein number 'p' to make each ORF unique
            baseid = re.sub(r'_', '', baseid)     ## Remove underscores
            baseid = re.sub(r'\.', '', baseid)    ## Remove periods 
        
            ## Assign the transcript to its Trinity assembly cluster
            cluster = re.sub(r'.*_DN','', baseid) ##'cluster' refers to the core 'TRINITY_DNXXX_cX' part of a name. Related/similar transcripts share a cluster.
            cluster = re.sub(r'_m.*','', cluster)
            if cluster != old_cluster:            ## check if we're onto a new cluster
                used_ids = []                     ## If so, reset list of used_IDS
                old_cluster = cluster
                cluster_count += 1          
        
            ## check if baseid has been used already by other proteins in this cluster
            newid = baseid + 'p' + str(protein)
            if newid not in used_ids:
                used_ids.append(newid)      
            else:
                while newid in used_ids:          ## if it's already used, increment by p+1, until p is unique             
                    protein += 1
                    newid = baseid + 'p' + str(protein)  
                    if newid not in used_ids:            
                        newid = baseid + 'p' + str(protein)
                        used_ids.append(newid)               
                        break
        
        ####### else, the header is the NEW transdecoder format (e.g. header has "~~" + p numbers) ########
        else:
            if count < 2:
                print("new transdecoder format (has p numbers already)")
            
            ## shorten seq_id -> baseid
            baseid = re.sub(r'.*_DN', '', header) ## remove wordy 'TRINITY_DN' prefix
            baseid = re.sub(r'_', '', baseid)     ## Remove underscores
            newid = re.sub(r'\.', '', baseid)     ## Remove periods  
            
        ## PUT IT ALL TOGETHER
        newheader = ACCESSION+'_'+newid+'-'+TAXID+'-'+ORGNAME+'-'+LINEAGE
        ##  Remove periods again in case of 'sp. or cf.'
        newheader = re.sub(r'\.', '', newheader)
        
        if count < 2:
            print("example seqid:")
            print(newheader)
        
        OUT.write('>' + str(newheader) + '\n' + str(sequence) + '\n')
    
    OUT.close()
    
    if cluster_count > 0:  
        print(str(cluster_count) + ' assembly clusters')
    print(str(count) + ' proteins renamed')

    ###### Check to make sure seqids in output is unique
    !/depot/jwisecav/data/ggavelis/scripts/is_uniq.sh "$OUTFILE"
    
    print('')
    
print("done")  