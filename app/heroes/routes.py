from flask import Blueprint, jsonify, render_template
from app.models import Hero, db
import requests as r

heroes = Blueprint('heroes',__name__, static_folder='static', static_url_path='/heroes')

@heroes.route('/home', methods=['GET'])
def home():
    
    return render_template('heroes.home.html')

@heroes.route('/create', methods=['GET','POST'])
def create_hero():
    
    return render_template('create_hero.html')