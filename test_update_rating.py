import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Boundary values: 1 and 5 stars are saved, 0 and 6 are refused and leave the rating at 3 stars.
@pytest.mark.parametrize("stars, expected", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_at_the_boundaries(api, auth, rating, stars, expected):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected
    if expected == 200:
        assert res.json()["stars"] == stars
    else:
        assert res.json() == {"error": STARS_ERROR}
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    if expected == 200:
        assert res.json()["stars"] == stars
    else:
        assert res.json()["stars"] == 3
