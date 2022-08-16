import pytest
import app

@pytest.fixture
def client():
    app_start = app.ClassApp().app_starter()
    with app_start as client:
        yield client