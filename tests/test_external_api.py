import app as app_module

def test_barcode_search_success(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {
                "status": 1,
                "product": {
                    "product_name": "Nutella",
                    "brands": "Ferrero",
                    "ingredients_text": "Sugar and hazelnuts"
                }
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(app_module.requests, "get", fake_get)

    result = app_module.search_openfoodfacts("3017620422003")
    assert result["name"] == "Nutella"
    assert result["brand"] == "Ferrero"
    assert result["barcode"] == "3017620422003"

def test_barcode_search_not_found(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"status": 0}
    monkeypatch.setattr(
        app_module.requests,
        "get",
        lambda *args, **kwargs: FakeResponse()
    )
    result = app_module.search_openfoodfacts("0000000000000")
    assert result is None

def test_barcode_search_api_error(monkeypatch):
    import requests
    def fake_get(*args, **kwargs):
        raise requests.RequestException("API unavailable")
    monkeypatch.setattr(app_module.requests, "get", fake_get)
    result = app_module.search_openfoodfacts("3017620422003")
    assert result is None
