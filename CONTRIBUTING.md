# Contributing to Django Flag App

There are many ways to contribute to the project. You may improve the documentation, address a bug, add some feature to the code or do something else. All sort of contributions are welcome.


### Development

To start development on this project, fork this repository and follow the following instructions.

```bash
# clone the forked repository
$ git clone YOUR_FORKED_REPO_URL

# create a virtual environment
$ python3 -m venv venv
# activate the virtual environment
$ source venv/bin/activate
# install dependencies in development mode
(venv) $ pip install -e . -r testapp/requirements.txt

# start the development server
(venv) $ python manage.py runserver
```

### Testing

To run tests against a particular `python` and `django` version installed inside your virtual environment, you may use:

```bash
(venv) $ pytest # `python manage.py test` or `make test` also work

```

To run tests against all supported `python` and `django` versions, you may run:

```bash
# install dependency
(venv) $ pip install tox
# run tests
(venv) $ tox
```
