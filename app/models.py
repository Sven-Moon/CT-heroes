from datetime import datetime
import secrets
from uuid import uuid4
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(40), primary_key=True)
    email = db.Column(db.String(100),nullable=True)
    username = db.Column(db.String(40), unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    token = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    character = db.relationship('Hero', backref='hero_owner',lazy=True)
    
    def __init__(self,username,email,password):
        self.id = str(uuid4())
        self.username = username
        self.email = email.lower()
        self.password = generate_password_hash(password)
        self.token = secrets.token_hex(32)
        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,   
            "date_created": self.date_created         
        }
    def get_token(self):
        return {"access-token":self.token}
        
class Hero(db.Model):
    id = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(200))
    comics_appeared_in = db.Column(db.Integer, default=0)
    super_power = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    owner = db.Column(db.String(60), db.ForeignKey("user.id"))
    image = db.Column(db.String(200), default="https://res.cloudinary.com/sventerprise/image/upload/e_improve,w_300,h_600,c_thumb,g_auto/v1653685149/CT-Random/Mystery-Hero_vydesf.png")
    
    def __init__(self,**kwargs) -> None:
        self.id = str(uuid.uuid4())
        for k in kwargs:
            setattr(self,k,kwargs[k])
        # self.name = d.get['name']
        # self.super_power = d.get['super_power']
        # self.comics_appeared_in = d.get['comics_appeared_in']
        # self.description = d.get['comics_appeared_in']
        # self.owner = d.get['owner']
        # self.image = d.get['image']
        
    def update(self,d):
        for k,v in d.items():
            getattr(self,k)
            setattr(self,k,v)
                  
    def to_dict(self):  
        return {k:v for k,v in vars(self).items() if k != '_sa_instance_state'}
    def init_from_form(self,d):
        for k,v in d:
            if self.__getattribute__(k):
                setattr(self,k,v)