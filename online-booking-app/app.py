"""Modules providing Flask realising hosting web-application at local instance"""
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from flask import Flask, render_template, request, redirect, make_response, jsonify, url_for
from flask_restful import Resource, Api
from sqlalchemy.orm import aliased
from models.models import *
from database_details import Database_dt
from datetime import datetime

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{Database_dt.db_user}:{Database_dt.db_password}@{Database_dt.db_host}/{Database_dt.db_title}'
db.init_app(app)
app.app_context().push()
db.create_all()


def response_200(response='OK'):
    """Returns response with code 200"""
    return make_response(response,200)
def response_201(response='Created'):
    """Returns response with code 201"""
    return make_response(response,201)
def response_202(response='Accepted'):
    """Returns response with code 202"""
    return make_response(response,202)
def response_208(response='Already Reported'):
    """Returns response with code 208"""
    return make_response(response,208)
def response_400(response='Bad Request'):
    """Returns response with code 400"""
    return make_response(response,400)
def response_404(response='Not Found'):
    """Returns response with code 404"""
    return make_response(response,404)

@app.route('/error' , methods=['GET'])
def error():
    """Error page function"""
    try:
        return render_template('error.html')
    except:
        return response_400()



def obj_to_list(obj) -> list:
    new_list = []
    for row in obj:
        new_list.append(list((getattr(row, col)) for col in row.__table__.columns.keys()))
    return new_list


def obj_to_json(obj) -> str:
    new_list = []
    for row in obj:
        row_dict = {col: getattr(row, col) for col in row.__table__.columns.keys()}
        new_list.append(row_dict)
    return new_list

# @app.route('/' , methods=['GET'])
# def main():
#     """main page function"""
#     try:
#         return render_template('test.html')
#     except:
#         return response_400()


# @app.route('/' , methods=['GET'])
# def main():
#     """main page function"""
#     try:
#         return render_template('child.html')
#     except:
#         return response_400()

# @app.route('/other_page')
# def other_page():
#     return render_template('ticket.html')

# @app.route('/redirect_to_other_page')
# def redirect_to_other_page():
#     return redirect(url_for('other_page'))



class Cities_Api(Resource):
    def get(self):
        try:
            data = obj_to_json(City.query.all())
            return response_200(data)
        except:
            return response_400()
api.add_resource(Cities_Api, '/cities')


@app.route('/' , methods=['GET', 'POST'])
def main():
    """Main page function"""
    try:
        url = "http://127.0.0.1:5000/cities"
        with urlopen(url) as req:
            res = req.read()
        dict_cities = json.loads(res)
        #print(dict_cities)

        return render_template('childs/ticket.html', cities = dict_cities)
    except:
        return redirect("http://127.0.0.1:5000/error")
    
@app.route('/tickets' , methods=['GET', 'POST'])
def tickets():
    """Main page function"""
    try:
        from_ID_FK = request.args['from_ID_FK']
        to_ID_FK = request.args['to_ID_FK']
        boarding_Time = request.args['date']
        #passengers_count = int(request.args["passengers_count"])
        passengers_count = int(request.args.get('passengers_count'))
        # print(from_ID_FK)
        # print(to_ID_FK)
        # print(boarding_Time)

        url_req = urlencode({"from_ID_FK": from_ID_FK, "to_ID_FK": to_ID_FK, "boarding_Time": boarding_Time})
        #print(url_req)
        url = "http://127.0.0.1:5000/search?" + url_req
        #print(url)

        with urlopen(url) as req:
            res = req.read()
        direct_ticket = json.loads(res)
        #print(direct_ticket2)



        #print(passengers_count)
        #direct_ticket = 
        # direct_ticket = [
        #                 {
        #                     "arrival_Time": "Wed, 07 Jun 2023 21:33:18 GMT",
        #                     "base_Price": 200,
        #                     "boarding_Time": "Wed, 07 Jun 2023 17:33:18 GMT",
        #                     "departure_Time": "Wed, 07 Jun 2023 20:33:18 GMT",
        #                     "flights_ID": 2,
        #                     "from_ID_FK": 1,
        #                     "gate": "Gate 2",
        #                     "plane_ID_FK": 2,
        #                     "to_ID_FK": 3
        #                 }
        # ]
        # undirect_tickets =   [
        #                 {
        #                     "arrival_Time": "Wed, 07 Jun 2023 19:33:18 GMT",
        #                     "base_Price": 100,
        #                     "boarding_Time": "Wed, 07 Jun 2023 17:33:18 GMT",
        #                     "departure_Time": "Wed, 07 Jun 2023 18:33:18 GMT",
        #                     "flights_ID": 1,
        #                     "from_ID_FK": 1,
        #                     "gate": "Gate 1",
        #                     "plane_ID_FK": 1,
        #                     "to_ID_FK": 2
        #                 },
        #                 {
        #                     "arrival_Time": "Wed, 07 Jun 2023 21:33:18 GMT",
        #                     "base_Price": 200,
        #                     "boarding_Time": "Wed, 07 Jun 2023 17:33:18 GMT",
        #                     "departure_Time": "Wed, 07 Jun 2023 20:33:18 GMT",
        #                     "flights_ID": 2,
        #                     "from_ID_FK": 2,
        #                     "gate": "Gate 2",
        #                     "plane_ID_FK": 2,
        #                     "to_ID_FK": 3
        #                 }
        #             ]
        return render_template('childs/tickets.html', direct_ticket = direct_ticket, undirect_tickets = [], passengers_count = passengers_count)
    except:
        return redirect("http://127.0.0.1:5000/error")
    
@app.route('/passangers' , methods=['GET', 'POST'])
def passangers():
    """Main page function"""
    #try:
    tickets_info = []
    direct_ticket = request.args.get('direct_ticket')
    undirect_tickets = request.args.get('undirect_tickets')
    passengers_count = int(request.args.get('passengers_count'))
    # print(direct_ticket)
    # print(undirect_tickets)
    # print(passengers_count)
    if direct_ticket == None:
        return render_template('childs/passangers.html', choiced_ticket = undirect_tickets, passengers_count = passengers_count)
    elif undirect_tickets == None:
        return render_template('childs/passangers.html', choiced_ticket = direct_ticket, passengers_count = passengers_count)
    else:
        return redirect("http://127.0.0.1:5000/error")
    #except:
        #return redirect("http://127.0.0.1:5000/error")

@app.route('/payment' , methods=['GET', 'POST'])
def payment():
    """Main page function"""
    #try:
    choiced_ticket = request.args.get('choiced_ticket')
    payment_info = []
    passenger_info = {
        'full_name': request.form['full_name'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'selected_class': request.form['class'],
        'seat_row': request.form['seat_row'],
        'seat_column': request.form['seat_column'],
        'birthday': request.form['birthday'],
        'country': request.form['country'],
        'sex': request.form['sex']
    }
    #passengers_data = request.form.get('passengersData')
    
    

    return render_template('childs/payment.html', choiced_ticket = choiced_ticket, passenger_info = passenger_info, payment = payment_info)
    #except:
        #return redirect("http://127.0.0.1:5000/error")
    
@app.route('/finish' , methods=['GET', 'POST'])
def finish():
    """Main page function"""
    #try:
    choiced_ticket = request.args.get('choiced_ticket')
    payment_info = []
    passenger_info = request.args.get('passenger_info')
    # card_number = int(request.form['card_number'].replace('-',''))
    # card_expiration_date = request.form['card_expiration_date']
    # card_cvv = int(request.form['card_cvv'])
    # print(card_number)
    # print(card_expiration_date)
    # print(card_cvv)
    # print(type(choiced_ticket))
    # print(choiced_ticket.replace("'",'"'))
    # print(type(passenger_info))
    # print(passenger_info.replace("'",'"'))

    return render_template('childs/finish.html', choiced_ticket = json.loads(choiced_ticket.replace("'",'"')), passenger_info = json.loads(passenger_info.replace("'",'"')), payment = payment_info)
    #except:
        #return redirect("http://127.0.0.1:5000/error")

# class ApiSearch(Resource):
#     def post(self):
#         #try:
#         # data = []
#         # for key, value in request.args.items():
#         #         print(key, value)
#         #         data.append({key: value})
#         # if data == []:
#         #     return response_400()
        
#         # data = ''
        
#         # for key, value in request.args.items():
#         #     data += f'{key} = "{value}", '
#         # data = data

#         # if data == '':
#         #     return response_400()
        
#         #print(data)

#         #from_ID_FK = request.args['departure_city']
#         from_ID_FK = request.args['from_ID_FK']

#         #to_ID_FK = request.args['arrival_city']
#         to_ID_FK = request.args['to_ID_FK']

#         print(type(from_ID_FK), type(to_ID_FK))

#         # 2023-06-07
#         date = request.args['boarding_Time']
#         # print(date)
#         # boarding_Time_start = date
#         # boarding_Time_end = date
#         # data = obj_to_json(Flights.query.filter_by(**eval('dict(' + data + ')')).all())
#         # flights = Flights.query.all()

#         #print(data)

#         data = obj_to_json(Flights.query.filter_by(from_ID_FK=from_ID_FK, to_ID_FK=to_ID_FK, boarding_Time=date).all())
#         # direct_flights = [
#         #     flight for flight in data 
#         #     if flight['from_ID_FK'] == from_ID_FK 
#         #     and flight['to_ID_FK'] == to_ID_FK 
#         #     and flight['boarding_Time'] == date
#         # ]
#         # if data == []:
#         #     flights_alias = aliased(Flights)
#         #     data = obj_to_json(
#         #         db.session.query(Flights)
#         #         .select_from(Flights)
#         #         .join(flights_alias, Flights.to_ID_FK == flights_alias.from_ID_FK)
#         #         .filter(Flights.boarding_Time >= date)
#         #         .all()
#         #     )
#         #     transfer_flights = find_transfer_flights(data)
#         #     data = [entry[0] for entry in transfer_flights]

#         #     data = [entry for entry in data if int(entry['from_ID_FK']) != int(to_ID_FK) and int(entry['to_ID_FK']) != int(from_ID_FK)]
#         #     return response_404(data)

#         return response_200(data)
#         #except:
#             #return response_400()
# api.add_resource(ApiSearch, '/search')


class ApiSearch(Resource):
    def get(self):
        from_ID_FK = request.args['from_ID_FK']
        to_ID_FK = request.args['to_ID_FK']
        boarding_Time = request.args['boarding_Time']
        data = obj_to_json(Flights.query.filter_by(from_ID_FK=from_ID_FK, to_ID_FK=to_ID_FK, boarding_Time=boarding_Time).all())

        if data == []:
            flights_alias = aliased(Flights)
            data = obj_to_json(
                db.session.query(Flights)
                .select_from(Flights)
                .join(flights_alias, Flights.to_ID_FK == flights_alias.from_ID_FK)
                .filter(Flights.boarding_Time >= boarding_Time)
                .all()
            )
            transfer_flights = find_transfer_flights(data)
            data = [entry[0] for entry in transfer_flights]

            data = [entry for entry in data if int(entry['from_ID_FK']) != int(to_ID_FK) and int(entry['to_ID_FK']) != int(from_ID_FK)]
            return response_200(data)
        
        return response_200(data)
api.add_resource(ApiSearch, '/search')

def find_transfer_flights(flights):
    transfer_flights = []
    
    for i in range(len(flights) - 1):
        current_flight = flights[i]
        next_flight = flights[i+1]
        
        if current_flight['to_ID_FK'] == next_flight['from_ID_FK'] and \
                current_flight['departure_Time'] < next_flight['arrival_Time']:
            
            transfer_flights.append((current_flight, next_flight))
    
    return transfer_flights








# class ApiSearch(Resource):
#     def post(self):
#         try:
#             from_ID_FK = request.args['from_ID_FK']
#             to_ID_FK = request.args['to_ID_FK']
#             boarding_Time = request.args['boarding_Time']
#             #direct_flights = obj_to_json(Flights.query.filter_by(from_ID_FK=from_ID_FK, to_ID_FK=to_ID_FK, boarding_Time=boarding_Time).all())
            
#             direct_flights = obj_to_json(Flights.query.filter_by(from_ID_FK=from_ID_FK, to_ID_FK=to_ID_FK, boarding_Time=boarding_Time).all())
#             direct_flights = [
#                 flight for flight in direct_flights 
#                 if flight['from_ID_FK'] == from_ID_FK 
#                 and flight['to_ID_FK'] == to_ID_FK 
#                 and flight['boarding_Time'] == boarding_Time
#             ]
#             # if data == []:
#             #     flights_alias = aliased(Flights)
#             #     data = obj_to_json(
#             #         db.session.query(Flights)
#             #         .select_from(Flights)
#             #         .join(flights_alias, Flights.to_ID_FK == flights_alias.from_ID_FK)
#             #         .filter(Flights.boarding_Time >= boarding_Time)
#             #         .all()
#             #     )
#             #     transfer_flights = find_transfer_flights(data)
#             #     data = [entry[0] for entry in transfer_flights]

#             #     data = [entry for entry in data if int(entry['from_ID_FK']) != int(to_ID_FK) and int(entry['to_ID_FK']) != int(from_ID_FK)]
#             #     return response_404(data)
            
            
            
#             return response_200(direct_flights)
#         except:
#             return response_400()
# api.add_resource(ApiSearch, '/search')

# class ApiSearch(Resource):
#     def post(self):
        
#         # data = ''
        
#         # for key, value in request.args.items():
#         #     data += f'{key} = "{value}", '
#         # data = data
#         # print(data)
#         # if data == '':
#         #     return response_400()
        
#         from_ID_FK = request.args['from_ID_FK']
#         to_ID_FK = request.args['to_ID_FK']
#         date = request.args['boarding_Time']
#         print(date)
#         data = obj_to_json(Flights.query.filter_by(from_ID_FK=from_ID_FK, to_ID_FK=to_ID_FK, boarding_Time=date).all())
#         print(data)
#         if data == []:
#             flights_alias = aliased(Flights)
#             data = obj_to_json(
#                 db.session.query(Flights)
#                 .select_from(Flights)
#                 .join(flights_alias, Flights.to_ID_FK == flights_alias.from_ID_FK)
#                 .filter(Flights.boarding_Time >= date)
#                 .all()
#             )


#             data = [entry for entry in data if entry['from_ID_FK'] != int(to_ID_FK) and entry['to_ID_FK'] != int(from_ID_FK)]

#         return response_200(data)
# api.add_resource(ApiSearch, '/search')


# class Api(Resource):
#     def get(self):
#         #try:
#         flight = Flight()
#         response = {"uid": flight.flight_ID,
#                     "fli_id": flight.flights_ID,
#                     "p_id": flight.passanger_ID,
#                     "price": flight.price,}
#         return response_200(response)
#         #except:
#             #return response_400()
# api.add_resource(Api, '/api')

# class ApiItemSearch(Resource):
#     """Item API Search realization"""
#     def get(self):
#         """API Item Search"""
#         try:
#             data = ''

#             for key, value in request.args.items():
#                 data += f'{key} = "{value}", '
#             data = data[:-2]

#             if data == '':
#                 return response_400()
            

#             item_data = obj_to_list(Items.query.filter_by(**eval('dict(' + data + ')')).all())

#             if not item_data:
#                 return response_404()

#             response = item_response(item_data)

#             return response_200(response)
#         except:
#             return response_400()
# api.add_resource(ApiItemSearch, '/api/item/search/')

# @app.route('/item/searching', methods=['GET', 'POST'])
# def item_searching():
#     """Search page function"""
#     try:
#         if len(request.form["item_label"]) > 0 and len(request.form["item_date"]) > 0:
#             url_req = urlencode({"item_label": request.form["item_label"], "item_date": request.form["item_date"]})
#         elif len(request.form["item_label"]) > 0:
#             url_req = urlencode({"item_label": request.form["item_label"]})
#         elif len(request.form["item_date"]) > 0:
#             url_req = urlencode({"item_date": request.form["item_date"]})
#         url = "http://127.0.0.1:5000/api/item/search/?" + url_req

#         with urlopen(url) as req:
#             res = req.read()
#         dict_res = json.loads(res)
#         values_list = list(dict_res.values())

#         return redirect(f"http://127.0.0.1:5000/item/{values_list[2]}")
#     except:
#         return redirect("http://127.0.0.1:5000/item/search")





















# class ApiCategoryCreate(Resource):
#     """Category API Create realization"""
#     def post(self,category_label):
#         """API Category Create"""
#         try:
#             cur = mysql.connection.cursor()
#             cur.execute(f"INSERT INTO categories (category_label) VALUES ('{category_label}');")
#             mysql.connection.commit()

#             cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_label}'")
#             categories_data = cur.fetchone()
#             cur.close()

#             response = {"category_id": categories_data[0], "category_label": categories_data[1]}
#             return response_201(response)
#         except:
#             try:
#                 cur = mysql.connection.cursor()
#                 cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_label}'")
#                 categories_data = cur.fetchone()
#                 cur.close()

#                 response = {"category_id": categories_data[0], "category_label": categories_data[1]}
#                 return response_208(response)
#             except:
#                 return response_400()
# api.add_resource(ApiCategoryCreate, '/api/category/create/<string:category_label>')


# class ApiCategoryRead(Resource):
#     """Category API Read realization"""
#     def get(self,category_request):
#         """API Category Read"""
#         try:
#             category_request = int(category_request)
#         except:
#             pass
#         try:
#             cur = mysql.connection.cursor()
#             if isinstance(category_request,int):
#                 cur.execute(f"SELECT * FROM categories WHERE category_id = '{category_request}'")
#             else:
#                 cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_request}'")
#             categories_data = cur.fetchone()
#             cur.close()

#             response = {"category_id": categories_data[0], "category_label": categories_data[1]}
#             return response_200(response)
#         except:
#             return response_400()
# api.add_resource(ApiCategoryRead, '/api/category/read/<string:category_request>')


# class ApiCategoryUpdate(Resource):
#     """Category API Update realization"""
#     def put(self,category_request):
#         """API Category Update"""
#         try:
#             category_request = int(category_request)
#         except:
#             pass
#         try:
#             category_label = str(request.args["category_label"])
#             cur = mysql.connection.cursor()

#             if isinstance(category_request,int):
#                 cur.execute(f"UPDATE categories SET category_label = '{category_label}'"
#                             f"WHERE category_id = {category_request};")
#                 mysql.connection.commit()
#                 cur.execute(f"SELECT * FROM categories WHERE category_id = {category_request}")
#             else:
#                 cur.execute(f"UPDATE categories SET category_label = '{category_label}'"
#                             f"WHERE category_label = '{category_request}';")
#                 mysql.connection.commit()
#                 cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_label}';")

#             categories_data = cur.fetchone()
#             cur.close()

#             response = {"category_id": categories_data[0], "category_label": categories_data[1]}
#             return response_202(response)
#         except:
#             return response_400()
# api.add_resource(ApiCategoryUpdate, '/api/category/update/<string:category_request>')


# class ApiCategoryDelete(Resource):
#     """Category API Delete realization"""
#     def delete(self,category_request):
#         """API Category Delete"""
#         try:
#             category_request = int(category_request)
#         except:
#             pass
#         try:
#             cur = mysql.connection.cursor()

#             if isinstance(category_request,int):
#                 cur.execute(f"DELETE FROM categories WHERE category_id = {category_request};")
#                 mysql.connection.commit()
#             else:
#                 cur.execute(f"DELETE FROM categories WHERE category_label = '{category_request}';")
#                 mysql.connection.commit()
#             cur.close()

#             return response_202()
#         except:
#             return response_400()
# api.add_resource(ApiCategoryDelete, '/api/category/delete/<string:category_request>')



# class ApiItemCreate(Resource):
#     """Item API Create realization"""
#     def post(self):
#         """API Item Create"""
#         try:
#             item_label = request.args['item_label']

#             request_keys,request_values = '',''
#             for key, value in request.args.items():
#                 request_keys += f'{key} , '
#                 request_values += f"'{value}' , "
#             request_keys = request_keys[:-3]
#             request_values = request_values[:-3]

#             cur = mysql.connection.cursor()
#             cur.execute(f"INSERT INTO items ({request_keys}) VALUES ({request_values});")
#             mysql.connection.commit()

#             cur.execute(f"SELECT * FROM items WHERE item_label = '{item_label}'")
#             item_data = cur.fetchone()
#             cur.close()

#             response = {"item_id": item_data[0],
#                         "item_category_id": item_data[1],
#                         "item_label": item_data[2],
#                         "item_info": item_data[3],
#                         "item_video_link": item_data[4],
#                         "item_photo_link": item_data[5],
#                         "item_date": item_data[6],
#                         "item_value": item_data[7]}
#             return response_201(response)
#         except:
#             return response_400()
# api.add_resource(ApiItemCreate, '/api/item/create/')


# class ApiItemRead(Resource):
#     """Item API Read realization"""
#     def get(self,item_request):
#         """API Item Read"""
#         try:
#             item_request = int(item_request)
#         except:
#             pass
#         try:
#             cur = mysql.connection.cursor()

#             if isinstance(item_request,int):
#                 cur.execute(f"SELECT * FROM items WHERE item_id = '{item_request}'")
#             else:
#                 cur.execute(f"SELECT * FROM items WHERE item_label = '{item_request}'")

#             item_data = cur.fetchone()
#             cur.close()

#             response = {"item_id": item_data[0],
#                         "item_category_id": item_data[1],
#                         "item_label": item_data[2],
#                         "item_info": item_data[3],
#                         "item_video_link": item_data[4],
#                         "item_photo_link": item_data[5],
#                         "item_date": item_data[6],
#                         "item_value": item_data[7]}
#             return response_200(response)
#         except:
#             return response_400()
# api.add_resource(ApiItemRead, '/api/item/read/<string:item_request>')


# class ApiItemUpdate(Resource):
#     """Item API Update realization"""
#     def put(self,item_request):
#         """API Item Update"""
#         try:
#             item_request = int(item_request)
#         except:
#             pass
#         try:
#             item_label = request.args['item_label']
#             item_update = ''
#             for key, value in request.args.items():
#                 item_update += f"{key} = '{value}' , "
#             item_update = item_update[:-3]

#             cur = mysql.connection.cursor()

#             if isinstance(item_request,int):
#                 cur.execute(f"UPDATE items SET {item_update} WHERE item_id = '{item_request}';")
#                 mysql.connection.commit()
#                 cur.execute(f"SELECT * FROM items WHERE item_label = '{item_label}';")
#             else:
#                 cur.execute(f"UPDATE items SET {item_update} WHERE item_label = '{item_request}';")
#                 mysql.connection.commit()
#                 cur.execute(f"SELECT * FROM items WHERE item_label = '{item_label}';")

#             item_data = cur.fetchone()
#             response = {"item_id": item_data[0],
#                         "item_category_id": item_data[1],
#                         "item_label": item_data[2],
#                         "item_info": item_data[3],
#                         "item_video_link": item_data[4],
#                         "item_photo_link": item_data[5],
#                         "item_date": item_data[6],
#                         "item_value": item_data[7]}
#             cur.close()
#             return response_200(response)
#         except:
#             return response_400()
# api.add_resource(ApiItemUpdate, '/api/item/update/<string:item_request>')


# class ApiItemDelete(Resource):
#     """Item API Delete realization"""
#     def delete(self,item_request):
#         """API Item Delete"""
#         try:
#             item_request = int(item_request)
#         except:
#             pass
#         try:
#             cur = mysql.connection.cursor()

#             if isinstance(item_request,int):
#                 cur.execute(f"DELETE FROM items WHERE item_id = {item_request};")
#             elif isinstance(item_request,str):
#                 cur.execute(f"DELETE FROM items WHERE item_label = '{item_request}';")
#                 return response_400()
#             else: return response_400()

#             mysql.connection.commit()
#             return response_202()
#         except:
#             return response_400()
# api.add_resource(ApiItemDelete, '/api/item/delete/<string:item_request>')


# class ApiItemSearch(Resource):
#     """Item API Search realization"""
#     def get(self):
#         """API Item Search"""
#         try:
#             item_keys,item_values = [],[]
#             for key, value in request.args.items():
#                 item_keys.append(key)
#                 item_values.append(value)

#             cur = mysql.connection.cursor()
#             if not item_keys:
#                 return response_400()

#             for i in range(0,len(item_keys)):
#                 cur.execute(f"SELECT * FROM items WHERE {item_keys[i]} = '{item_values[i]}';")
#                 item_data = cur.fetchone()
#                 if item_data:
#                     break

#             if not item_data:
#                 return response_404()
#             cur.close()
#             response = {"item_id": item_data[0],
#                         "item_category_id": item_data[1],
#                         "item_label": item_data[2],
#                         "item_info": item_data[3],
#                         "item_video_link": item_data[4],
#                         "item_photo_link": item_data[5],
#                         "item_date": item_data[6],
#                         "item_value": item_data[7]}

#             return response_200(response)
#         except:
#             return response_400()
# api.add_resource(ApiItemSearch, '/api/item/search/')


@app.route('/error_page')
def error_page():
    return render_template('error.html')

@app.route('/redirect_to_error_page')
def redirect_to_error_page():
    return redirect(url_for('error_page'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
