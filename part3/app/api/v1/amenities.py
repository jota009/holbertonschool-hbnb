from flask_restx import Namespace, Resource, fields, abort
# from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade


api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity UUID'),
    'name': fields.String(required=True, description='Amenity name')
})


@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        return facade.get_all_amenities(), 200

    # @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    # @api.response(403, 'Admin privileges required')
    def post(self):
        """Public: Create a new amenity"""
        # claims = get_jwt()
        # if not claims.get('is_admin'):
            # abort(403, 'Admin privileges required')
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity, 201
        except ValueError as e:
            abort(400, str(e))


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Public: Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            abort(404, 'Amenity not found')
        return amenity, 200

    # @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    # @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Public: Update an existing amenity"""
        # claims = get_jwt()
        # if not claims.get('is_admin'):
            # abort(403, 'Admin privileges required')
        try:
            updated = facade.update_amenity(amenity_id, api.payload)
            if not updated:
                abort(404, 'Amenity not found')
            return updated, 200
        except ValueError as e:
            abort(400, str(e))
