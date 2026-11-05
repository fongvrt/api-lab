# Another user cannot read the rating, and the owner still reads it unchanged.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    assert 400 <= res.status_code <= 499
    assert "error" in res.json()
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# Another user cannot change the stars of the rating, and the owner still reads it unchanged.
def test_other_user_cannot_change_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 1}, headers=other_auth)
    assert 400 <= res.status_code <= 499
    assert "error" in res.json()
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# Another user cannot delete the rating, and the owner still reads it unchanged.
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    assert 400 <= res.status_code <= 499
    assert "error" in res.json()
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json() == rating
