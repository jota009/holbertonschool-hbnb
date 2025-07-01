from flask_restx import Namespace, Resource, fields, abort
from app.services import facade


api = Namespace('reviews', description='Review operations')

# Input model for POST & PUT
review_input = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User UUID'),
    'place_id': fields.String(required=True, description='Place UUID')
})

# Output model for listing & detail
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='Review UUID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(attribute='user.id', description='User UUID'),
    'place_id': fields.String(attribute='place.id', description='Place UUID')
})

# Partial‐update schema: no field is required
review_update = api.model('ReviewUpdate', {
    'text':     fields.String(description='Review text'),
    'rating':   fields.Integer(description='Rating (1–5)'),
    'user_id':  fields.String(description='User UUID'),
    'place_id': fields.String(description='Place UUID')
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """Retrieves a list of all reviews"""
        return facade.get_all_reviews(), 200

    @api.expect(review_input, validate=True)
    @api.marshal_list_with(review_model, code=201)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            rev = facade.create_review(api.payload)
            return rev, 201
        except ValueError as e:
            abort(400, str(e))

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get review details by ID"""
        rev = facade.get_review(review_id)
        if not rev:
            abort(404, 'Review not found')
        return rev, 200

    @api.expect(review_update, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update a review's information"""
        try:
            updated = facade.update_review(review_id, api.payload)
            if not updated:
                abort(404, 'Review not found')
            return updated, 200
        except ValueError as e:
            abort(400, str(e))

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            abort(404, 'Review not found')
        return {'message': 'Review deleted successfully'}, 200
