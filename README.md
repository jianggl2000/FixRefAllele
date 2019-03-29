# FixRef.py

# usage:
python2 FixRef.py input.vcf fixRef.vcf reference.fasta

The program can be used to correct issue with vcf that the Ref allele not match reference genome sequence. For example,
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT
chr1    69511   .       C       A,G     .       PASS    .       GT:DP

In the vcf file above, the reference genome hg19 has 

# requirment
The program depends on samtools to retrieve sequence from reference genome fasta file. Please have samtools installed and path set up before running the program.
