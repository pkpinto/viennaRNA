#include  <stdio.h>
#include  <stdlib.h>
#include  <math.h>
#include  <string.h>
#include  "ViennaRNA/utils.h"
#include  "ViennaRNA/fold_vars.h"
#include  "ViennaRNA/fold.h"
#include  "ViennaRNA/part_func.h"
#include  "ViennaRNA/inverse.h"
#include  "ViennaRNA/RNAstruct.h"
#include  "ViennaRNA/treedist.h"
#include  "ViennaRNA/stringdist.h"
#include  "ViennaRNA/profiledist.h"

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

int main()
{
    char *sequence = "CGCAGGGAUACCCGCGCC";
    char* structure;
    float mfe, gfe;
    structure = seq_fold(sequence, &mfe);
    printf("%s\n", sequence);
    printf("%s\n", structure);
    structure = seq_pf_fold(sequence, &gfe);
    printf("%s\n", structure);
    printf("%f, %f\n", mfe, gfe);
}
