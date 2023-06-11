# Implementation

This is an API to list an Anime from local DB.

## Components
- Flask.
- SQLAlchemy.
- JWT support.
- Flassgger for Swagger docs.

## How to run
- Use a virtualenv
    ```bash
    python3.9 -m venv .venv
    ```
    (and activate it)
    ```bash
    source .venv/bin/activate
    ```

- Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

- Export variables
    ```bash
    export FLASK_SECRET_KEY=your_key
    export FLASK_APP=animes
    ```

- Run
    ```bash
    flask run
    ```

- See API documentation
    Access `localhost:5000/apidocs`.

## Resources
- [Real Python Flask JWT auth tutorial](https://realpython.com/token-based-authentication-with-flask/).
- [RESTful Auth with Flask](https://blog.miguelgrinberg.com/post/restful-authentication-with-flask).
- [Werkzeug Docs](https://werkzeug.palletsprojects.com/en/2.3.x/utils/).
- [Flask make_response method](https://tedboy.github.io/flask/generated/flask.make_response.html).
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/models/#defining-models).
- [Flasgger](https://github.com/flasgger/flasgger) docs.

## Changelog
- [1.3](https://github.com/marianogg9/flasking/commit/ac1b5eee6468e18c4e476dee36dcdb8ff270a6a8)
    - added tests.
    - updated documentation.

- [1.2](https://github.com/marianogg9/flasking/commit/7c0bbca6c2eaf6e4944c0a5e964dc5bc27cebe02)
    - added Swagger support.
    - refactored `login_required` decorator.
    - added `/logout` method.

- [1.1](https://github.com/marianogg9/flasking/commit/a73a18edddeaa90fc9bbe7cfae4b283da60b7894)
    
    - added JWT support.
    - added API documentation.

- [1.0](https://github.com/marianogg9/flasking/commit/0befc32708fec0c663d8d987803dec61ef661b60)
    
    - Basic authorization support.