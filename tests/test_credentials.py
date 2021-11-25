from credentials import MyCredentials

def test_caching():
    assert MyCredentials.creds is None
    MyCredentials.load_from_file()
    assert MyCredentials.creds is not None

def test_loading_of_creds():
    creds = MyCredentials.load_from_file()
    assert "url" in creds.keys()
    assert "http" in creds["url"]
