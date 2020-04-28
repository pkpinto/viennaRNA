#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

#include <ViennaRNA/model.h>  // (...)temperature
#include <ViennaRNA/mfe.h>  // vrna_fold
#include <ViennaRNA/part_func.h>  // vrna_pf_fold
#include <ViennaRNA/subopt.h>   // subopt
#include <ViennaRNA/eval.h>  // vrna_eval_structure_simple
#include <ViennaRNA/utils.h>  // xsubi
#include <ViennaRNA/inverse.h>  // inverse_fold, inverse_fold


float get_temperature(void)
{
    return vrna_md_defaults_temperature_get();
}
void set_temperature(float T) 
{
    vrna_md_defaults_temperature(T);
}

float sequence_fold(const char* sequence, char* structure)
{
    return vrna_fold(sequence, structure);
}

float pf_sequence_fold(const char* sequence, char* structure)
{
    return vrna_pf_fold(sequence, structure, NULL);
}

SOLUTION* subopt_structures(const char* sequence, float delta)
{
    int delta_interval = (int)(delta / 0.01);
    // subopt takes the sequence as a char* thought it should be a const char*
    // create a temporary char* where the sequence can be stored
    char* seq = malloc(strlen(sequence) + 1);
    strcpy(seq, sequence);
    SOLUTION* sol = subopt(seq, NULL, delta_interval, NULL);
    free(seq);
    return sol;
}

float eval_structure(const char* sequence, const char* structure)
{
    return vrna_eval_structure_simple(sequence, structure);
}

void initiate_rand(unsigned int seed)
{
    // if rnalib was compiled with HAVE_ERAND48
    xsubi[0] = xsubi[1] = xsubi[2] = (unsigned short) seed;  /* lower 16 bit */
    xsubi[1] += (unsigned short) ((unsigned)seed >> 6);
    xsubi[2] += (unsigned short) ((unsigned)seed >> 12);
    // or without
    srand(seed);
}

float sequence_design(char* sequence, const char* structure, unsigned int rng_seed, int give_up_switch)
{
    give_up = give_up_switch;
    initiate_rand(rng_seed);

    return inverse_fold(sequence, structure);
}

float pf_sequence_design(char* sequence, const char* structure, unsigned int rng_seed, int give_up_switch, float delta_to_target)
{
    give_up = give_up_switch;
    final_cost = delta_to_target;
    initiate_rand(rng_seed);

    return inverse_pf_fold(sequence, structure);
}
