#!/usr/bin/env python3
from app import create_app, db


if __name__ == '__main__':
    app = create_app()

    # reset and recreate all tables so smoke_tests can be re-run
    with app.app_context():
        db.drop_all()
        db.create_all()
    # serve on 0.0.0.0:5000, disable the extra reloader process
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
