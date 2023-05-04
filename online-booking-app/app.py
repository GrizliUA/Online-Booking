"""Modules providing Flask realising hosting web-application at local instance"""
from flask import Flask, render_template, request, redirect, make_response


app = Flask(__name__)

def response_400(response='Bad Request'):
    """Returns response with code 400"""
    return make_response(response,400)


@app.route('/' , methods=['GET'])
def main():
    """main page function"""
    try:
        return render_template('child.html')
    except:
        return response_400()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
