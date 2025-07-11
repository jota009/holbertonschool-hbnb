from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

# Define the namespace
api = Namespace('users', description='User operations')

# Define the Data-transfer object for input & docs
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User UUID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'is_admin': fields.Boolean(required=True, description='Admin flag')
})

user_input = api.model('UserInput', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Valid email of the user'),
    'password': fields.String(required=True, description='Plaintext password', min_length=6),
    'is_admin': fields.Boolean(default=False, description='Admin flag')
})

user_update = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

user_admin_update = api.model('UserAdminUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Valid email'),
    'password': fields.String(description='Plaintext password', min_length=6),
    'is_admin': fields.Boolean(description='Admin flag')
})


# List & Create: /api/v1/users/
@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)  # serializes output to match user_model
    def get(self):
        """List all users (public)"""
        return facade.get_all_users(), 200

    @jwt_required(optional=True)
    @api.expect(user_input, validate=True)
    @api.marshal_list_with(user_model, code=201)
    @api.response(400, 'Email already registered or invalid data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """
        Public: Register a new user.
        If you try to set is_admin=True, you must supply a valid admin JWT—
        except if you are the *very first* user in the system.
        """
        data = api.payload.copy()
        want_admin   = data.get('is_admin', False)
        users        = facade.get_all_users()
        admin_exists = any(u.is_admin for u in users)

        if want_admin:
            # after the very first admin, require an existing admin's token
            if admin_exists:
                claims = get_jwt()
                if not claims.get('is_admin', False):
                    abort(403, 'Admin privileges required to create admin accounts')
        else:
            data['is_admin'] = False

        # enforce unique email
        if facade.get_user_by_email(data['email']):
            abort(400, 'Email already registered')

        user = facade.create_user(data)
        return user, 201


# Retrieve & Update: /api/v1/users/<user_id>
@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID (public)"""
        user = facade.get_user(user_id)
        if not user:
            abort(404, 'User not found')
        return user, 200

    @jwt_required()
    @api.expect(user_admin_update, validate=True)
    @api.marshal_with(user_model)
    @api.response(403, 'Unauthorized action or admin privileges required')
    @api.response(400, 'Invalid data or email conflict')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update user details.
        - Admins may change any field (email, password, is_admin).
        - Regular users may only change their own first_name and last_name.
        """
        current_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        data = api.payload.copy()

            # If non-admin and trying to change email or password, reject.
        if not is_admin and any(field in data for field in ('email', 'password', 'is_admin')):
            abort(400, 'Cannot modify email or password or admin flag')

        # Ensure only admin can update others
        if not is_admin and current_id != user_id:
            abort(403, 'Unauthorized action')

        # Admin path: full update (with uniqueness checks)
        if is_admin:
            if 'email' in data:
                existing = facade.get_user_by_email(data['email'])
                if existing and existing.id != user_id:
                    abort(400, 'Email already registered to another user')
            if 'password' in data:
                user = facade.get_user(user_id)
                if not user:
                    abort(404, 'User not found')
                user.hash_password(data.pop('password'))
            updated = facade.update_user(user_id, data)
            if not updated:
                abort(404, 'User not found')
            return updated, 200

        # Self-service path: only name fields
        allowed = {'first_name', 'last_name'}
        filtered = {k: v for k, v in data.items() if k in allowed}
        updated = facade.update_user(user_id, filtered)
        if not updated:
            abort(404, 'User not found')
        return updated, 200
