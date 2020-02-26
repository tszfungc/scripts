""" Add Mutation to the tree
Input:
-----
    INTS:
        input tree sequence to add mutation
    PREFIX:
        output prefix

Output:
------
    <PREFIX>.ts:
        output tree sequence with mutation
    <PREFIX>.vcf:
        output in vcf format

Notes:
-----
    By default, the individual names are tsk_[0-9]+ in the order of
    admixed population at current time
    populations in the input tree sequence in SLiM (YRI, CEU, CHB)
    admixed population at 0 generation

    e.g. 1000 YRI, 1000 CEU, 5 ASN, and 1000 admixed individuals would be
    tsk_0 - tsk_999: admixed individuals at current time
    tsk_1000 - tsk_1999: YRI
    tsk_2000 - tsk_2999: CEU
    tsk_3000 - tsk_3004: CHB


"""
import pyslim
import msprime
import sys

INTS=sys.argv[1]
PREFIX=sys.argv[2]

# Input read tree
tree_seq = pyslim.load(INTS)

# Add mutation mutation rate 1.25e-8
mut_tree = pyslim.SlimTreeSequence(msprime.mutate(tree_seq, rate=1.25e-8))

# Write mutated tree
mut_tree.dump(PREFIX+".ts")

with open(PREFIX+".vcf", "w") as f:
    mut_tree.write_vcf(f, ploidy=2, individuals=list(range(3005)))

