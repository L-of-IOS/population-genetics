#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TIPS:
1. read the input file , sort by order
2. read the whole large vcf file and output the needed data
3. write chr pos function in new file

"""




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

if args.gzip:
    opener = gzip.open
else:
    opener = open
