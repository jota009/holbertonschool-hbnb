import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_review_crud_flow(client):
    # 1) Create a User
    rv = client.post('/api/v1/users/',
                     json={'first_name':'T','last_name':'ester','email':'t@example.com'})
    assert rv.status_code == 201
    user_id = rv.get_json()['id']

    # 2) Create an Amenity
    rv = client.post('/api/v1/amenities/', json={'name':'Pool'})
    assert rv.status_code == 201
    amenity_id = rv.get_json()['id']

    # 3) Create a Place
    place_payload = {
        'title':'Lake House','description':'Chill','price':200.0,
        'latitude':45.0,'longitude':-75.0,
        'owner_id':user_id, 'amenities':[amenity_id]
    }
    rv = client.post('/api/v1/places/', json=place_payload)
    assert rv.status_code == 201
    place_id = rv.get_json()['id']

    # 4️⃣ CREATE Review
    rev_payload = {
        'text':'Amazing stay','rating':5,
        'user_id':user_id, 'place_id':place_id
    }
    rv = client.post('/api/v1/reviews/', json=rev_payload)
    assert rv.status_code == 201
    review = rv.get_json()
    rid = review['id']
    assert review['text']=='Amazing stay'
    assert review['rating']==5

    # 5️⃣ LIST ALL Reviews
    rv = client.get('/api/v1/reviews/')
    assert rv.status_code == 200
    assert any(r['id']==rid for r in rv.get_json())

    # 6️⃣ GET by ID
    rv = client.get(f'/api/v1/reviews/{rid}')
    assert rv.status_code == 200
    assert rv.get_json()['id']==rid

    # 7️⃣ UPDATE
    rv = client.put(f'/api/v1/reviews/{rid}',
                    json={'text':'Pretty good','rating':4,
                          'user_id':user_id,'place_id':place_id})
    assert rv.status_code == 200
    assert rv.get_json()['rating']==4

    # 8️⃣ DELETE
    rv = client.delete(f'/api/v1/reviews/{rid}')
    assert rv.status_code == 200

    # 9️⃣ GET Deleted → 404
    rv = client.get(f'/api/v1/reviews/{rid}')
    assert rv.status_code == 404

    # 🔟 LIST Reviews for a Place
    # recreate one
    client.post('/api/v1/reviews/', json=rev_payload)
    rv = client.get(f'/api/v1/places/{place_id}/reviews')
    assert rv.status_code == 200
    arr = rv.get_json()
    assert isinstance(arr, list) and len(arr) >= 1
