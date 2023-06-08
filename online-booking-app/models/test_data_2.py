from models import *
from flask import Flask
from flask_restful import Api
import datetime as dt

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123321@localhost/airport_db'
db.init_app(app)
app.app_context().push()
db.create_all()

# Create plane data
plane_data = [
    {'agency_ID_FK': 1, 'model_ID_FK': 1},
    {'agency_ID_FK': 1, 'model_ID_FK': 2},
    {'agency_ID_FK': 2, 'model_ID_FK': 3}
]

for data in plane_data:
    plane = Plane(**data)
    db.session.add(plane)

db.session.commit()
# Test data for Flights model
flights_data = [
    {
        'plane_ID_FK': 1,
        'from_ID_FK': 1,
        'to_ID_FK': 2,
        'boarding_Time': dt.datetime.now(),
        'departure_Time': dt.datetime.now() + dt.timedelta(hours=1),
        'arrival_Time': dt.datetime.now() + dt.timedelta(hours=2),
        'base_Price': 100,
        'gate': 'Gate 1'
    },
    {
        'plane_ID_FK': 2,
        'from_ID_FK': 2,
        'to_ID_FK': 3,
        'boarding_Time': dt.datetime.now(),
        'departure_Time': dt.datetime.now() + dt.timedelta(hours=3),
        'arrival_Time': dt.datetime.now() + dt.timedelta(hours=4),
        'base_Price': 200,
        'gate': 'Gate 2'
    },
    {
        'plane_ID_FK': 3,
        'from_ID_FK': 3,
        'to_ID_FK': 1,
        'boarding_Time': dt.datetime.now(),
        'departure_Time': dt.datetime.now() + dt.timedelta(hours=5),
        'arrival_Time': dt.datetime.now() + dt.timedelta(hours=6),
        'base_Price': 300,
        'gate': 'Gate 3'
    }
]

for data in flights_data:
    flight = Flights(**data)
    db.session.add(flight)
db.session.commit()
# Test data for Passenger model
passenger_data = [
    {
        'full_name': 'Passenger 1',
        'phone': '123456789',
        'email': 'passenger1@example.com',
        'flight_class': 'Economy',
        'seat': 'A1',
        'birthdate': dt.date(1990, 1, 1),
        'country': 'Country 1',
        'sex': 'Male',
        'baggage_weight': 20.5,
        'passanger_coef': 1,
        'pilga': 100
    },
    {
        'full_name': 'Passenger 2',
        'phone': '987654321',
        'email': 'passenger2@example.com',
        'flight_class': 'Business',
        'seat': 'B2',
        'birthdate': dt.date(1995, 2, 2),
        'country': 'Country 2',
        'sex': 'Female',
        'baggage_weight': 30.5,
        'passanger_coef': 2,
        'pilga': 200
    },
    {
        'full_name': 'Passenger 3',
        'phone': '555555555',
        'email': 'passenger3@example.com',
        'flight_class': 'First Class',
        'seat': 'C3',
        'birthdate': dt.date(1985, 3, 3),
        'country': 'Country 3',
        'sex': 'Male',
        'baggage_weight': 25.5,
        'passanger_coef': 3,
        'pilga': 300
    }
]

for data in passenger_data:
    passenger = Passenger(**data)
    db.session.add(passenger)
db.session.commit()
# Test data for Flight model
flight_data = [
    {'flights_ID': 1, 'passanger_ID': 1, 'price': 100},
    {'flights_ID': 2, 'passanger_ID': 2, 'price': 200},
    {'flights_ID': 3, 'passanger_ID': 3, 'price': 300}
]

for data in flight_data:
    flight = Flight(**data)
    db.session.add(flight)

# Commit the changes to the database
db.session.commit()