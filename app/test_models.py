import pytest
from .models import Hero, User

@pytest.fixture
def hero():
    d = {'name': 'name1',
     'description': 'description1',
     'comics_appeared_in': 1,
    'super_power': 'superpower1',
    'image': 'image1'}
    hero = Hero(d)
    return hero
@pytest.fixture
def hero_data():
    d = {'name': 'name1',
     'description': 'description1',
     'comics_appeared_in': 1,
    'super_power': 'superpower1',
    'image': 'image1'}
    hero = Hero(**d)
    return hero
    


def test_should_create_Hero(hero_data):
    hero = Hero(**hero_data)
    assert hero.name == 'name1'
    
def test_extra_data_doesnt_prevent_create_Hero(hero_data):
    hero_data['something_else'] = 3
    hero = Hero(**hero_data)
    hero.name == 'name1'