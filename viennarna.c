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

typedef struct
{
    char *sequence;
    char *structure;
    float mfe;
    float gfe;
}
seqdata;

void sequencefold(seqdata *s)
{
    char *_struct = (char *)space(sizeof(char) * (strlen(s->sequence) + 1));
    s->mfe = fold(s->sequence, _struct);
    s->structure = _struct;
    free_arrays();
}

void sequencepf(seqdata *s)
{
    char *_struct = (char *)space(sizeof(char) * (strlen(s->sequence) + 1));
    s->gfe = pf_fold(s->sequence, _struct);
    free_pf_arrays();
}

int main()
{
    seqdata s;
    s.sequence = "CGCAGGGAUACCCGCGCC";
    sequencefold(&s);
    printf("%s\n", s.sequence);
    printf("%s\n", s.structure);
    sequencepf(&s);
    printf("%f, %f\n", s.mfe, s.gfe);
    float kT = (temperature + 273.15) * 1.98717 / 1000.;  /* kT in kcal/mol */
    printf("%f\n", exp(-(s.mfe - s.gfe) / kT));
}