from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from .forms import DeleteHeroForm, HeroForm
from app.models import Hero, User, db
from flask_login import current_user, login_required

heroes = Blueprint('heroes',__name__, static_folder='static', url_prefix='/heroes', template_folder='templates')


@heroes.route('/create', methods=['GET','POST'])
@login_required
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

@heroes.route('/hero/<string:id>/edit', methods=['GET','POST'])
@login_required
def edit_hero(id):    
    hero = Hero.query.get(id)
    form = HeroForm()
    if request.method == 'POST':
        form_hero = request.form.to_dict()
        # form_hero['owner'] = current_user.id 
        del form_hero['csrf_token']
        hero.update(form_hero)
        try:
            db.session.commit()
            print('fine')
            flash(f'Hero successfully edited: {form.name.data}', 'success')
        except:
            flash(f'Hero NOT edited: Server Error {form.name.data}','danger')
        return redirect(url_for('heroes.hero_detail',id=hero.id))
    return render_template('edit_hero.html',form=form,hero=hero)

@heroes.route('/')
@heroes.route('/browse', methods=['GET'])
def browse():
    if not current_user.is_authenticated:
        heroes = Hero.query.all()
    else: 
        heroes = Hero.query.filter(Hero.owner!=current_user.id).all()
    return render_template('browse.html', heroes=heroes)

@heroes.route('/myheroes', methods=['GET'])
@login_required
def my_heroes():
    if current_user:
        heroes = Hero.query.filter_by(owner=current_user.id).all()    
        return render_template('my_heroes.html', heroes=heroes)
    redirect(url_for('not_found_404'))

@heroes.route('/hero/<string:id>/detail', methods=['GET'])
@login_required
def hero_detail(id):    
    hero = Hero.query.get(id)
    owner = User.query.filter_by(id=hero.owner).first()
    if not hero and owner:
        return redirect(url_for('not_found_404'))
    return render_template('detail.html', hero=hero,owner=owner)

@heroes.route('/hero/<string:id>/delete', methods=['GET','POST'])
@login_required
def delete_hero(id):
    hero = Hero.query.get(id)
    form = DeleteHeroForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            db.session.delete(hero)
            db.session.commit()
            flash('Hero has been deleted!', 'info')        
            return redirect(url_for('heroes.my_heroes'))
        else:
            flash('Hero NOT deleted.', 'info')    
    return render_template('delete_hero.html',hero=hero,form=form)