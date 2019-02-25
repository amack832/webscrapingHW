from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_nasa


app = Flask(__name__)

# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

    mars_data = mongo.db.mars_data.find_one()

    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data

    data =  scrape_nasa.scrape()
    mars_data.update({},data,upsert=True)
    return redirect('/', code = 302)



if __name__ == "__main__":
    app.run(debug=True)