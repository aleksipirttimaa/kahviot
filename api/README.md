# KahvIOT API

## Development environment

This project uses pipenv for dependency management.

Ensure you have python 3.9 and pip:

```sh
python --version
```

```sh
pip --version
```

Install `pipenv`:

```sh
pip install --user pipenv
```

Run following in this directory:

```sh
cd api/
```

Install the project dependencies:

```sh
pipenv install
```

Source the virtual environment:

```sh
pipenv shell
```

Use hug to run the development server:

```sh
hug -f main.py
```
