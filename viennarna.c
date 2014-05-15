#include  <stdio.h>
#include  <stdlib.h>
#include  <math.h>
#include  <string.h>

#include  "ViennaRNA/utils.h"
#include  "ViennaRNA/fold.h" // fold
#include  "ViennaRNA/part_func.h" // pf_fold
#include  "ViennaRNA/subopt.h" // subopt

// gcc viennarna.c -dynamiclib -o viennarna.dylib -I /usr/local/include/ -L /usr/local/lib/ -lm -lRNA
// gcc viennarna.c -shared -o viennarna.so -lm -lRNA -fopenmp -fpic

char* seq_fold(char* sequence, float* mfe)
{
    char* structure = (char*)space(sizeof(char) * (strlen(sequence) + 1));
    *mfe = fold(sequence, structure);
    free_arrays();
    return structure;
}

char* seq_pf_fold(char* sequence, float* gfe)
{
    char* structure = (char*)space(sizeof(char) * (strlen(sequence) + 1));
    *gfe = pf_fold(sequence, structure);
    free_pf_arrays();
    return structure;
}

SOLUTION* seq_subopt(char* sequence, float delta)
{
    int delta_intervals = (int)(delta / 0.01);
    SOLUTION* sol = subopt(sequence, NULL, delta_intervals, NULL);
    return sol;
}

int main()
{
    char* sequence = "CGCAGGGAUACCCGCGCC";
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
}
