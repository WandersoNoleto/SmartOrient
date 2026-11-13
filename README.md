![apresentation-tip](https://github.com/WandersoNoleto/SmartOrient/blob/main/documentation/Doc-tip.png)

## SmartOrient [![NPM](https://img.shields.io/npm/l/react)](https://github.com/WandersoNoleto/SmartOrient/blob/main/LICENSE)


## About

SmartOrient is an open-source, web-based management solution for academic thesis guidance. The proposal is to bring together functionalities that encompass the entire process of managing guidance within a single platform, eliminating the need for multiple tools. The application caters to three types of users:
* Student - can view and register projects, attach files
* Advisor - can view projects they are a part of, accept participation requests, read attached files
* Coordination - responsible for overseeing all actions carried out by other parties

### :clipboard: Tecnologies and Tolls
* Python
* Django - Web framework
* PostgreSQL - SGBD
* [AdminLTE](https://github.com/ColorlibHQ/AdminLTE) - dashboard template based on Bootstrap 5
* [PDF.js](https://github.com/mozilla/pdf.js) - PDF Reader in JavaScript

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.



What things you need to install the software and how to install them

First, clone the repository
```
git clone https://github.com/WandersoNoleto/SmartOrient.git
```
Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and sync the dependencies (it creates the `.venv` with the right Python version)
```
uv sync
```
###### :key: Copy [.env.example](https://github.com/WandersoNoleto/SmartOrient/blob/main/.env.example) to `.env` (project root) and fill in `SECRET_KEY` and `DB_PASSWORD`.
Generate a new Django key and assign it to SECRET_KEY (in Python CLI)
```
from django.core.management import utils
print(utils.get_random_secret_key())
```
Or in a single command
```
uv run python -c "from django.core.management import utils; print(utils.get_random_secret_key())"
```

Start PostgreSQL (Docker) and apply the migrations
```
docker compose up -d
uv run python manage.py migrate
```

Use the command to run the service
```
uv run python manage.py runserver
```

### Development

Enable the git hooks (ruff lint + format and basic checks run on every commit)
```
uv run pre-commit install
```
Run the tests (requires the PostgreSQL container running) with coverage
```
uv run pytest --cov
```
Run the hooks manually on the whole project
```
uv run pre-commit run --all-files
```
