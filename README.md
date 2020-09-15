# star-wars

This project retrieves info from the star wars swapi.api


Chosen stack:
    - Python (Flask and Jinja)
    - Mongodb
    - Docker / Docker-Compose

## Run the project:
```bash
git clone https://github.com/tlnob/star-wars.git
```

```bash
cd star-wars
```

```bash
docker-compose up
```
- The Docker containers run on ports 5000 and 27017, so they must be available

## Routes:

### populate database 
This should take a while, there are lots of data to be loaded
 -  localhost:5000/db

### ui routes:
##### - character info, page starts from 1
 - localhost:5000/<page>
##### - starships info:
  - localhost:5000/starships

