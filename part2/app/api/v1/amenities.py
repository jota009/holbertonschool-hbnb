from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity UUID'),
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        return facade.get_all_amenities(), 200

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        return facade.create_amenity(api.payload), 201

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity, 200


    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an existing amenity"""
        updated = facade.update_amenity(amenity_id, api.payload)
        if not updated:
            api.abort(404, 'Amenity not found')
        return updated, 200


