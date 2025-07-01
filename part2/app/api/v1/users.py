from flask_restx import Namespace, Resource, fields
from app.services import facade

# Define the namespace
api = Namespace('users', description='User operations')

# Define the Data-transfer object for input & docs
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User UUID'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_input = api.model('UserInput', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Valid email of the user'),
    'password': fields.String(required=True, description='Plaintext password', min_length=6),
    'is_admin': fields.Boolean(default=False, description='Admin flag')
})


# List & Create: /api/v1/users/
@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)  # serializes output to match user_model
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        # Returns a list of User objects; flask-restx will serialize fields
        return users, 200

    @api.expect(user_input, validate=True)
    @api.marshal_with(user_model, code=201)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid data')
    # NEXT TO DO: Edit post method to handle password hashing
    def post(self):
        """Register a new user"""
        data = api.payload
        # Checks uniqueness
        if facade.get_user_by_email(data['email']):
            api.abort(400, 'Email already registered')
        # Delegate to facade
        user = facade.create_user(data)
        # Returns only specific fields
        return user, 201


# Retrieve & Update: /api/v1/users/<user_id>
@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    @api.response(200, 'User details retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user, 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    @api.response(200, 'User updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid data or email conflict')
    def put(self, user_id):
        """Update an existing user"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')

        data = api.payload
        # Prevent email conflict on update
        existing = facade.get_user_by_email(data['email'])
        if existing and existing.id != user_id:
            api.abort(400, 'Email already registered to another user')

        # Delegate the update
        updated = facade.update_user(user_id, data)
        return updated, 200
