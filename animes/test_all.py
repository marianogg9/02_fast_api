import pytest
from . import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

# TODO: Instead of calling the signup endpoint, i would create test data with sqlalchemy directly.
def signup(client):
    response = client.post("/signup",json={"email":"alguna@sarasa.com","password":"1234"})
    return response

def login(client):
    # TODO: Instead of calling signup first, i would create test data with sqlalchemy directly.
    #   This user could be defined in a fixture.
    signup(client)
    response = client.post("/login",json={"email":"alguna@sarasa.com","password":"1234"})
    return response

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_signup(client):

    response = signup(client)
    # TODO: Personal preference is to add empty line to divide the three blocks of a test,
    #  pre-requisite, function call and assertions
    assert response.status_code == 200

def test_login_no_signup(client):
    # TODO: Delete comment if uneeded
    # no signup first
    response = client.post("/login",json={"email":"alguna@sarasa.com"})
    assert response.status_code == 404
    assert response.json["message"] == "User does not exist."


# TODO: Is the name of this test correct?
#  i can see the word wrong so i would expect an error instead of a 201 http response (Created)
def test_login_wrong_body(client):
    signup(client)
    response = client.post("/login",json={"email":"alguna@sarasa.com"})
    assert response.status_code == 201


# TODO: Maybe we can look at the HTML content to also verify
#  that we are now redirected to a page accessible only for authenticated users.
#  I would create a user directly in a test db to test this feature
#  A unit test should only test one thing
def test_login(client):
    # signup first
    signup(client)
    response = login(client)
    assert response.status_code == 200

def test_all(client):
    # extract auth_token from login method
    # TODO: Could the header be part of a fixture as well, will make your code more readable
    #   Following the REST principles here instead of all, it should be /animes/
    response = client.get("/all",headers={"Authorization": login(client).json["auth_token"]})
    assert response.status_code == 200


# TODO: test_anime => test_get_anime_by_name
def test_anime(client):
    # TODO: Following the REST principles, the uri should be "/animes/<id>/ or /animes/death-note-rewrite/ using a slug
    response = client.get("/anime/Death Note Rewrite",headers={"Authorization": login(client).json["auth_token"]})
    assert response.status_code == 200
    assert response.json[0]["Members"] == 88699

# TODO: test_profile => test_get_profile
def test_profile(client):
    response = client.get("/profile",headers={"Authorization": login(client).json["auth_token"]})
    assert response.json["data"]["email"] == "alguna@sarasa.com"


# TODO: test_all_not_authorized => test_return_error_for_invalid_credentials
def test_all_not_authorized(client):
    # no auth_token
    response = client.get("/all")
    assert response.status_code == 401


# TODO: test_all_wrong_method => test_return_error_for_invalid_method
def test_all_wrong_method(client):
    response = client.post("/all",headers={"Authorization": login(client).json["auth_token"]})
    assert response.status_code == 405


# TODO: No need for logout since the token will expire
def test_logout(client):
    login(client)
    response = client.post("/logout",headers={"Authorization": login(client).json["auth_token"]})
    assert response.status_code == 200
    assert response.json["message"] == "Successfully logged out."