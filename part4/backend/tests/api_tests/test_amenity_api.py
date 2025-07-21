import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_amenity_crud_flow(client):
    # CREATE
    rv = client.post(
        '/api/v1/amenities/',
        json={'name':'Pool'}
    )
    assert rv.status_code == 201
    amenity = rv.get_json()
    assert 'id' in amenity and amenity['name']=='Pool'
    amenity_id = amenity['id']

    # LIST
    rv = client.get('/api/v1/amenities/')
    assert rv.status_code == 200
    all_amenities = rv.get_json()
    assert any(a['id']==amenity_id for a in all_amenities)

    # GET by ID
    rv = client.get(f'/api/v1/amenities/{amenity_id}')
    assert rv.status_code == 200
    single = rv.get_json()
    assert single['name']=='Pool'

    # UPDATE
    rv = client.put(
        f'/api/v1/amenities/{amenity_id}',
        json={'name':'Hot Tub'}
    )
    assert rv.status_code == 200
    updated = rv.get_json()
    assert updated['name']=='Hot Tub'
