from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from .extensions import bcrypt, jwt, db
from config import DevelopmentConfig


def create_app(config_class=None):
    config_class = config_class or DevelopmentConfig

    app = Flask(__name__)
    CORS(app,
         resources={r"/api/.*": {"origins": "*"}},
         supports_credentials=True,
         methods=["GET","POST","PUT","DELETE","OPTIONS"])
    app.config.from_object(config_class)

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Register your namespaces
    from app.api.v1.auth       import api as auth_ns
    from app.api.v1.users      import api as users_ns
    from app.api.v1.amenities  import api as amenities_ns
    from app.api.v1.places     import api as places_ns
    from app.api.v1.reviews    import api as reviews_ns

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        strict_slashes=False
    )

    api.add_namespace(auth_ns,      path='/api/v1/auth')
    api.add_namespace(users_ns,     path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns,    path='/api/v1/places')
    api.add_namespace(reviews_ns,   path='/api/v1/reviews')

    # ─── Add a Flask‐CLI command to seed the DB ────────────────
    @app.cli.command('seed')
    def seed_command():
        """Seed the database with initial data."""
        # your existing seed.py needs a run_seed() function
        from scripts.seed import run_seed
        run_seed()
        print("✅ Database seeded!")

    return app
