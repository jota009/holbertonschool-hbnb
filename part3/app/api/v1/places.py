from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.api.v1.reviews import review_model as place_review_model


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
    # 'owner_id': fields.String(required=True, description='Owner User UUID'),
    'amenities': fields.List(fields.String, required=True, description='List of Amenity UUIDs')
})

# ----Update schema ----
place_update = api.model('PlaceUpdate', {
    'title': fields.String(description='Title'),
    'description': fields.String(description='Description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude (-90 to 90)'),
    'longitude': fields.Float(description='Longitude (-180 to 180)'),
    # 'owner_id': fields.String(description='Owner User UUID'),
    'amenities': fields.List(fields.String, description='List of Amenity UUIDs')
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
    'amenities': fields.List(fields.Nested(amenity_model)),
    'reviews': fields.List(fields.Nested(place_review_model), description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_list)
    def get(self):
        """List all places"""
        return facade.get_all_places(), 200

    @jwt_required()
    @api.expect(place_input, validate=True)
    @api.marshal_with(place_detail, code=201)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid data')
    def post(self):
        """Create a new place (owner set from token)"""
        user_id = get_jwt_identity()
        data = api.payload.copy()
        data['owner_id'] = user_id
        try:
            place = facade.create_place(data)
            return place, 201
        except ValueError as err:
            abort(400, str(err))


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_detail)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Public: Retrieve a place by ID (with owner, amenities & reviews)"""
        place = facade.get_place(place_id)
        if not place:
            abort(404, 'Place not found')
        return place, 200

    @jwt_required()
    @api.expect(place_update, validate=True)
    @api.marshal_with(place_detail)
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update an existing place (owner or admin)"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            abort(404, 'Place not found')

        # Only admin or owner can update
        if not is_admin and place.owner.id != user_id:
            abort(403, 'Unauthorized action')

        try:
            updated = facade.update_place(place_id, api.payload)
            return updated, 200
        except ValueError as err:
            abort(400, str(err))


@api.route('/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.marshal_list_with(place_review_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Public: List all reviews for a specific place"""
        try:
            return facade.get_reviews_by_place(place_id), 200
        except ValueError:
            abort(404, 'Place not found')
