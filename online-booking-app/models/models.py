from flask_sqlalchemy import SQLAlchemy
import datetime as dt

db = SQLAlchemy()
   
class City(db.Model):
    __tablename__ = 'city'
    city_ID = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    country = db.Column(db.String(100), nullable=False)

class Airport(db.Model):
    __tablename__ = 'airport'
    airport_ID = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    city_ID_FK = db.Column(db.Integer,db.ForeignKey('city.city_ID', ondelete="CASCADE", onupdate="CASCADE") ,nullable=False)
    airport_Name = db.Column(db.String(255), nullable=False)

class Agency(db.Model):
    __tablename__ = 'agency'
    agency_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(45))
    
class PlaneModels(db.Model):
    __tablename__ = 'planemodels'
    model_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_title = db.Column(db.String(45))
    model_capacity = db.Column(db.String(45))
    model_efficient = db.Column(db.String(45))
    model_range = db.Column(db.Integer)

class Plane(db.Model):
    __tablename__ = 'plane'
    plane_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agency_ID_FK = db.Column(db.Integer,db.ForeignKey('agency.agency_ID', ondelete="CASCADE", onupdate="CASCADE") ,nullable=False)
    model_ID_FK = db.Column(db.Integer, db.ForeignKey('planemodels.model_ID', ondelete="CASCADE", onupdate="CASCADE"), nullable = False)

class Flights(db.Model):
    __tablename__ = 'flights'
    flights_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plane_ID_FK = db.Column(db.Integer, db.ForeignKey('plane.plane_ID', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    from_ID_FK = db.Column(db.Integer, nullable=False)
    to_ID_FK = db.Column(db.Integer, nullable=False)
    boarding_Time = db.Column(db.DateTime, nullable=False)
    departure_Time = db.Column(db.DateTime, nullable=False)
    arrival_Time = db.Column(db.DateTime, nullable=False)
    base_Price = db.Column(db.Integer, nullable=False, default = 0) # CALCULATIONS
    gate = db.Column(db.String(45), nullable=False)

class Passenger(db.Model):
    __tablename__ = 'passenger'
    passenger_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    flight_class = db.Column(db.String(20), nullable=False)
    seat = db.Column(db.String(5), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    baggage_weight = db.Column(db.Float, nullable=False)
    passanger_coef = db.Column(db.Integer, nullable=False, default=0)
    pilga = db.Column(db.Integer, nullable=False) # CALCULATIONS

class Flight(db.Model):
    __tablename__ = 'flight'
    flight_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flights_ID = db.Column(db.Integer, db.ForeignKey('flights.flights_ID', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    passanger_ID = db.Column(db.Integer, db.ForeignKey('passenger.passenger_ID', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    price = db.Column(db.Integer)
