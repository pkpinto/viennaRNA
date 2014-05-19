#include  <stdio.h>
#include  <stdlib.h>
#include  <math.h>
#include  <string.h>

#include  "ViennaRNA/utils.h"
#include  "ViennaRNA/fold.h" // fold
#include  "ViennaRNA/part_func.h" // pf_fold
#include  "ViennaRNA/subopt.h" // subopt
#include  "ViennaRNA/fold_vars.h" // temperature

// mac
// gcc viennarna.c -dynamiclib -o viennarna.so -I /usr/local/include/ -L /usr/local/lib/ -lm -lRNA
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

float seq_eval(const char *sequence, const char *structure)
{
    return energy_of_structure(sequence, structure, 0);
}

float get_T(void) { return temperature; }
void set_T(float T) { temperature = T; }

int main()
{
    const char* sequence = "CGCAGGGAUACCCGCGCC";
    char* structure;
    float mfe, gfe;
    structure = seq_fold(sequence, &mfe);
    printf("%s\n", sequence);
    printf("%s\n", structure);
    structure = seq_pf_fold(sequence, &gfe);
    printf("%s\n", structure);
    printf("%f, %f\n", mfe, gfe);
    SOLUTION* sol = seq_subopt(sequence, 4.0);
    for(SOLUTION* s = sol; s->structure != NULL; s++)
        printf("%f, %s\n", s->energy, s->structure);
    printf("%f\n", seq_eval(sequence, "(((.((.....))))).."));
    printf("%f\n", get_T());
    set_T(15.0);
    printf("%f\n", get_T());
}
