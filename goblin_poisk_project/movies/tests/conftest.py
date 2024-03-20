import os

import pytest
from django.core.management import call_command
from django.db import connection

from movies.forms import MovieForm


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        current_dir = os.path.dirname(__file__)
        initial_data_path = os.path.join(current_dir, 'initial_data.json')
        call_command('loaddata', initial_data_path, verbosity=0)
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION pg_trgm;")
        yield


@pytest.fixture
def create_movie_form():
    form = MovieForm(data={
        'title': 'Test movie',
        'release_year': 2020,
        'director': 1,
        'description': 'Test description',
        'length': 120,
        'genres': [1],
        'original_rating': 5.0,
    })
    return form
