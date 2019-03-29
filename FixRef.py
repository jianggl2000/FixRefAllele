#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import re
import subprocess

def processVCF(infile, outfile, refile):
    nRef = nFlip = nErr = 0
    input = open(infile)
    output = open(outfile, "w")
    for line in input.readlines():
        lines = line.split("\t")
        if line.startswith("#"):
            output.write(line)
        else:
            Chr = lines[0]
            Ref = lines[3]
            Alts = lines[4].split(",")            
            Start = lines[1]
            End1 = str(int(Start) + len(Ref) - 1)
            CMD = "samtools faidx " + refile +" "+ Chr+":"+Start+"-"+End1
            rd = os.popen(CMD)
            rText = rd.read()
            refSeq = rText.split("\n")[1]
            rd.close()

            NoRef = True #none of the allele can be found in reference sequence
            if Ref == refSeq:
                nRef = nRef+1
                output.write(line)
                NoRef = False
                continue
            else:
                for i,allele in enumerate(Alts):
                    End2 = str(int(Start) + len(allele)-1)
                    CMD = "samtools faidx " + refile +" "+ Chr+":"+Start+"-"+End2
                    rd = os.popen(CMD)
                    rText = rd.read()
                    refSeq = rText.split("\n")[1]
                    rd.close()
                    if allele == refSeq:
                        NoRef = False
                        nFlip = nFlip+1
                        lines[3] = refSeq
                        newAlts = Alts
                        newAlts.remove(allele)
                        newAlts.insert(i, Ref)
                        lines[4] = ",".join(newAlts)
                        for j in range(9, len(lines)): #genotype for sample j
                            if lines[j].rstrip() == ".":
                                continue
                            Geno = lines[j].rstrip().split(":")
                            GT = Geno[0]
                            if re.search("/", GT):
                                GTs = GT.split("/")
                                tmpGTs = GTs
                                for t in range(0,2):
                                    if tmpGTs[t] == '0':
                                        GTs[t] = str(i+1)
                                    elif tmpGTs[t] == str(i+1):
                                        GTs[t] = '0'
                                if int(GTs[0]) > int(GTs[1]):
                                    tmp = GTs[0]
                                    GTs[0] = GTs[1]
                                    GTs[1] = tmp
                                GT = "/".join(GTs)
                                Geno[0] = GT
                                lines[j] = ":".join(Geno)
                            elif re.search("\|", GT):
                                GTs = GT.split("|")
                                tmpGTs = GTs
                                for t in range(0,2):
                                    if tmpGTs[t] == '0':
                                        GTs[t] = str(i+1)
                                    elif tmpGTs[t] == str(i+1):
                                        GTs[t] = '0'
                                if int(GTs[0]) < int(GTs[1]):
                                    tmp = GTs[0]
                                    GTs[0] = GTs[1]
                                    GTs[1] = tmp
                                GT = "|".join(GTs)
                                Geno[0] = GT
                                lines[j] = ":".join(Geno)
                            else:
                                print "Error: Non-missing genotype not seperated by '/' nor '|' at %s:%s" % (Chr, Start)
                        line = "\t".join(lines).rstrip()+"\n"
                        output.write(line)
                        continue #stop once found match allele
            if NoRef:
                nErr = nErr+1
                print "Reference allele not found for %s:%s-%s %s %s" % (lines[0], Start, End1, lines[3], lines[4])

    print "*****************************************\n"
    print "* Number of variants have matched allele: %s\n" % (nRef)
    print "* Number of variants have flipped allele: %s\n" % (nFlip)
    print "* Number of variants have no-match allele: %s\n" % (nErr)
    print "*****************************************\n"
    input.close()
    output.close()

if __name__=="__main__":
    print "Please note that this software can only be used to flip Ref and Alt alleles to make the Ref allele same as reference genome.\nMake sure you have the same version of reference for variant calling."
    print "Read from %s, and save to %s" % (sys.argv[1], sys.argv[2])
    processVCF(sys.argv[1], sys.argv[2], sys.argv[3])
