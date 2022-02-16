from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marshw_db")

@app.route("/")
def index():
    mars_info = mongo.db.mars_scraped.find_one()
    # print(mars)
    return render_template("index.html", data = mars_info)

@app.route("/scrape")
def scrape():  
    my_scrape = scrape_mars.scrape_info()
    print(my_scrape)
    
    mongo.db.mars_scraped.update_one({}, {"$set": my_scrape}, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)