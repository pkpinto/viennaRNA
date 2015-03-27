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

// Build command:
// mac
// gcc viennarna.c -dynamiclib -o viennarna.so -I /usr/local/include/
//         -L /usr/local/lib/ -lm -lRNA
// linux
// gcc viennarna.c -shared -o viennarna.so -lm -lRNA -fopenmp -fpic -std=c99

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

int main()
{
    // Optimal fold
    const char* sequence = "CGCAGGGAUACCCGCGCC";
    char* structure;
    float mfe, gfe;
    structure = seq_fold(sequence, &mfe);
    printf("%s %s %f\n", sequence, structure, mfe);
    free(structure);

    // Ensemble fold
    structure = seq_pf_fold(sequence, &gfe);
    printf("%s %s %f\n", sequence, structure, gfe);
    free(structure);

    printf("\n");

    // Find suboptimal structures
    SOLUTION* sol = seq_subopt(sequence, 4.0);
    for (SOLUTION* s = sol; s->structure != NULL; s++)
    {
        printf("%s %s %f\n", sequence, s->structure, s->energy);
        free(s->structure);
    }
    free(sol);

    printf("\n");

    // Evaluate fe of a structure (given a sequence)...
    printf("%f\n", get_T());
    const char* test_str = "(((.((.....)))))..";
    printf("%s %s %f\n", sequence, test_str, seq_eval(sequence, test_str));
    // ... and how it changes with temperature
    set_T(15.0);
    printf("%f\n", get_T());
    printf("%s %s %f\n", sequence, test_str, seq_eval(sequence, test_str));
    set_T(37.0);

    printf("\n");

    // Take a not so different sequence with a different optimal structure
    const char* seed_seq = "AAUAGGGAUACCCGCGCC";
    structure = seq_fold(seed_seq, &mfe);
    printf("%s %s %f\n", seed_seq, structure, mfe);

    // See that is not even stable on the test fold
    printf("%s %s %f\n", seed_seq, test_str, seq_eval(seed_seq, test_str));

    // Mutate it until you get the test fold...
    char* seq = malloc(strlen(seed_seq) + 1);
    strcpy(seq, seed_seq);
    float dist = str_inverse(seq, test_str, 12345, 0);
    // ... and confirm it's its ground state
    structure = seq_fold(seq, &mfe);
    printf("%s %s %f\n", seq, structure, mfe);

    free(seq);
}
