import pytest
from test.common import truncate_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_suite(request):
    print("TODO: Create and start docker image")


@pytest.fixture(autouse=True)
def cleanup_tests(request):
    print("Clearing db...")
    truncate_db()
