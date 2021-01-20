from flask import Flask
import json
import requests
from models import *

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
        print("fail to populate db")

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
        print("fail to populate planets")
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
        print("fail to populate vehicles")
    return Vehicles.get_all()

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
        print("fail to populate films db")

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
        print("fail to populate starships db") 
