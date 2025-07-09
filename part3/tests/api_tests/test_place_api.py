import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_place_crud_flow(client):
    # 1️⃣ Create & login a User (with password)
    rv = client.post(
        '/api/v1/users/',
        json={
            'first_name': 'Tester',
            'last_name': 'User',
            'email': 'tester@example.com',
            'password': 'Test1234',
            'is_admin': False
        }
    )
    assert rv.status_code == 201
    user_id = rv.get_json()['id']

    # 1️⃣a) Login the User to get JWT token
    rv = client.post(
        '/api/v1/auth/login',
        json={'email': 'tester@example.com', 'password': 'Test1234'}
    )
    assert rv.status_code == 200
    token = rv.get_json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # 2️⃣ Create an Amenity prerequisite
    rv = client.post(
        '/api/v1/amenities/',
        json={'name':'Pool'}
    )
    assert rv.status_code == 201
    amenity = rv.get_json()
    amenity_id = amenity['id']

    # 3️⃣ CREATE a Place
    place_data = {
        'title':       'Cozy Cottage',
        'description': 'A quiet getaway',
        'price':       120.0,
        'latitude':    45.0,
        'longitude':   -73.0,
        # 'owner_id':    user_id,
        'amenities':   [amenity_id]
    }
    rv = client.post('/api/v1/places/', headers=headers, json=place_data)
    assert rv.status_code == 201
    place = rv.get_json()
    assert place['title'] == 'Cozy Cottage'
    assert place['owner']['id'] == user_id
    assert any(a['id'] == amenity_id for a in place['amenities'])
    place_id = place['id']

    # 4️⃣ LIST all Places
    rv = client.get('/api/v1/places/')
    assert rv.status_code == 200
    all_places = rv.get_json()
    assert any(p['id'] == place_id for p in all_places)

    # 5️⃣ GET Place by ID
    rv = client.get(f'/api/v1/places/{place_id}')
    assert rv.status_code == 200
    single = rv.get_json()
    assert single['id'] == place_id
    assert single['owner']['email'] == 'tester@example.com'

    # 6️⃣ UPDATE the Place
    rv = client.put(
        f'/api/v1/places/{place_id}',
        headers=headers,
        json={'price': 150.0}
    )
    assert rv.status_code == 200
    updated = rv.get_json()
    assert updated['price'] == 150.0

    # 7️⃣ 404 on missing Place
    rv = client.get('/api/v1/places/non-existent-id')
    assert rv.status_code == 404
