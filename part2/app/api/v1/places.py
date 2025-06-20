from flask_restx import Namespace, Resource, fields, abort
from app.services import facade


api = Namespace('places', description='Place operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(description='Amenity UUID'),
    'name': fields.String(description='Amenity name')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User UUID'),
    'first_name': fields.String(description='Owner first name'),
    'last_name': fields.String(description='Owner last name'),
    'email': fields.String(description='Owner email')
})

# ----Input schema for create/update----
place_input = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title'),
    'description': fields.String(description='Description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude (-90 to 90)'),
    'longitude': fields.Float(required=True, description='Longitude (-180 to 180)'),
    'owner_id': fields.String(required=True, description='Owner User UUID'),
    'amenities': fields.List(fields.String, required=True, description='List of Amenity UUIDs')
})

# Lightweight listing schema
place_list = api.model('PlaceList', {
    'id': fields.String,
    'title': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float
})

# Detailed view schema
place_detail = api.model('PlaceDetail', {
    'id': fields.String,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model))
})

# ----Partial update schema (Optional but implemented to pass al tests)----
place_update = api.model('PlaceUpdate', {
    'title': fields.String(description='Title'),
    'description': fields.String(description='Description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude (-90 to 90)'),
    'longitude': fields.Float(description='Longitude (-180 to 180)'),
    'owner_id': fields.String(description='Owner User UUID'),
    'amenities': fields.List(fields.String, description='List of Amenity UUIDs')
})


@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_list)
    def get(self):
        """List all places"""
        return facade.get_all_places(), 200

    @api.expect(place_input, validate=True)
    @api.marshal_with(place_detail, code=201)
    def post(self):
        """Create a new place"""
        try:
            place = facade.create_place(api.payload)
            return place, 201
        except ValueError as err:
            abort(400, str(err))

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_detail)
    def get(self, place_id):
        """Retrieve a place by ID (with owner & amenities)"""
        place = facade.get_place(place_id)
        if not place:
            abort(404, 'Place not found')
        return place, 200

    @api.expect(place_update, validate=True)
    @api.marshal_with(place_detail)
    def put(self, place_id):
        """Update an existing place"""
        try:
            updated = facade.update_place(place_id, api.payload)
            if not updated:
                abort(404, 'Place not found')
            return updated, 200
        except ValueError as err:
            abort(400, str(err))
