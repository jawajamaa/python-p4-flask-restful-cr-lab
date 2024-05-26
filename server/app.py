#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    
    def get(self):
        response_dict = {
            "message": "Welcome to Plantsy"
        }

        return make_response(
            response_dict,
            200
        )
    
api.add_resource(Home, '/')

class Plants(Resource):
    
    def get(self):
        shrubberies = [shrub.to_dict() for shrub in Plant.query.all()]
        # shrubberies = []
        # for shrub in Plant.query.all():
        #     shrub.to_dict()
        #     shrubberies.append(shrub)

        return make_response( shrubberies, 200 )
    
    def post(self):
        data = request.get_json()

# lines 47-52 ChatGPT3.5 suggested validations with my alterations
        if data is None or not all(field in data for field in ["name", "image", "price"]):
            response_dict = {
            "message": "Invalid input - please try again",
            }
            return make_response( response_dict, 400 ) 
        
        new_plant = Plant(
            name = data["name"],
            image = data["image"],
            price = data["price"]
        )
       
        db.session.add(new_plant)
        db.session.commit()

        return make_response( new_plant.to_dict(), 201)
        
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    
    def get(self, id):
        response_dict = Plant.query.filter_by(id=id).first().to_dict()
        
        return make_response( response_dict, 200 ) 
    
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
