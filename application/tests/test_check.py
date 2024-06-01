def test_home_page(client):
    response = client.get('/api/v1/check/')
    assert response.status_code == 200
    assert b'{"message":"> Api is alive! <"}\n' in response.data