"""Output tree sequence
function out_of_africa was copied from user manual of msprime.
Parameters updated according to Gravel 2011. Table 2.
Numbers in the comments are the original parameters in Gutenkunst 2009 Table 1..

length (genome), recombination_rate and mutation_rate should be set in the return line of out_of_africa. I left mutation_rate empty because I use the output for forward simulation in SLiM and add mutations after that. If you only use msprime, please modify the return line and choose which object to dump

Changes
-------
03 06 2020:
    Removed migration between African and European before the split
"""

import msprime
import pyslim
import math
import sys
import argparse

parser = argparse.ArgumentParser(description="Simulate YRI, CEU and CHB populations and output as tskit's tree saequence format")
parser.add_argument("out",help="Output filename")
parser.add_argument("sample_n_AF",help="Sample size of YRI")
parser.add_argument("sample_n_EU",help="Sample size of CEU")
parser.add_argument("sample_n_AS",help="Sample size of CHB")
args = parser.parse_args()

def out_of_africa(sample_n_AF, sample_n_EU, sample_n_AS):
    # First we set out the maximum likelihood values of the various parameters
    # given in Table 1.
    N_A = 7310
    N_B = 1861
    N_AF = 14474 # 12300
    N_EU0 = 1032 # 1000
    N_AS0 = 554 # 510
    # Times are provided in years, so we convert into generations.
    generation_time = 25
    T_AF = 148e3 / generation_time # 220e3
    T_B = 51e3 / generation_time # 140e3
    T_EU_AS = 23e3 / generation_time # 21.2e3
    # We need to work out the starting (diploid) population sizes based on
    # the growth rates provided for these two populations
    r_EU = 0.0038 # 0.004
    r_AS = 0.0048 # 0.0055
    N_EU = N_EU0 / math.exp(-r_EU * T_EU_AS)
    N_AS = N_AS0 / math.exp(-r_AS * T_EU_AS)
    # Migration rates during the various epochs.
    m_AF_B = 15e-5 # 25e-5
    m_AF_EU = 2.5e-5 # 3e-5
    m_AF_AS = 0.78e-5 # 1.9e-5
    m_EU_AS = 3.11e-5 # 9.6e-5
    # Population IDs correspond to their indexes in the population
    # configuration array. Therefore, we have 0=YRI, 1=CEU and 2=CHB
    # initially.
    # Set sample_size of YRI, CEU and CHB you want to output in the current generation
    population_configurations = [
        msprime.PopulationConfiguration(
            sample_size=sample_n_AF, initial_size=N_AF),
        msprime.PopulationConfiguration(
            sample_size=sample_n_EU, initial_size=N_EU, growth_rate=r_EU),
        msprime.PopulationConfiguration(
            sample_size=sample_n_AS, initial_size=N_AS, growth_rate=r_AS)
    ]
    migration_matrix = [
        [      0, m_AF_EU, m_AF_AS],
        [m_AF_EU,       0, m_EU_AS],
        [m_AF_AS, m_EU_AS,       0],
    ]
    demographic_events = [
        # CEU and CHB merge into B with rate changes at T_EU_AS
        msprime.MassMigration(
            time=T_EU_AS, source=2, destination=1, proportion=1.0),
        msprime.MigrationRateChange(time=T_EU_AS, rate=0),
        msprime.MigrationRateChange(
            time=T_EU_AS, rate=m_AF_B, matrix_index=(0, 1)),
        msprime.MigrationRateChange(
            time=T_EU_AS, rate=m_AF_B, matrix_index=(1, 0)),
        msprime.PopulationParametersChange(
            time=T_EU_AS, initial_size=N_B, growth_rate=0, population_id=1),
        # Population B merges into YRI at T_B
        msprime.MassMigration(
            time=T_B, source=1, destination=0, proportion=1.0),
        msprime.MigrationRateChange(time=T_B, rate=0), ## Missing in the old tutorial. update 03 06 2020
        # Size changes to N_A at T_AF
        msprime.PopulationParametersChange(
            time=T_AF, initial_size=N_A, population_id=0)
    ]
    # Use the demography debugger to print out the demographic history
    # that we have just described.
    dd = msprime.DemographyDebugger(
        population_configurations=population_configurations,
        migration_matrix=migration_matrix,
        demographic_events=demographic_events)
    dd.print_history()

    # set mutation_rate to you need to genotypes
    return msprime.simulate(
        population_configurations=population_configurations,
        migration_matrix=migration_matrix,
        demographic_events=demographic_events,
        length=2.5e8,
        recombination_rate=1e-8,
        mutation_rate=0
    )

outofafrica_tree = out_of_africa(arg.sample_n_AF, arg.sample_n_EU, arg.sample_n_AS)
# If you want msprime tree sequence
#outofafrica_tree.dump(arg.out)

# If your analysis is followed by SLiM
new_outofafrica_tree = pyslim.annotate_defaults(outofafrica_tree, model_type="WF", slim_generation=1)
new_outofafrica_tree.dump(arg.out)

