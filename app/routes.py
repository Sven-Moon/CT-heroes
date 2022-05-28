from flask import render_template, redirect, url_for
from app import app
import requests as r


@app.route('/')
@app.route('/home')
def home():
 
    return render_template('home.html')
    
@app.route('/404', methods=['GET'])
def not_found_404():    
    return render_template('404.html')