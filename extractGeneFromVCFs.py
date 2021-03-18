#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TIPS:
1. read the input file , sort by order
2. read the whole large vcf file and output the needed data
3. write chr pos function in new file

"""
class My_window:
    def __init__(self,i,CHR,bin_in,bin_out):
        self.CHR = CHR
        self.ind = i
        self.bin_in = bin_in
        self.bin_out = bin_out

    
    

windows = []

import argparse
import gzip
import csv

parser = argparse.ArgumentParser(description="script to extract all GFF annotations from noted vcf file")
parser.add_argument("-v", "--vcf", action="store", required=True, help="Input VCF file. Should be a multisample vcf, though it should theoretically work with a single sample.")
parser.add_argument("-i", "--input", action="store", required=True, help="Input file with chr window_in window_end columns")
parser.add_argument("-o", "--out", action="store", required=True, help="Output filename")
parser.add_argument("-g", "--gzip", action="store_true", required=False, help="Set if the VCF is gzipped.")

args = parser.parse_args()
vcf_in = args.vcf
out_name = args.out
win_input = args.input

if args.gzip:
    opener = gzip.open
else:
    opener = open



with open(win_input,mode = 'r') as win_file:    
    for row in win_file:
        if "chrom\t" in row:
            continue
        else :
            CHR,bin_in,bin_out = row.split()[0:3]
            windows.append(My_window(i = len(windows),
		CHR = CHR,bin_in = bin_in,bin_out = bin_out))

##sort class
windows = sorted(windows,key = lambda x:  (x.CHR,x.bin_in))

out_file = open(out_name,mode = 'w')
out_file.write("CHROM\tpos\tfunction\n")

with opener(vcf_in, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')

        for row in tsvin:
            if any('##' in strings for strings in row):
                continue
            if any('#CHROM' in strings for strings in row):
                continue
            chrom,pos,id,ref,alt,qual,filter,info,format=row[0:9]
            haplotypes = row[9:]            
            if not any(chrom  in i.CHR for i in windows):
                continue
            elif all(int(pos) < k for k in [int(i.bin_out) for i in windows if chrom ==i.CHR \
                                            and  int(pos) < int(i.bin_in)] \
                     and int(pos) > p for p in [int(i.bin_out) for i in windows if chrom ==i.CHR \
                                                and int(pos) > int(i.bin_in) ]) :
                    ##if  bin_in<pos<bin_out and chr == chr
                    notes = info.split("|")[1:]
                    notes = '\t'.join(notes)
                    out_file.write(chrom+"\t"+str(pos)+"\t"+notes+"\n")





