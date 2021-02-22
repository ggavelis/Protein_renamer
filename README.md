# Protein_renamer
python | ETE_toolkit

Tools to add phylogeny-ready names (including accession, genus, species, lineage &amp; taxid) to protein fastas from:
* rename_from_SRA.py. (SRA reads that have been assembled in Trinity and AA-predicted in TransDecoder)
* rename_from_genbank.py
* rename_from_supp_data.py

# About the SeqID format:
#### A.
**Full seqid** Example:<br><br>
\>SRR7816690_10015c0g1i1p1-158475-Pfiesteria_sp-Dinophyceae<br><br>

**What each (-) separated field means** <br>
Accession_CoreSeqid - Taxonomy_ID - Genus_species - Lineage<br><br>
1. Accession: SRR if assembled from one Sequence Read Archive run, but a project # if assembled from multiple
2. *CoreSeqid*: only present if we assembled or predicted this protein ourselves -- see part B for details.
3. Taxonomy_ID: this organism's official NCBI taxID #.
4. Genus_species (but includes 'sp' and unofficial names like 'Ross_Sea_Dinoflagellate)
5. Lineage: (E.g. 'Plantae') determined automatically by mapping our taxon_ID and against a custom lineages.dmp file

#### B.
**Core of reformatted Seqid**<br><br>
Example:   *10844c0g1i2* **p1**

I. About the *italics* part:
1. allows the protein to be traced back to the trinity transcript from which it was predicted
2. '10844c0g1i2' is shorted from 'TRINITY_DN10844_c0_g1_i2'
3. proteins that share the '10844c0g1' part but differ in the 'i_' (isoform) number could represent different mature splicing variants of an immature mRNA

II. About the **bold** part:
1. This **p1** is added in TransDecoder when it predicts an one or more ORFS from each transcript. Any p# > 1 means that there were be multiple proteins predicted from the same transcript. 

III: In short: These seqids are long and kind of ugly but are more meaningful than just replacing the trinity+transdecoder output with random accessions. (For example, in downsteam analysis, I'll be able to consider which proteins could have resulted from alternative splicing.)
