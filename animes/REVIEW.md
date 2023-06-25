# Anime API Full review

animes/test_all.py

[ ] I would create a new folder called tests and inside i would rename test_all to test_views

[ ] Since you use pytest you can put the fixture in another file called conftest

[ ] You can use the library black to clean the style automatically of your code

[ ] Rename your test by using a verb after test_ to explain what the test is doing. For example, `test_profile` will become `test_get_profile`

[ ] Remove comments if unused in your project

[ ] Simplify requirements.txt file, displaying only the most important

[ ] You can use the Sphinx format for docstrings https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html

[ ] I would potentially create a folder called views and inside user containing view related to signup, login etc and anime for views specific to anime

[ ] Use flask shortcut for response with tuple instead of using make response https://flask.palletsprojects.com/en/2.3.x/quickstart/#about-responses

return {"bla": "blabla"}, 200

[ ] For 404 error, you could a 404 error handler like in this example
https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json

[ ] I think there is rooms to simplify your views by removing unneeded nested conditions in views