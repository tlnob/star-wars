from flask import Flask, render_template, request
import json
import requests
from mongoengine import connect
from characters import Character
from starships import Starships

app = Flask(__name__)

connect('star-wars-app')

def populate_db():
    for index in range(1,84):
        try:
            data = requests.get("https://swapi.dev/api/people/{index}/".format(index=index))
            if(data.status_code == 200):
                data = data.json()
                json.dumps(data)
                Character(
                    name=data["name"],
                    height=data["height"],
                    mass=data["mass"],
                    hair_color=data["hair_color"],
                    skin_color=data["skin_color"],
                    eye_color=data["eye_color"],
                    birth_year=data["birth_year"],
                    gender=data["gender"],
                    homeworld=data["homeworld"],
                    films=data["films"]
                ).save()
        except ConnectionAbortedError:
            print("Invalid id") 

@app.route('/st', methods=['GET'])
def populate_starship_db():
    for index in range(1,17):
        try:
            data = requests.get("https://swapi.dev/api/starships/{index}/".format(index=index))
            if(data.status_code == 200):
                data = data.json()
                json.dumps(data)
                print(data)
                try:
                    cost = float(data["cost_in_credits"])    
                except ValueError:
                    cost = 1
                Starships(
                    name=data["name"],
                    model=data["model"],
                    manufacturer=data["manufacturer"],
                    cost_in_credits=data["cost_in_credits"],
                    length=data["length"],
                    max_atmosphering_speed=data["max_atmosphering_speed"],
                    crew=data["crew"],
                    passengers=data["passengers"],
                    cargo_capacity=data["cargo_capacity"],
                    consumables=data["consumables"],
                    hyperdrive_rating=data["hyperdrive_rating"],
                    MGLT=data["MGLT"],
                    starship_class=data["starship_class"],
                    calc=round(float(data["hyperdrive_rating"]) / cost , 2) 
                ).save() 
        except ConnectionAbortedError: 
            print("Invalid id") 

@app.route('/starships', methods=['GET'])
def get_starships():
    if (len(Starships.objects) == 0):
        populate_starship_db()
    starships = Starships.objects.order_by('-score')
    return render_template('starships.html', starships=starships)

@app.route('/', methods=['GET', 'POST'])
def get_characters():
    if (len(Character.objects) == 0):
        populate_db()
        print("populating db...")
    if request.method == 'POST':
        key_type = request.form.get('type')
        value = request.form.get('filter')
        if key_type == "height":
            character = Character.objects(height=value).order_by('name', 'gender', 'mass', 'height')
        elif key_type == "name":
            character = Character.objects(name=value).order_by('name', 'gender', 'mass', 'height')
        elif key_type == "gender":
            character = Character.objects(gender=value).order_by('name', 'gender', 'mass', 'height')
        elif key_type == "mass":
            character = Character.objects(mass=value).order_by('name', 'gender', 'mass', 'height')
        return render_template('characters.html', character=character)

    character = Character.objects.order_by('name', 'gender', 'mass', 'height')
    return render_template('characters.html', character=character)

