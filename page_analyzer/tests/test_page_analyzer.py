import pytest
from page_analyzer.app_handlers import app


@pytest.fixture()
def app_test():
    app.config.update({'TESTING': True})
    yield app


@pytest.fixture()
def client(app_test):
    return app.test_client()


def test_index(client):
    response = client.get("/")
    page = response.data.decode()
    assert '<title>Анализатор страниц</title>' in page
    assert '<a class= "navbar-brand text-white" ' \
           'href="/">Анализатор страниц</a>' in page
    assert '<a class="nav-link text-white-20" href="/urls">Сайты</a>' in page
    assert '<h1 class="display-3">Анализатор страниц</h1>' in page
    assert '<p class="lead">Бесплатно проверяйте сайты ' \
           'на SEO пригодность</p>' in page
