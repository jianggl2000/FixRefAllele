### FixRef.py: Fix reference allele in vcf file

```bash
python2   FixRef.py   input.vcf   fixRef.vcf   reference.fasta
```

#### Usage:
The program can be used to correct issue with VCF that the REF allele does not match the reference genome sequence. For example,
```
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT   S1    S2    S3
chr1    69511   .       C       A,G     .       PASS    .       GT       0/0   0/1   1/2
```
The reference genome hg19 has "A" base at the location chr1:69511. However, in the vcf file above, 'A' is one of the alternative allele. The _FixRef.py_ program will set A as REF allele, and C,G as ALT alleles, and change the genotype call for samples S1, S2 and S3 to 1/1, 0/0, 0/2 accordingly.

The output file for the variant above is as following,

```
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT    S1    S2    S3
chr1    69511   .       A       C,G     .       PASS    .       GT        1/1   0/1   0/2
```
For variants do not find matched allele with reference genome, the information about that variant will be output to screen.

The program can be used to correct allele issue when merge multiple gvcf file with gvcftools.

#### Requirement:
The program depends on samtools to retrieve sequence from reference genome fasta file. Please have samtools installed and path set up before running the program.

#### Important:
Please note that the program assumes all the variants using the reference sequncing to call variants, and it won't fix strand issue, that is, if the VCF file used reverse-complement strand to call variant, the problem won't be fixed and the variant will be removed from the VCF file.

#### linkout:
   - [gvcftools](https://sites.google.com/site/gvcftools/)
   - [bcftools +fixref](https://samtools.github.io/bcftools/howtos/plugin.fixref.html)
