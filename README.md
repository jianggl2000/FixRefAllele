# FixRef.py

### Usage:
python2        FixRef.py        input.vcf        fixRef.vcf        reference.fasta

The program can be used to correct issue with vcf that the Ref allele not match reference genome sequence. For example,
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT
chr1    69511   .       C       A,G     .       PASS    .       GT:DP

In the vcf file above, the reference genome hg19 has 

### Requirement:
The program depends on samtools to retrieve sequence from reference genome fasta file. Please have samtools installed and path set up before running the program.

### Important
Please note that the program won't fix strand issue, that is, if the VCF file used based from reverse-complement strand, it won't be fixed and will be removed from the VCF file.
