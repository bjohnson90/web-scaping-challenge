# 1. import Flask
import json
import pymongo
from flask import Flask, render_template, redirect
from scrape_mars import scrape
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Declare the database
db = client.mars
data = db.scrape

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    result = data.find()
    for item in result:
        doc = item
    print("Server received request for 'Home' page...")
    return render_template('index.html', doc=doc)


# 4. Define what to do when a user hits the /about route
@app.route("/scrape")
def about():
    print("Server received request for 'scrape'")
    scraped_data = scrape()
    data.update({}, scraped_data , upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
