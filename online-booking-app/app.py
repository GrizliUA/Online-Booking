"""Modules providing Flask realising hosting web-application at local instance"""
import json
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, make_response
from flask_restful import Resource, Api
from models.models import db
from database_details import Database_dt

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



test_data = [1,'03.05.2023','04.05.2023']

# class Api(Resource):
#     def get(self):
#         try:
#             flight = Flight(test_data)
#             response = {"uid": flight.uid,
#                         "dep": flight.departure_time,
#                         "arr": flight.arrival_time}
#             return response_200(response)
#         except:
#             return response_400()
# api.add_resource(Api, '/api')







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



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
