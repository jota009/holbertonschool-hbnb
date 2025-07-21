import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_review_crud_flow(client):
    # 1) Create & log in the OWNER (password + JWT)
    rv = client.post('/api/v1/users/', json={
        'first_name':'Owner',
        'last_name':'User',
        'email':'owner@example.com',
        'password':'OwnerPass123',
        'is_admin': False
    })
    assert rv.status_code == 201
    owner_id = rv.get_json()['id']

    rv = client.post('/api/v1/auth/login', json={
        'email':'owner@example.com',
        'password':'OwnerPass123'
    })
    assert rv.status_code == 200
    owner_token = rv.get_json()['access_token']
    owner_headers = {'Authorization': f'Bearer {owner_token}'}

    # 2) Create an Amenity
    rv = client.post('/api/v1/amenities/', json={'name':'Pool'})
    assert rv.status_code == 201
    amenity_id = rv.get_json()['id']

    # 3) Owner creates the Place
    place_payload = {
        'title':'Lake House','description':'Chill','price':200.0,
        'latitude':45.0,'longitude':-75.0,
        'amenities':[amenity_id]
    }
    rv = client.post('/api/v1/places/',
                     headers=owner_headers,
                     json=place_payload)
    assert rv.status_code == 201
    place_id = rv.get_json()['id']

    # ——————————————————————————————————————————————————————————
    # **NEW**: 4) OWNER attempts to review their own place → should 400
    rv = client.post('/api/v1/reviews/',
                     headers=owner_headers,
                     json={'text':'My Review','rating':5,'place_id':place_id})
    assert rv.status_code == 400
    # ——————————————————————————————————————————————————————————

    # **NEW**: 5) Create & log in a SECOND “Reviewer” user
    rv = client.post('/api/v1/users/', json={
        'first_name':'Reviewer',
        'last_name':'User',
        'email':'rev@example.com',
        'password':'RevPass123',
        'is_admin': False
    })
    assert rv.status_code == 201
    reviewer_id = rv.get_json()['id']

    rv = client.post('/api/v1/auth/login', json={
        'email':'rev@example.com',
        'password':'RevPass123'
    })
    assert rv.status_code == 200
    reviewer_token = rv.get_json()['access_token']
    reviewer_headers = {'Authorization': f'Bearer {reviewer_token}'}
    # ——————————————————————————————————————————————————————————

    # 6) CREATE Review (by reviewer) → 201
    rev_payload = {'text':'Amazing stay','rating':5,'place_id':place_id}
    rv = client.post('/api/v1/reviews/',
                     headers=reviewer_headers,
                     json=rev_payload)
    assert rv.status_code == 201
    review = rv.get_json()
    rid = review['id']
    assert review['text']=='Amazing stay'
    assert review['rating']==5

    # 7) LIST ALL Reviews → 200
    rv = client.get('/api/v1/reviews/')
    assert rv.status_code == 200
    assert any(r['id']==rid for r in rv.get_json())

    # 8) GET by ID → 200
    rv = client.get(f'/api/v1/reviews/{rid}')
    assert rv.status_code == 200
    assert rv.get_json()['id']==rid

    # 9) UPDATE (by reviewer) → 200
    rv = client.put(f'/api/v1/reviews/{rid}',
                    headers=reviewer_headers,
                    json={'text':'Pretty good','rating':4})
    assert rv.status_code == 200
    assert rv.get_json()['rating']==4

    # 🔟 DELETE (by reviewer) → 200
    rv = client.delete(f'/api/v1/reviews/{rid}',
                       headers=reviewer_headers)
    assert rv.status_code == 200

    # 11) GET Deleted → 404
    rv = client.get(f'/api/v1/reviews/{rid}')
    assert rv.status_code == 404

    # 12) LIST Reviews for a Place → 200
    client.post('/api/v1/reviews/',
                headers=reviewer_headers,
                json=rev_payload)
    rv = client.get(f'/api/v1/places/{place_id}/reviews')
    assert rv.status_code == 200
    arr = rv.get_json()
    assert isinstance(arr, list) and len(arr) >= 1
