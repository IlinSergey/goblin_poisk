import os

import pytest
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        current_dir = os.path.dirname(__file__)
        initial_data_path = os.path.join(current_dir, 'initial_data.json')
        call_command('loaddata', initial_data_path, verbosity=0)
        yield
