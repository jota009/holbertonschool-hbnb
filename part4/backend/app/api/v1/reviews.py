from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('reviews', description='Review operations')

# Input model for POST & PUT
review_input = api.model('ReviewInput', {
    'place_id': fields.String(required=True, description='Place UUID'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)')
})

# Output model for listing & detail
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='Review UUID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(attribute='user.id', description='User UUID'),
    'place_id': fields.String(attribute='place.id', description='Place UUID')
})

# Partial‐update schema
review_update = api.model('ReviewUpdate', {
    'text':     fields.String(description='Review text'),
    'rating':   fields.Integer(description='Rating (1–5)')
})


@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """Public: Retrieves a list of all reviews"""
        return facade.get_all_reviews(), 200

    @jwt_required()
    @api.expect(review_input, validate=True)
    @api.marshal_list_with(review_model, code=201)
    @api.response(400, 'Cannot review own place or duplicate review')
    @api.response(404, 'Place not found')
    def post(self):
        """Authenticated: Register a new review (not on your own place)"""
        user_id = get_jwt_identity()
        data = api.payload.copy()
        place_id = data.get('place_id')

        place = facade.get_place(place_id)
        if not place:
            abort(404, 'Place not found')
        if place.owner.id == user_id:
            abort(400, 'You cannot review your own place')
        for existing in facade.get_reviews_by_place(data['place_id']):
            if existing.user.id == user_id:
                abort(400, 'You have already reviewed this place')

        data['user_id'] = user_id
        review = facade.create_review(data)
        return review, 201


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Public: get a single review"""
        review = facade.get_review(review_id)
        if not review:
            abort(404, 'Review not found')
        return review, 200

    @jwt_required()
    @api.expect(review_update, validate=True)
    @api.marshal_with(review_model)
    @api.response(200, 'Review updated')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Authenticated: Update your own review"""
        user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            abort(404, 'Review not found')

        # Only owner or admin can update
        if not is_admin and review.user.id != user_id:
            abort(403, 'Unauthorized action')

        updated = facade.update_review(review_id, api.payload)
        return updated, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Authenticated: delete your own review (admin can delete any)"""
        user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            abort(404, 'Review not found')
        # Only owner or admin can delete
        if not is_admin and review.user.id != user_id:
            abort(403, 'Unauthorized action')

        if not facade.delete_review(review_id):
            abort(500, 'Could not delete review')
        return {'message': 'Review deleted successfully'}, 200
