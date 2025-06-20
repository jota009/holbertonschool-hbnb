import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_user_crud_flow(client):
    # CREATE
    rv = client.post(
        '/api/v1/users/',
        json={'first_name':'Bob','last_name':'Builder','email':'bob@build.com'}
    )
    assert rv.status_code == 201
    user = rv.get_json()
    assert 'id' in user
    user_id = user['id']

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

    # UPDATE
    rv = client.put(
        f'/api/v1/users/{user_id}',
        json={'first_name':'Robert','last_name':'Builder','email':'robert@build.com'}
    )
    assert rv.status_code == 200
    updated = rv.get_json()
    assert updated['first_name']=='Robert'
