###A script to remove none-chromosome contigs
import gzip
import csv
import argparse
import sys

parser = argparse.ArgumentParser(description="script to remove all none-chromosome contigs")
parser.add_argument("-v", "--vcf", action="store", required=True, help="Input VCF file. Should be a multisample vcf, though it should theoretically work with a single sample.")
parser.add_argument("-o", "--out", action="store", required=True, help="Output filename")
parser.add_argument("-c", "--chrom_list", action="store", required=True, help="indiviul file with chromosome list to output. Should be something in the first column of the vcf.")
parser.add_argument("-g", "--gzip", action="store_true", required=False, help="Set if the VCF is gzipped.")

args = parser.parse_args()
vcf_in = args.vcf
out_name = args.out
chrom_in = args.chrom_list
rows_finished = 0

if args.gzip:
    opener = gzip.open
else:
    opener = open
#out_chr = args.chromosome
with open(chrom_in,"r") as chrom_in_list:
    chromlist = chrom_in_list.readline()


out_vcf = open(out_name+"nocontig.vcf",mode = "w")
writein = out_vcf.writelines(row)
with opener(vcf_in, 'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    for row in tsvin:
        if any('##' in strings for strings in row):
            row.append("\n")
            if any('##contig=<ID=' in strings for strings in row):
                if any(chroms in row for chroms in chromlist ):
                    writein
                    continue
                else:
                    continue
            else:
                writein
                continue
        if any('#CHROM' in strings for strings in row):
            writein
            continue
        chrom,pos,id,ref,alt,qual,filter,info,format=row[0:9]
        row.append("\n")
        haplotypes = row[9:]
        if chrom in chromlist:
            writein
        rows_finished+=1
        if round(rows_finished) == rows_finished/500000:
            print(str(rows_finished)+" rows finished, now on chr "+chrom)
    print("done")
        
