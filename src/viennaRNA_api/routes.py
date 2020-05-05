from flask import current_app
from flask_restx import Api, Resource, fields

import viennaRNA as vrna


api = Api(current_app)
ns = api.namespace('viennarna/v1', description='viennaRNA API')

# input parser
fold_parser = api.parser()
fold_parser.add_argument('sequence', type=str, required=True, help='RNA sequence', location='form')
fold_parser.add_argument('temperature', type=float, help='Termodynamic temperature', default=37, location='form')

# output model
fold_result = api.model('FoldResult', {
    'structure': fields.String(description='Folded structure'),
    'energy': fields.Float(description='Energy of the fold (kcal/mol)'),
})

@ns.route('/sequence-fold')
@ns.doc(parser=fold_parser)
class SequenceFold(Resource):
    ''' '''

    @ns.marshal_with(fold_result, code=200)
    def post(self):
        ''' '''
        args = fold_parser.parse_args()
        structure, mfe = vrna.sequence_fold(args['sequence'], T=args['temperature'])
        return {'structure': structure, 'energy': mfe}

@ns.route('/pf-sequence-fold')
@ns.doc(parser=fold_parser)
class PFSequenceFold(Resource):
    ''' '''

    @ns.marshal_with(fold_result, code=200)
    def post(self):
        ''' '''
        args = fold_parser.parse_args()
        structure, gfe = vrna.pf_sequence_fold(args['sequence'], T=args['temperature'])
        return {'structure': structure, 'energy': gfe}

# input parser
subopt_parser = api.parser()
subopt_parser.add_argument('sequence', type=str, required=True, help='RNA sequence', location='form')
subopt_parser.add_argument('delta', type=float, required=True, help='Energy interval where to fold', location='form')
subopt_parser.add_argument('temperature', type=float, help='Termodynamic temperature', default=37, location='form')

# output model
fold_result_list = api.model('FoldResultList', {
    'fold_results': fields.List(fields.Nested(fold_result), description='List of folded structures, (structure, energy) tuples'),
})

@ns.route('/subopt-structures')
@ns.doc(parser=subopt_parser)
class SuboptStructures(Resource):
    ''' '''

    @ns.marshal_with(fold_result_list, code=200)
    def post(self):
        ''' '''
        args = subopt_parser.parse_args()
        sol_tuples = vrna.subopt_structures(args['sequence'], args['delta'], sort=True, T=args['temperature'])
        return {'fold_results': [{'structure': structure, 'energy': energy} for structure, energy in sol_tuples]}

# input parser
eval_parser = api.parser()
eval_parser.add_argument('sequence', type=str, required=True, help='RNA sequence', location='form')
eval_parser.add_argument('structure', type=str, required=True, help='RNA structure', location='form')
eval_parser.add_argument('temperature', type=float, help='Termodynamic temperature', default=37, location='form')

# output model
eval_result = api.model('EvalResult', {
    'energy': fields.Float(description='Energy of the fold (kcal/mol)'),
})

@ns.route('/eval-structure')
@ns.doc(parser=eval_parser)
class EvalStructure(Resource):
    ''' '''

    @ns.marshal_with(eval_result, code=200)
    def post(self):
        ''' '''
        args = eval_parser.parse_args()
        energy = vrna.eval_structure(args['sequence'], args['structure'], T=args['temperature'])
        return {'energy': energy}
