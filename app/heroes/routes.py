from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from .forms import HeroForm
from app.models import Hero, User, db
from flask_login import current_user, login_required

heroes = Blueprint('heroes',__name__, static_folder='static', url_prefix='/heroes', template_folder='templates')


@heroes.route('/create', methods=['GET','POST'])
def create_hero():
    form = HeroForm()
    if request.method == 'POST':
        form_data = request.form.to_dict()
        new_hero = Hero(form_data)        
        try:
            db.session.add(new_hero)
            db.session.commit()
            flash(f'Hero added: {new_hero.name}', 'success')
        except:
            flash('Hero not added: Server Error','danger')
        return redirect(url_for('heroes.hero_detail',id=new_hero.id))
    return render_template('create_hero.html',form=form)

@heroes.route('/edit/<string:id>', methods=['GET','POST'])
def edit_hero(id):    
    print(id)
    hero = Hero.query.get(id)
    print(hero)
    hero_data=hero.to_dict()
    print(hero_data)
    form = HeroForm()
    if request.method == 'POST':
        form_hero = request.form.to_dict()
        # form_hero['owner'] = current_user.id 
        del form_hero['csrf_token']
        hero.update(form_hero)
        try:
            db.session.commit()
            flash(f'Hero added: {form_hero.name}', 'success')
        except:
            flash('Hero not added: Server Error','danger')
        return redirect(url_for('heroes.hero_detail',id=hero.id))
    return render_template('edit_hero.html',form=form,hero=hero)

@heroes.route('/')
@heroes.route('/browse', methods=['GET'])
def browse():
    heroes = Hero.query.filter(Hero.owner!=current_user.id).all()
    return render_template('browse.html', heroes=heroes)

@heroes.route('/myheroes', methods=['GET'])
@login_required
def my_heroes():
    if current_user:
        heroes = Hero.query.filter_by(owner=current_user.id).all()    
        return render_template('my_heroes.html', heroes=heroes)
    redirect(url_for('not_found_404'))

@heroes.route('/hero-detail/<string:id>', methods=['GET'])
@login_required
def hero_detail(id):    
    hero = Hero.query.get(id)
    owner = User.query.filter_by(id=hero.owner).first()
    if not hero and owner:
        return redirect(url_for('not_found_404'))
    return render_template('detail.html', hero=hero,owner=owner)

@heroes.route('/hero/delete/<string:id>', methods=['DELETE'])
def delete_hero(id):    
    db.session.delete(id)
    return render_template('my_heroes.html')