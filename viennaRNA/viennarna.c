#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

#include "ViennaRNA/utils.h"
#include "ViennaRNA/fold.h"  // fold
#include "ViennaRNA/part_func.h"  // pf_fold
#include "ViennaRNA/subopt.h"   // subopt
#include "ViennaRNA/fold_vars.h"  // temperature
#include "ViennaRNA/inverse.h"  // inverse

char* seq_fold(const char* sequence, float* mfe)
{
    char* structure = (char*)space(sizeof(char) * (strlen(sequence) + 1));
    *mfe = fold(sequence, structure);
    free_arrays();
    return structure;
}

char* seq_pf_fold(const char* sequence, float* gfe)
{
    char* structure = (char*)space(sizeof(char) * (strlen(sequence) + 1));
    *gfe = pf_fold(sequence, structure);
    free_pf_arrays();
    return structure;
}

SOLUTION* seq_subopt(const char* sequence, float delta)
{
    int delta_intervals = (int)(delta / 0.01);
    // subopt takes the sequence as a char* thought it should be a const char*
    // create a temporary char* where the sequence can be stored
    char* seq = malloc(strlen(sequence) + 1);
    strcpy(seq, sequence);
    SOLUTION* sol = subopt(seq, NULL, delta_intervals, NULL);
    free(seq);
    return sol;
}

float seq_eval(const char* sequence, const char* structure)
{
    return energy_of_structure(sequence, structure, 0);
}

float get_T(void) { return temperature; }
void set_T(float T) { temperature = T; }

void initiate_rand(unsigned int seed)
{
    // if rnalib was compiled with HAVE_ERAND48
    xsubi[0] = xsubi[1] = xsubi[2] = (unsigned short) seed;  /* lower 16 bit */
    xsubi[1] += (unsigned short) ((unsigned)seed >> 6);
    xsubi[2] += (unsigned short) ((unsigned)seed >> 12);
    // or without
    srand(seed);
}

float str_inverse(char* sequence, const char* structure,
                  unsigned int rng_seed, int give_up_switch)
{
    give_up = give_up_switch;
    initiate_rand(rng_seed);

    return inverse_fold(sequence, structure);
}

float str_pf_inverse(char* sequence, const char* structure,
                     unsigned int rng_seed, int give_up_switch,
                     float delta_to_target)
{
    give_up = give_up_switch;
    final_cost = delta_to_target;
    initiate_rand(rng_seed);

    return inverse_pf_fold(sequence, structure);
}
