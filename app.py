from flask import Flask, render_template, request
import json
from mongoengine import connect
import requests
from models import Character
from populatedb import *

app = Flask(__name__)

def init_db():
    connection = connect(db='star-wars-app', host='db', port=27017)
    return connection

def paginate(page_num):
    skips = 10 * page_num - 1

    cursor = Character.objects.order_by('name', 'gender', 'mass', 'height').skip(skips).limit(10)
    return [x for x in cursor]

@app.route('/db', methods=['GET'])
def db():
    populate_db()
    return Character.objects.to_json()

@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.objects.order_by('-calc')
    return render_template('starships.html', starships=starships)


@app.route('/<int:page>', methods=['GET', 'POST'])
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