
from flask import Blueprint, jsonify, request as r
from app.models import Hero, db
from .services import token_required


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/test', methods=['GET'])
def test():
    htest = Hero.query.all()[0]
    print(htest.to_dict())
    return jsonify({"result": htest.to_dict()}), 200

@api.route('/heroes', methods=['GET'])
def get_heroes():
    
    return jsonify([a.to_dict() for a in Hero.query.all()]), 200
    return jsonify({a.species: a.to_dict() for a in Hero.query.all()}), 200

@api.route('/hero/<string:name>', methods=['GET'])
def get_hero(name):
    
    hero = Hero.query.filter_by(name=name).first()
    print(hero)
    if Hero:
        return jsonify(hero.to_dict()),200
    return jsonify({'error': f'no such Hero exits: {name}'}), 404

@api.route('hero/create', methods=['POST'])
@token_required
def create_hero(new_hero):
    if new_hero:
        h = new_hero
    else:
        try:
            new_hero = r.get_json()
            h = Hero(**new_hero)
        except:
            return jsonify({'error': 'improper request or body data'}), 400
    try:
        db.session.add(h)
        db.session.commit()
    except:
        return jsonify({'error': 'Hero not added'})
    return jsonify({'created': new_hero}), 200

@api.route('/update/<string:id>', methods=['POST'])
@token_required
def update_hero(id):
    
    # possible errors: id wrong, data shape wrong
    try:
        new_hero = r.get_json()    
        hero = Hero.query.get(id)
        hero.update(new_hero)
        db.session.commit()
        hero = Hero.query.get(id)
        return jsonify({f'{hero.name.title()} updated': new_hero}),200
    except:
        return jsonify({'error':'Invalid request or Hero doesn\'t exist'})
    
@api.route('/delete/<string:id>', methods=['DELETE'])
@token_required
def delete_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error':f'Not found, id: {id}'}), 404
    db.session.delete(hero)
    db.session.commit()
    return jsonify({'Removed Hero':hero.to_dict()}), 200