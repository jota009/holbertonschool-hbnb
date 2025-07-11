from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT token."""
        data = api.payload
        user = facade.get_user_by_email(data['email'])
        if not user or not user.verify_password(data['password']):
            return {'message': 'Invalid credentials'}, 401
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin})
        return {'access_token': access_token}, 200

@api.route('/protected')
class Protected(Resource):
    @jwt_required()
    def get(self):
        """Protected route that requires a valid JWT token."""
        user_id = get_jwt_identity()
        claims = get_jwt()
        return {
            'message': f'Hello, user {user_id}! Admin: {claims.get("is_admin")}'
            }, 200
