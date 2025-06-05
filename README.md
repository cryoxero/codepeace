# CodePeace

A pretty barebones codewars/leetcode clone powered by django

## setup

Go to the project base directory

```bash
git clone git@github.com:cryoxero/codepeace.git
cd codepeace
```

Get the dependencies ready

```bash
poetry install
```

Create the code interpreters

```bash
chmod +x ready_images.sh
./ready_images.sh
```

Create admin account and run the project

```bash
poetry run python src/manage.py createsuperuser
poetry run python src/manage.py runserver
```
