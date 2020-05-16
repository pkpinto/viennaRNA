from flask import current_app
from flask_restx import Api, Resource, fields

import viennaRNA as vrna


api = Api(current_app)
ns = api.namespace('viennarna/v1', description='viennaRNA API')

# input
fold_request = api.parser()
fold_request.add_argument('sequence', type=str, required=True, help='RNA sequence', location='form')
fold_request.add_argument('temperature', type=float, help='Termodynamic temperature', default=37, location='form')

# output
fold_result = api.model('FoldResult', {
    'structure': fields.String(description='Folded structure'),
    'energy': fields.Float(description='Energy of the fold (kcal/mol)'),
})

@ns.route('/sequence_fold')
@ns.doc(parser=fold_request)
class SequenceFold(Resource):
    ''' '''

    @ns.marshal_with(fold_result, code=200)
    def post(self):
        ''' '''
        args = fold_request.parse_args()
        structure, mfe = vrna.sequence_fold(args['sequence'], T=args['temperature'])
        return {'structure': structure, 'energy': mfe}

@ns.route('/pf_sequence_fold')
@ns.doc(parser=fold_request)
class PFSequenceFold(Resource):
    ''' '''

    @ns.marshal_with(fold_result, code=200)
    def post(self):
        ''' '''
        args = fold_request.parse_args()
        structure, gfe = vrna.pf_sequence_fold(args['sequence'], T=args['temperature'])
        return {'structure': structure, 'energy': gfe}
