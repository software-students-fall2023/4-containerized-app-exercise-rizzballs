"""Module designed to supplement front end webpage"""
import os
import datetime
import sys
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    session,
)
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId

app = Flask("project4")


@app.route("/")
def root_page():
    """Root page route"""
    return render_template("root.html")


@app.route("/analyze_data", methods=["POST"])
def anaylze_data():
    """Analyze data by sending it to the ml client"""
    return


if __name__ == "__main__":
    PORT = os.getenv("PORT", 5000)
    app.run(debug=True, port=PORT)
