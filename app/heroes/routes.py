from flask import Blueprint, jsonify, render_template, url_for
from .forms import HeroForm
from app.models import Hero, db
import requests as r
from flask_login import current_user, login_required

heroes = Blueprint('heroes',__name__, static_folder='static', url_prefix='/heroes', template_folder='templates')


@heroes.route('/create', methods=['GET','POST'])
def create_hero():
    form = HeroForm()
    return render_template('create_hero.html',form=form)

@heroes.route('/browse', methods=['GET'])
def browse():
    heroes = Hero.query.filter_by(owner=current_user.id).all()
    return render_template('browse.html', heroes)

@heroes.route('/myheroes', methods=['GET'])
@login_required
def my_heroes():
    if current_user:
        heroes = Hero.query.filter_by(owner=current_user.id).all()
    return render_template('my_heroes.html', heroes=heroes)