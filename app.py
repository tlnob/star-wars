from flask import Flask, render_template, request
import json
from mongoengine import connect
import requests
from models import *

app = Flask(__name__)

def init_db():
    connection = connect('star-wars-app')
    return connection

def paginate(page_num):
    print(page_num.isdigit())
    page_num = int(page_num)
    skips = 10 * (int(page_num) - 1)

    cursor = Character.objects.order_by('name', 'gender', 'mass', 'height').skip(skips).limit(10)
    return [x for x in cursor]

def populate_planets_db(planets):
    try:
        data = requests.get(planets)
        if(data.status_code == 200):
            data = data.json()
            json.dumps(data)
            Planets.objects(name=data["name"]).update_one(
                name=data["name"],
                url=data["url"],
                upsert=True
            )
    except ConnectionAbortedError:
        print("Invalid id")
    return Planets.get_all()


def populate_vehicles_db(vehicles):
    try:
        for vehicle in vehicles:
            data = requests.get(vehicle)
            if(data.status_code == 200):
                data = data.json()
                json.dumps(data)
                Vehicles.objects(name=data["name"]).update_one(
                   url=data["url"],
                   upsert=True
                )

    except ConnectionAbortedError:
        print("Invalid id")
    return Vehicles.get_all()

def populate_db():
    try:
        meta_data = requests.get("https://swapi.dev/api/people/").json()
        total = meta_data["count"]
        for index in range(1,total):
            data = requests.get("https://swapi.dev/api/people/{index}/".format(index=index))
            if(data.status_code == 200):
                data = data.json()
                json.dumps(data)
                populate_starship_db(data["starships"])
                populate_vehicles_db(data["vehicles"])
                populate_films_db(data["films"])
                populate_planets_db(data["homeworld"])
                Character.add(
                    data["name"],
                    data["height"],
                    data["mass"],
                    data["birth_year"],
                    data["gender"],
                    data["url"],
                    data["films"],
                    data["starships"],
                    data["vehicles"],
                    data["homeworld"]
                )
    except ConnectionAbortedError:
        print("Invalid id") 

def populate_films_db(films):
    try:
        for film in films:
            data = requests.get(film)
            if(data.status_code == 200):
                data = data.json()
                json.dumps(data)
                Films.objects(episode_id=data["episode_id"]).update_one(
                    title=data["title"],
                    url=data["url"],
                    upsert=True
                )
    except ConnectionAbortedError: 
        print("Invalid id")   

def populate_starship_db(starships):
    try:
        for starship in starships:
            data = requests.get(starship)
            if(data.status_code == 200):
                data = data.json()
                json.dumps(data)
                try:
                    cost = float(data["cost_in_credits"])    
                    calc = float(data["hyperdrive_rating"]) / cost
                except ValueError:
                    calc = 0
                Starships.objects(name=data["name"]).update_one(
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
                    calc= calc,
                    url=data["url"],
                    upsert=True
                )
    except ConnectionAbortedError: 
        print("Invalid id") 

@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.objects.order_by('-calc')
    return render_template('starships.html', starships=starships)

@app.route('/db', methods=['GET'])
def db():
    populate_db()
    return Character.objects.to_json()

@app.route('/<page>', methods=['GET', 'POST'])
def get_characters(page):
    if request.method == 'POST':
        key_type = request.form.get('type')
        value = request.form.get('filter')
        if value == "":
            return render_template('characters.html', character=paginate(page), filtered=True, page=page)
        if key_type == "films": 
            character = Character.objects(films__icontains=value)
        elif key_type == "starships":
            character = Character.objects(starships__icontains=value)
        elif key_type == "vehicles":
            character = Character.objects(vehicles__icontains=value)
        elif key_type == "planets":
            character = Character.objects(planets__icontains=value)
        
        return render_template('characters.html', character=character, filtered=True, page=page)

    return render_template('characters.html', character=paginate(page), filtered=False, page=page)

if __name__ == '__main__':
    init_db()
    app.run(debug=True,host='0.0.0.0', port=5000)