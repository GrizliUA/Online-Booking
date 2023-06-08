from models import *
from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:123321@localhost/airport_db'
db.init_app(app)
app.app_context().push()
db.create_all()

agency_data = [
    {'title': 'Agency 1'},
    {'title': 'Agency 2'},
    {'title': 'Agency 3'}
]

for data in agency_data:
    agency = Agency(**data)
    db.session.add(agency)

db.session.commit()

city_data = [
    {'country': 'Country 1'},
    {'country': 'Country 2'},
    {'country': 'Country 3'}
]

for data in city_data:
    city = City(**data)
    db.session.add(city)

db.session.commit()

# Test data for Airport model
airport_data = [
    {'city_ID_FK': 1, 'airport_Name': 'Airport 1'},
    {'city_ID_FK': 2, 'airport_Name': 'Airport 2'},
    {'city_ID_FK': 3, 'airport_Name': 'Airport 3'}
]

for data in airport_data:
    airport = Airport(**data)
    db.session.add(airport)
db.session.commit()

# Test data for PlaneModels model
plane_models_data = [
    {'model_title': 'Model 1', 'model_capacity': 'Capacity 1', 'model_efficient': 'Efficient 1', 'model_range': 1000},
    {'model_title': 'Model 2', 'model_capacity': 'Capacity 2', 'model_efficient': 'Efficient 2', 'model_range': 2000},
    {'model_title': 'Model 3', 'model_capacity': 'Capacity 3', 'model_efficient': 'Efficient 3', 'model_range': 3000}
]


for data in plane_models_data:
    plane_model = PlaneModels(**data)
    db.session.add(plane_model)

db.session.commit()


# from models import *
# from flask import Flask
# from flask_restful import Api

# app = Flask(__name__)
# api = Api(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:123321@localhost/airport_db'
# db.init_app(app)
# app.app_context().push()
# db.create_all()

# # Додавання даних в таблицю "Agency"
# agency_data = [
#     {'title': f'Agency {i+1}'} for i in range(20)
# ]

# for data in agency_data:
#     agency = Agency(**data)
#     db.session.add(agency)

# db.session.commit()

# # Додавання даних в таблицю "City"
# city_data = [
#     {'country': f'Country {i+1}'} for i in range(20)
# ]

# for data in city_data:
#     city = City(**data)
#     db.session.add(city)

# db.session.commit()

# # Додавання даних в таблицю "Airport"
# airport_data = [
#     {'city_ID_FK': i+1, 'airport_Name': f'Airport {i+1}'} for i in range(20)
# ]

# for data in airport_data:
#     airport = Airport(**data)
#     db.session.add(airport)

# db.session.commit()

# # Додавання даних в таблицю "PlaneModels"
# plane_models_data = [
#     {'model_title': f'Model {i+1}', 'model_capacity': f'Capacity {i+1}', 'model_efficient': f'Efficient {i+1}', 'model_range': (i+1)*1000} for i in range(20)
# ]

# for data in plane_models_data:
#     plane_model = PlaneModels(**data)
#     db.session.add(plane_model)

# db.session.commit()
