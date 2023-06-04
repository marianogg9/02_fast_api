# Anime API

There is a big community and 2 new animee streaming websites are interested
to list animee information and help their users to choose their favorites.
They don't want to type manually those data and are interested in a pay monthly solution to use.

The goal of this project is to create an API providing information about japanese/chinese animee.
The API should be able to return responses for the following queries.
The data will be stored in a sqlite db.

0 - Import data via SQLAlchemy models into a sqlite db [X]

1 - List the first 100 animees sorted by [X]

2 - Get all details about "Death Note" [X]

3 - Add an animee not existing in the database [X]

4 - Update partially an animee [X]

5 - Update completely an animee [X]

6 - Delete an animee [X]

7 - Generate a token for a client [X]

8 - Only authenticated clients can interact with the API [X]

## Docs

To complete this project, a link to a documentation is expected to help any clients to interact with the API.

## Test

In order to test, that the API is responding accordingly.
You can use pytest. At least one test is expected for each request.

[Bonus] Create a collection of requests in Postman.

## References

[Video - Creator of FastAPI speaks about FastAPI](https://www.youtube.com/watch?v=37CcB2GBdlY)
[Video - Full course](https://www.youtube.com/watch?v=7t2alSnE2-I)
