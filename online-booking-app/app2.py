"""Modules providing Flask realising hosting web-application at local instance"""
from flask import Flask, render_template, request, redirect, make_response, url_for


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

@app.route('/other_page')
def other_page():
    return render_template('ticket.html')

@app.route('/redirect_to_other_page')
def redirect_to_other_page():
    return redirect(url_for('other_page'))

@app.route('/error_page')
def error_page():
    return render_template('error.html')

@app.route('/redirect_to_error_page')
def redirect_to_error_page():
    return redirect(url_for('error_page'))

@app.route('/passanger_page')
def passanger_page():
    return render_template('passangers.html')

@app.route('/redirect_to_passanger_page')
def redirect_to_passanger_page():
    return redirect(url_for('passanger_page'))

@app.route('/payment_page')
def payment_page():
    return render_template('payment.html')

@app.route('/redirect_to_payment_page')
def redirect_to_payment_page():
    return redirect(url_for('payment_page'))

@app.route('/finish_page')
def finish_page():
    return render_template('finish.html')

@app.route('/redirect_to_finish_page')
def redirect_to_finish_page():
    return redirect(url_for('finish_page'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)