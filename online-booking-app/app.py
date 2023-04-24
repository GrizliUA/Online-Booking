"""Modules providing Flask realising hosting web-application at local instance"""
from flask import Flask, render_template, request, redirect, make_response



app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
