from typing import Optional

from fastapi import APIRouter

import viennaRNA as vrna


default_router = APIRouter(prefix='/viennarna/v1')


@default_router.get(
    '/sequence-fold/{sequence}',
    summary='Compute folded structure and associated minimum free energy for a given sequence (at a specified temperature)',
)
async def sequence_fold(sequence: str, T: Optional[float] = 37.0):
    structure, mfe = vrna.sequence_fold(sequence, T=T)
    return {'sequence': sequence, 'temperature': T, 'structure': structure, 'free_energy': mfe}


@default_router.get(
    '/sequence-fold/{sequence}/{structure}',
    summary='Compute free energy of an already folded structure (at a specified temperature)'
)
async def eval_structure(sequence: str, structure: str, T: Optional[float] = 37.0):
    energy = vrna.eval_structure(sequence, structure, T=T)
    return {'sequence': sequence, 'temperature': T, 'structure': structure, 'energy': energy}


@default_router.get(
    '/pf-sequence-fold/{sequence}',
    summary='Compute pairing propensity and ensemble free energy for a given sequence (at a specified temperature)',
)
async def pf_sequence_fold(sequence: str, T: Optional[float] = 37.0):
    structure, gfe = vrna.pf_sequence_fold(sequence, T=T)
    return {'sequence': sequence, 'temperature': T, 'structure': structure, 'free_energy': gfe}


@default_router.get(
    '/subopt-structures/{sequence}',
    summary='Compute all suboptimal secondary structures within a `delta` of the optimum'
)
async def subopt_structures(sequence: str, delta: float, T: Optional[float] = 37.0):
    sol_tuples = vrna.subopt_structures(sequence, delta, sort=True, T=T)
    return {
        'sequence': sequence, 'temperature': T,
        'fold_results': [{'structure': structure, 'energy': energy} for structure, energy in sol_tuples]
    }
