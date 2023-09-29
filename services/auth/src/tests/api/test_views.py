async def test_health_check(http_client):
    response = await http_client.get("/health-check")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
