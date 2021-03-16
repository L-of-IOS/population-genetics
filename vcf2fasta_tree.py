#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file only pick the gene type of the reserved gene and output it.
tips:
1. pass those ##
2. from #CHROM row, get all samples
3. read REF col and ALT col
4. write: use a lot of memory, or just write in 10 files? No, I prefer run over and over


"""

import argparse
import gzip
import csv

parser = argparse.ArgumentParser(description="script to convert an all sites vcf to sweepfinder format. FASTA description will be the sample name in the VCF header.Only does one chromosome/region at a time.")
parser.add_argument("-v", "--vcf", action="store", required=True, help="Input VCF file. Should be a multisample vcf, though it should theoretically work with a single sample.")
parser.add_argument("-o", "--out", action="store", required=True, help="Output filename")
parser.add_argument("-g", "--gzip", action="store_true", required=False, help="Set if the VCF is gzipped.")


args = parser.parse_args()

vcf_in = args.vcf
out_name = args.out

sample_names = []
sample_seqs = []

if args.gzip:
    opener = gzip.open
else:
    opener = open

fasta_out = open(out_name, 'w')
fasta_out.write(">REF\n")




with opener(vcf_in, 'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    
    for row in tsvin:
        if any('##' in strings for strings in row):
            continue
        if any('#CHROM' in strings for strings in row):
            sample_names = row[9:]
            for sample in sample_names:
                sample_seqs.append(sample)
            continue
        chrom,pos,id,ref,alt,qual,filter,info,format=row[0:9]
        fasta_out.write(ref)
    fasta_out.write("\n")



for sample_index,sample in enumerate(sample_seqs):
    fasta_out.write(">"+sample+"\n")
    with opener(vcf_in, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')

        for row in tsvin:
            if any('##' in strings for strings in row):
                continue
            if any('#CHROM' in strings for strings in row):
                continue
            chrom,pos,id,ref,alt,qual,filter,info,format=row[0:9]
            haplotypes = row[9:]
            alt_list = alt.split(",")
            haplotype = haplotypes[sample_index]
            
            if not any(i in haplotype.split(":")[0] for i in ["0","1","2","3"]):
                fasta_out.write("N")
            elif haplotype.split(":")[0].count("3") !=0 and alt_list[2] not in ["*."]:
                fasta_out.write(alt_list[2])
            elif haplotype.split(":")[0].count("2") !=0 and alt_list[1] not in ["*."]:
                fasta_out.write(alt_list[1])
            elif haplotype.split(":")[0].count("1") !=0 and alt_list[0] not in ["*."]:
                fasta_out.write(alt_list[0])
            else :
                fasta_out.write(ref)
        fasta_out.write("\n")
