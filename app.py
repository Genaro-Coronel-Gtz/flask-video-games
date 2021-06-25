from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps
import code

app = Flask(__name__)

app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.Integer)
  name = db.Column(db.String(50))
  password = db.Column(db.String(50))
  admin = db.Column(db.Boolean)


class Company(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  country = db.Column(db.String(50), nullable=False)
  games = db.relationship('Games', backref='company', lazy=True)


class Games(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  genre = db.Column(db.String(20), nullable=False)
  price = db.Column(db.Float, nullable=False)
  company_id = db.Column(db.Integer, db.ForeignKey(
      'company.id'), nullable=False)


def token_required(f):
  @wraps(f)
  def decorator(*args, **kwargs):
      token = None

      if 'x-access-tokens' in request.headers:
          token = request.headers['x-access-tokens']

      if not token:
          return jsonify({'message': 'a valid token is missing'})

      try:
          data = jwt.decode(
              token, app.config['SECRET_KEY'], algorithms=["HS256"])
          current_user = Users.query.filter_by(
              public_id=data['public_id']).first()
      except:
          return jsonify({'message': 'token is invalid'})

      return f(current_user, *args,  **kwargs)
  return decorator


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
  data = request.get_json()

  hashed_password = generate_password_hash(data['password'], method='sha256')

  new_user = Users(public_id=str(uuid.uuid4()),
                   name=data['name'], password=hashed_password, admin=False)
  db.session.add(new_user)
  db.session.commit()

  return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():

  auth = request.authorization

  if not auth or not auth.username or not auth.password:
      return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

  user = Users.query.filter_by(name=auth.username).first()

  if check_password_hash(user.password, auth.password):
      token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow(
      ) + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
      return jsonify({'token': token})

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/user', methods=['GET'])
def get_all_users():

  users = Users.query.all()

  result = []

  for user in users:
      user_data = {}
      user_data['public_id'] = user.public_id
      user_data['name'] = user.name
      #user_data['password'] = user.password
      user_data['admin'] = user.admin

      result.append(user_data)

  return jsonify({'users': result})


@app.route('/games', methods=['GET'])
@token_required
def get_games(current_user):

  games = Games.query.all()
  #code.interact(local=dict(globals(), **locals()))

  output = []

  for game in games:
      game_data = {}
      game_data['id'] = game.id
      game_data['name'] = game.name
      game_data['genre'] = game.genre
      game_data['price'] = game.price
      game_data['company'] = game.company.name
      output.append(game_data)
  return jsonify({'list_of_games': output})


@app.route('/companies', methods=['GET'])
@token_required
def get_companies(current_user):

  companies = Company.query.all()

  output = []

  for company in companies:
      company_data = {}
      company_data['id'] = company.id
      company_data['name'] = company.name
      company_data['country'] = company.country
      output.append(company_data)
  return jsonify({'list_of_companies': output})



@app.route('/create-game', methods=['POST'])
@token_required
def create_game(current_user):
  data = request.get_json()

  new_games = Games(name=data['name'], 
                    price=data['price'],
                    genre=data['genre'], 
                    company_id=1)
  db.session.add(new_games)
  db.session.commit()

  return jsonify({'message': 'new game created'})


@app.route('/create-company', methods=['POST'])
@token_required
def create_company(current_user):
  data = request.get_json()

  new_company = Company(name=data['name'], country=data['country'])
  db.session.add(new_company)
  db.session.commit()

  return jsonify({'message': 'new company created'})


@app.route('/authors/<name>', methods=['DELETE'])
@token_required
def delete_author(current_user, name):
  author = Authors.query.filter_by(
      name=name, user_id=current_user.id).first()
  if not author:
      return jsonify({'message': 'author does not exist'})

  db.session.delete(author)
  db.session.commit()

  return jsonify({'message': 'Author deleted'})


@app.route('/game/<id>', methods=['DELETE'])
@token_required
def delete_game(current_user, id):
  game = Games.query.filter_by(id=id).first()
  if not game:
      return jsonify({'message': 'game does not exist'})

  db.session.delete(game)
  db.session.commit()

  return jsonify({'message': 'Game deleted'})


if __name__ == '__main__':
    app.run(debug=True)
