from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from encoder import MyEncoder

app = Flask(__name__)
app.json_encoder = MyEncoder

app.config["MONGO_URI"] = "mongodb://192.168.0.50:27017/todos"
mongodb_client = PyMongo(app)
db = mongodb_client.db
doc = db.todos

@app.route('/')
def get():
    todos = doc.find()
    return jsonify([todo for todo in todos])

@app.route("/<int:todoId>", methods=["GET"])
def get_one(todoId):
	todo = doc.find_one({"_id": todoId})
	return todo

@app.route("/create", methods=["POST"])
def create():
    input_json = request.get_json(force=True)
    doc.insert_one({'_id': input_json['id'],'title': input_json['title'], 'body': input_json['body']})
    return jsonify(message="success")

@app.route("/update/<int:todoId>", methods=["PUT"])
def update(todoId):
	input_json = request.get_json(force=True)
	db.todos.find_one_and_update(
		{'_id': todoId}, {"$set": {'title': input_json['title'], 'body': input_json['body']}}
	)
	return jsonify(message="success")

@app.route("/delete/<int:todoId>", methods=['DELETE'])
def delete(todoId):
	db.todos.delete_one({'_id': todoId})
	return jsonify(message="success")
	