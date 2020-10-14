## Simulate 3 populations - msprime

Dependency:

- msprime
- tskit
- tabix

Goal: Simulate 1000 YRI, 1000 CEU and 5 CHB (i.e. 2000, 2000 and 10 haploids)


```bash
python sim_demography.py OutOfAfrica_3G11.ts 2000 2000 10
```

```
Model =  hudson(reference_size=1)
=============================
Epoch: 0 -- 920.0 generations
=============================
     start     end      growth_rate |     0        1        2
   -------- --------       -------- | -------- -------- --------
0 |1.45e+04 1.45e+04              0 |     0     2.5e-05  7.8e-06
1 | 3.4e+04 1.03e+03         0.0038 |  2.5e-05     0    3.11e-05
2 |4.59e+04    554           0.0048 |  7.8e-06 3.11e-05     0

Events @ generation 920.0
   - Mass migration: Lineages moved with probability 1.0 backwards in time with source 2 & dest 1
                     (equivalent to migration from 1 to 2 forwards in time)
   - Migration rate change to 0 everywhere
   - Migration rate change for (0, 1) to 0.00015
   - Migration rate change for (1, 0) to 0.00015
   - Population parameter change for 1: initial_size -> 1861 growth_rate -> 0
==================================
Epoch: 920.0 -- 2040.0 generations
==================================
     start     end      growth_rate |     0        1        2
   -------- --------       -------- | -------- -------- --------
0 |1.45e+04 1.45e+04              0 |     0     0.00015     0
1 |1.86e+03 1.86e+03              0 |  0.00015     0        0
2 |   554     2.56           0.0048 |     0        0        0

Events @ generation 2040.0
   - Mass migration: Lineages moved with probability 1.0 backwards in time with source 1 & dest 0
                     (equivalent to migration from 0 to 1 forwards in time)
   - Migration rate change to 0 everywhere
===================================
Epoch: 2040.0 -- 5920.0 generations
===================================
     start     end      growth_rate |     0        1        2
   -------- --------       -------- | -------- -------- --------
0 |1.45e+04 1.45e+04              0 |     0        0        0
1 |1.86e+03 1.86e+03              0 |     0        0        0
2 |  2.56   2.09e-08         0.0048 |     0        0        0

Events @ generation 5920.0
   - Population parameter change for 0: initial_size -> 7310
================================
Epoch: 5920.0 -- inf generations
================================
     start     end      growth_rate |     0        1        2
   -------- --------       -------- | -------- -------- --------
0 |7.31e+03 7.31e+03              0 |     0        0        0
1 |1.86e+03 1.86e+03              0 |     0        0        0
2 |2.09e-08     0            0.0048 |     0        0        0
```

The output is tree sequence stored in `OutOfAfrica_3G11.ts`. A tree sequence describe a collection of genomes as a sequence of trees. Each tree represent a genome region.


```bash
python -m tskit info OutOfAfrica_3G11.ts
```
```
sequence_length:  250000000.0
trees:            1610243
samples:          4010
individuals:      0
nodes:            924311
edges:            6281688
sites:            2082643
mutations:        2082643
migrations:       0
populations:      3
provenances:      1
```


```bash
python -m tskit vcf --ploidy 2 OutOfAfrica_3G11.ts | bcftools view -Oz > OutOfAfrica_3G11.vcf.gz
bcftools stats OutOfAfrica_3G11.vcf.gz
```
```
...
# SN    [2]id   [3]key  [4]value
SN      0       number of samples:      2005
SN      0       number of records:      2082643
SN      0       number of no-ALTs:      0
SN      0       number of SNPs: 2082643
SN      0       number of MNPs: 0
SN      0       number of indels:       0
SN      0       number of others:       0
SN      0       number of multiallelic sites:   0
SN      0       number of multiallelic SNP sites:       0
...
```

## Simulate 3 population - stdpop

Link to stdpop [here](https://stdpopsim.readthedocs.io/en/latest/installation.html)


```bash
stdpopsim HomSap -c chr1 -o OutOfAfrica_3G09.ts -d OutOfAfrica_3G09 2000 2000 10
```

```
Simulation information:
    Engine: msprime (0.7.4)
    Model id: OutOfAfrica_3G09
    Model desciption: Three population out-of-Africa
    Population: number_samples (sampling_time_generations):
        YRI: 2000 (0)
        CEU: 2000 (0)
        CHB: 10 (0)
Contig Description:
    Contig length: 249250621.0
    Mean recombination rate: 1.1485597641285933e-08
    Mean mutation rate: 1.29e-08
    Genetic map: None

If you use this simulation in published work, please cite:
[stdpopsim]
Adrion et al., 2019: https://doi.org/10.1101/2019.12.20.885129
[simulation engine]
Kelleher et al., 2016: https://doi.org/10.1371/journal.pcbi.1004842
[genome assembly]
The Genome Sequencing Consortium, 2001: http://dx.doi.org/10.1038/35057062
[mutation rate]
Tian, Browning, and Browning, 2019: https://doi.org/10.1016/j.ajhg.2019.09.012
[recombination rate]
The International HapMap Consortium, 2007: https://doi.org/10.1038/nature06258
[demographic model]
Gutenkunst et al., 2009: https://doi.org/10.1371/journal.pgen.1000695
```


```bash
python -m tskit info OutOfAfrica_3G09.ts
```

```
sequence_length:  249250621.0
trees:            1686068
samples:          4010
individuals:      0
nodes:            969773
edges:            6556330
sites:            1978294
mutations:        1978294
migrations:       0
populations:      3
provenances:      2
```


```bash
python -m tskit vcf --ploidy 2 OutOfAfrica_3G09.ts | bcftools view -Oz > OutOfAfrica_3G09.vcf.gz
bcftools stats OutOfAfrica_3G09.vcf.gz
```
```
...
# SN    [2]id   [3]key  [4]value
SN      0       number of samples:      2005
SN      0       number of records:      1978294
SN      0       number of no-ALTs:      0
SN      0       number of SNPs: 1978294
SN      0       number of MNPs: 0
SN      0       number of indels:       0
SN      0       number of others:       0
SN      0       number of multiallelic sites:   0
SN      0       number of multiallelic SNP sites:       0
...
```


# Simulate European+African, simulate African American, add mutations

```
# 1. msprime simulate 1000 European, 1000 African, 5 Asian
# similar to above. Except for mutation_rate=0
python sim_demography_preadmix.py AA_ancestor.ts 2000 2000 10

# 2. SLiM admixture 80% Euro+20% Afr for 10 generations
slim -m -d "N=10" -d "ints='demographic.ts'" -d "outts='admixture.ts'" -d "NUM_AA=1000" sim_admixture.slim

# 3. Add mutations to the tree sequence. 
# <Input tree sequence> <output prefix> <number of admixed individuals>
python mutate_tree.py admixture.ts admixture_mutate 1000
```



