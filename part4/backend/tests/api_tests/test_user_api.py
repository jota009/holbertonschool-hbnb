import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_user_crud_flow(client):
    # CREATE (now requires password & is_admin)
    rv = client.post(
        '/api/v1/users/',
        json={
            'first_name': 'Bob',
            'last_name': 'Builder',
            'email': 'bob@build.com',
            'password': 'BobPass123',
            'is_admin': False
        }
    )
    assert rv.status_code == 201
    user_id = rv.get_json()['id']

    # LIST
    rv = client.get('/api/v1/users/')
    assert rv.status_code == 200
    users = rv.get_json()
    assert any(u['id']==user_id for u in users)

    # GET by ID
    rv = client.get(f'/api/v1/users/{user_id}')
    assert rv.status_code == 200
    single = rv.get_json()
    assert single['email']=='bob@build.com'

    # UPDATE (jwtrequired; only first_name, last_name allowed)
    # -- log in to get a token
    rv = client.post('/api/v1/auth/login',
                    json={'email':'bob@build.com','password':'BobPass123'})
    assert rv.status_code == 200, "Login should succeed"
    token = rv.get_json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    rv = client.put(
        f'/api/v1/users/{user_id}',
        headers=headers,
        json={'first_name': 'Robert', 'last_name': 'Builder'}
    )
    assert rv.status_code == 200
    updated = rv.get_json()
    assert updated['first_name'] == 'Robert'

    # EMAIL CHANGE ATTEMPT → 400
    rv = client.put(
        f'/api/v1/users/{user_id}',
        headers=headers,
        json={'email': 'hacker@example.com'}
    )
    assert rv.status_code == 400
