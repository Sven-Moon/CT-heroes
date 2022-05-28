from flask import render_template, redirect, url_for
from app import app
import requests as r


@app.route('/')
@app.route('/home')
def home():
 
    return render_template('home.html')